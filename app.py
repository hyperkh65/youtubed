import streamlit as st
import yt_dlp
import os
from datetime import datetime
import tempfile
from pathlib import Path

def verify_product_key(input_key):
    """제품 키 검증"""
    correct_key = "7977"
    return input_key == correct_key

def get_directory_from_file(uploaded_file):
    """업로드된 파일의 경로를 통해 디렉토리 경로 추출"""
    if uploaded_file:
        # 임시 파일로 저장하고 그 경로를 사용
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        return os.path.dirname(temp_path)
    return None

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
        ydl_opts = {
            'format': quality_format,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],
            'logger': MyLogger(),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 먼저 영상 정보 가져오기
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
            
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
    st.caption("Version 0.1")
    
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
        
        # 저장 경로 설정 (3가지 방법 제공)
        st.subheader("저장 경로 선택")
        path_method = st.radio(
            "저장 경로 선택 방법:",
            ["기본 경로 사용", "경로 직접 입력", "폴더 선택 (파일 업로드)"]
        )
        
        if path_method == "기본 경로 사용":
            save_path = os.path.join(os.getcwd(), "downloads")
            st.info(f"현재 저장 경로: {save_path}")
            
        elif path_method == "경로 직접 입력":
            save_path = st.text_input("저장할 경로를 입력하세요:", value=os.path.join(os.getcwd(), "downloads"))
            try:
                os.makedirs(save_path, exist_ok=True)
                st.success(f"저장 경로가 설정되었습니다: {save_path}")
            except Exception as e:
                st.error(f"경로 생성 중 오류가 발생했습니다: {str(e)}")
                
        else:  # "폴더 선택 (파일 업로드)"
            st.info("원하는 폴더에서 아무 파일이나 하나 선택하면, 해당 폴더가 저장 경로로 설정됩니다.")
            uploaded_file = st.file_uploader("폴더 선택을 위한 파일 업로드", type=['txt', 'pdf', 'png', 'jpg'])
            if uploaded_file:
                save_path = get_directory_from_file(uploaded_file)
                st.success(f"선택된 저장 경로: {save_path}")
            else:
                save_path = None
                st.warning("파일을 업로드하여 저장 경로를 선택해주세요.")
        
        # 다운로드 버튼 및 진행 상태
        if st.button("다운로드 시작", type="primary", disabled=not (url and save_path)):
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
