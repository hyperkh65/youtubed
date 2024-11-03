import streamlit as st
import yt_dlp
import os
from datetime import datetime
import tempfile
from pathlib import Path
import time

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
                    # Extract percentage from the progress text
                    percent = float(progress_text.split('%')[0].split()[-1])
                    st.session_state['progress'] = percent / 100
                    st.session_state['status_text'] = progress_text
                except:
                    pass
    
    def warning(self, msg):
        st.warning(msg)
    
    def error(self, msg):
        st.error(msg)

def download_video(url, output_path, progress_bar, status_text):
    """YouTube 비디오 다운로드 함수"""
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],
            'logger': MyLogger(),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, "다운로드가 완료되었습니다."
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
        st.session_state.download_path = os.path.expanduser("~/Downloads")
    
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
    
    # 메인 다운로드 섹션
    if st.session_state.product_key_verified:
        st.subheader("YouTube 동영상 다운로드")
        
        # URL 입력
        url = st.text_input("YouTube URL을 입력하세요:")
        
        # 저장 경로 설정
        col1, col2 = st.columns([3, 1])
        with col1:
            save_path = st.text_input(
                "저장 경로:",
                value=st.session_state.download_path,
                key="path_input"
            )
        with col2:
            if st.button("폴더 선택"):
                root = tk.Tk()
                root.withdraw()  # tkinter 창 숨기기
                folder_path = filedialog.askdirectory()
                if folder_path:
                    st.session_state.download_path = folder_path
                    st.rerun()
        
        # 품질 선택
        quality = st.selectbox(
            "다운로드 품질 선택:",
            ["최고 품질", "720p", "480p", "360p"],
            index=0
        )
        
        # 다운로드 버튼 및 진행 상태
        if st.button("다운로드", type="primary"):
            if url and save_path:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                with st.spinner('다운로드 준비 중...'):
                    success, message = download_video(url, save_path, progress_bar, status_text)
                    if success:
                        st.success(message)
                        # 다운로드 완료 후 진행바 리셋
                        time.sleep(1)
                        progress_bar.empty()
                        status_text.empty()
                    else:
                        st.error(message)
            else:
                st.warning("URL과 저장 경로를 모두 입력해주세요.")
        
        # 다운로드 기록
        if 'download_history' not in st.session_state:
            st.session_state.download_history = []
        
        if st.session_state.download_history:
            st.subheader("다운로드 기록")
            for item in st.session_state.download_history:
                st.text(f"{item['date']} - {item['title']}")
    
    # 푸터
    st.markdown("---")
    st.caption("Copyright all reserved by 미라쿨")

if __name__ == "__main__":
    main()
