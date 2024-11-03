import streamlit as st
import yt_dlp
import os
from datetime import datetime
from pathlib import Path

def get_downloads_path():
    """서버의 다운로드 폴더 경로 생성"""
    downloads_path = Path.cwd() / "downloads"  # 현재 경로에 downloads 폴더 생성
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
                    # 진척률(퍼센트)을 추출하여 반영
                    percent = float(progress_text.split('%')[0].split()[-1])
                    st.session_state['progress'] = percent / 100  # 0~1 사이 값으로 변환
                    st.session_state['status_text'] = progress_text
                except:
                    pass

    def warning(self, msg):
        st.warning(msg)

    def error(self, msg):
        st.error(msg)

def download_video(url, output_path, progress_bar, status_text):
    """단순히 URL을 받아 YouTube 비디오 다운로드"""
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'logger': MyLogger(),
            'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],  # 진척률 업데이트
            'verbose': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            title = info.get('title', 'video')
            return True, f"다운로드 완료: {title}", file_path
    except Exception as e:
        return False, f"다운로드 중 오류가 발생했습니다: {str(e)}", None

def update_progress(d, progress_bar, status_text):
    """다운로드 진행 상태 업데이트"""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        
        if total_bytes:
            progress = downloaded_bytes / total_bytes
            progress_bar.progress(progress)
            
            # 다운로드 속도와 ETA 계산
            speed = d.get('speed', 0)
            if speed:
                speed_mb = speed / 1024 / 1024  # MB/s로 변환
                eta = d.get('eta', 0)
                status = f'다운로드 중... {progress:.1%} ({speed_mb:.1f} MB/s, {eta}초 남음)'
                status_text.text(status)
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_text.text('다운로드 완료! 파일 처리 중...')

def main():
    st.set_page_config(page_title="YouTube 단순 다운로드", layout="wide")
    st.title("YouTube 단순 다운로드")
    st.caption("버전 0.3")

    # 제품 키 인증
    if 'product_key_verified' not in st.session_state:
        st.session_state.product_key_verified = False

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
        
        # 저장 경로 표시 (현재 경로에 downloads 폴더)
        save_path = get_downloads_path()
        st.info(f"다운로드 위치: {save_path}")
        
        # 다운로드 버튼 및 진행 상태
        if st.button("다운로드 시작", type="primary", disabled=not url):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner('다운로드 준비 중...'):
                success, message, file_path = download_video(url, save_path, progress_bar, status_text)
                
                if success:
                    st.success(message)
                    
                    # 다운로드 링크 생성
                    with open(file_path, "rb") as file:
                        btn = st.download_button(
                            label="로컬로 다운로드",
                            data=file,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4"
                        )
                else:
                    st.error(message)

    # 푸터
    st.markdown("---")
    st.caption("Copyright all reserved by 미라쿨")

if __name__ == "__main__":
    main()
