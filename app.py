import streamlit as st
import yt_dlp
import os
from datetime import datetime
import platform
from pathlib import Path

def get_downloads_path():
    """운영체제에 따른 다운로드 경로 반환"""
    home = Path.home()
    downloads_path = home / "Downloads"
    
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

def download_video(url):
    """YouTube 비디오 다운로드 함수"""
    try:
        downloads_path = get_downloads_path()
        ydl_opts = {
            'outtmpl': os.path.join(downloads_path, '%(title)s.%(ext)s'),
            'progress_hooks': [update_progress],
            'logger': MyLogger(),
            'format': 'best',  # 최고 품질로 다운로드
            'noplaylist': True,  # 플레이리스트는 다운로드하지 않음
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)  # 직접 다운로드
            title = info.get('title', 'video')
            return True, f"다운로드 완료: {title}"
    except Exception as e:
        return False, f"다운로드 중 오류가 발생했습니다: {str(e)}"

def update_progress(d):
    """다운로드 진행 상황 업데이트"""
    if d['status'] == 'downloading':
        try:
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded_bytes = d.get('downloaded_bytes', 0)
            if total_bytes:
                progress = downloaded_bytes / total_bytes
                st.session_state['progress'] = progress
                st.session_state['status_text'] = f'다운로드 중... {progress:.1%}'
        except:
            pass
    elif d['status'] == 'finished':
        st.session_state['progress'] = 1.0
        st.session_state['status_text'] = '다운로드 완료!'

def main():
    st.set_page_config(page_title="YouTube 동영상 다운로드 프로그램", layout="wide")
    
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
    if 'progress' not in st.session_state:
        st.session_state.progress = 0.0
    if 'status_text' not in st.session_state:
        st.session_state.status_text = ""

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
        
        # 다운로드 버튼 및 진행 상태
        if st.button("다운로드 시작", type="primary", disabled=not url):
            with st.spinner('다운로드 준비 중...'):
                success, message = download_video(url)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        # 진행률 표시
        progress_bar = st.progress(st.session_state.progress)
        status_text = st.empty()
        status_text.text(st.session_state.status_text)

if __name__ == "__main__":
    main()
