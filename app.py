import streamlit as st
import yt_dlp
import os
from datetime import datetime
import platform
from pathlib import Path

def get_downloads_path():
    """운영체제에 따른 바탕화면/downloads 경로 반환"""
    system = platform.system()
    home = Path.home()
    
    if system == "Windows":
        downloads_path = home / "Desktop" / "downloads"
    elif system == "Darwin":  # macOS
        downloads_path = home / "Desktop" / "downloads"
    else:  # Linux 등 기타 운영체제
        downloads_path = home / "Desktop" / "downloads"
    
    # downloads 폴더가 없으면 생성
    if not downloads_path.exists():
        downloads_path.mkdir(parents=True)
    
    return str(downloads_path)

def verify_product_key(input_key):
    """제품 키 검증"""
    correct_key = "7977"
    return input_key == correct_key

class MyLogger:
    def debug(self, msg):
        if msg.startswith('[download]'):
            progress_text = msg.strip()
            if '%' in progress_text:
                try:
                    percent = float(progress_text.split('%')[0].split()[-1])
                    st.session_state['progress'] = percent / 100
                    st.session_state['status_text'] = progress_text
                except:
                    pass
    
    def warning(self, msg):
        st.warning(msg)
    
    def error(self, msg):
        st.error(msg)

def download_video(url, output_path, progress_bar, status_text, quality_format):
    """YouTube 비디오 다운로드 함수"""
    try:
        status_text.text("영상 정보를 가져오는 중...")
        
        ydl_opts = {
            'format': quality_format,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],
            'logger': MyLogger(),
            'verbose': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 영상 정보 가져오기
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            
            # 다운로드 시작 전 상태 표시
            status_text.text(f"'{title}' 다운로드 시작...")
            
            # 다운로드 실행
            ydl.download([url])
            
            return True, f"다운로드 완료: {title}"
    except Exception as e:
        return False, f"다운로드 중 오류가 발생했습니다: {str(e)}"

def update_progress(d, progress_bar, status_text):
    if d['status'] == 'downloading':
        try:
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            
            if total_bytes:
                progress = downloaded_bytes / total_bytes
                progress_bar.progress(progress)
                
                # Calculate download speed and ETA
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / 1024 / 1024  # Convert to MB/s
                    eta = d.get('eta', 0)
                    status = f'다운로드 중... {progress:.1%} ({speed_mb:.1f} MB/s, {eta}초 남음)'
                    status_text.text(status)
        except:
            pass
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_text.text('다운로드 완료! 파일 처리 중...')

def main():
    st.set_page_config(
        page_title="YouTube 동영상 다운로드 프로그램",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 타이틀 및 로고
    st.title("Quickgrab Youtube")
    st.caption("Version 0.2")
    
    # 경고문
    st.warning("""
    주의사항:
    - 동영상을 저작권자 허락 없이 무단으로 다운받는 행위는 저작권 침해 등 법적 책임을 질 수 있습니다.
    - 불법사용에 대한 일체 행위에 본 프로그램 제작자는 아무런 법적 책임을 지지 않습니다.
    """)
    
    # 세션 상태 초기화
    if 'product_key_verified' not in st.session_state:
        st.session_state.product_key_verified = False
    
    # 사이드바에 제품 키 입력 섹션
    with st.sidebar:
        st.subheader("제품 키 인증")
        if not st.session_state.product_key_verified:
            product_key = st.text_input("제품 키를 입력하세요:", type="password")
            if st.button("인증하기"):
                if verify_product_key(product_key):
                    st.session_state.product_key_verified = True
                    st.success("제품 키가 인증되었습니다!")
                    st.rerun()
                else:
                    st.error("잘못된 제품 키입니다. 다시 확인해주세요.")
        else:
            st.success("인증됨 ✓")
            
        # 다운로드 품질 선택
        st.subheader("다운로드 설정")
        quality_options = {
            "최고 품질": "bestvideo+bestaudio/best",
            "1080p": "137+140/best",
            "720p": "22/best",
            "480p": "135+140/best",
            "360p": "18/best",
            "음성만": "bestaudio/best"
        }
        selected_quality = st.selectbox(
            "품질 선택:",
            list(quality_options.keys()),
            index=0
        )
    
    # 메인 다운로드 섹션
    if st.session_state.product_key_verified:
        st.subheader("YouTube 동영상 다운로드")
        
        # URL 입력
        url = st.text_input("YouTube URL을 입력하세요:")
        
        # 저장 경로 표시 (바탕화면/downloads 고정)
        save_path = get_downloads_path()
        st.info(f"다운로드 위치: {save_path}")
        
        # 다운로드 버튼 및 진행 상태
        if st.button("다운로드 시작", type="primary", disabled=not url):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner('다운로드 준비 중...'):
                success, message = download_video(
                    url, 
                    save_path, 
                    progress_bar, 
                    status_text,
                    quality_options[selected_quality]
                )
                if success:
                    st.success(message)
                    # 다운로드 기록 저장
                    if 'download_history' not in st.session_state:
                        st.session_state.download_history = []
                    st.session_state.download_history.append({
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'url': url,
                        'path': save_path
                    })
                else:
                    st.error(message)
        
        # 다운로드 기록 표시
        if 'download_history' in st.session_state and st.session_state.download_history:
            st.subheader("최근 다운로드 기록")
            for item in reversed(st.session_state.download_history[-5:]):  # 최근 5개만 표시
                with st.expander(f"다운로드 - {item['date']}"):
                    st.write(f"URL: {item['url']}")
                    st.write(f"저장 경로: {item['path']}")
    
    # 푸터
    st.markdown("---")
    st.caption("Copyright all reserved by 미라쿨")

if __name__ == "__main__":
    main()
