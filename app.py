import streamlit as st
import yt_dlp
import os
from datetime import datetime
import hashlib

def verify_product_key(input_key):
    """제품 키 검증"""
    correct_key = "7977"
    return input_key == correct_key

def download_video(url, output_path):
    """YouTube 비디오 다운로드 함수"""
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'progress': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True, "다운로드가 완료되었습니다."
    except Exception as e:
        return False, f"다운로드 중 오류가 발생했습니다: {str(e)}"

def main():
    st.set_page_config(page_title="YouTube 동영상 다운로드 프로그램", layout="wide")
    
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
    
    # 제품 키 입력 섹션
    with st.expander("제품 키 인증", expanded=not st.session_state.product_key_verified):
        product_key = st.text_input("제품 키를 입력하세요:", type="password")
        if st.button("인증하기"):
            if verify_product_key(product_key):
                st.session_state.product_key_verified = True
                st.success("제품 키가 인증되었습니다!")
                st.rerun()
            else:
                st.error("잘못된 제품 키입니다. 다시 확인해주세요.")
    
    # 메인 다운로드 섹션
    if st.session_state.product_key_verified:
        st.subheader("YouTube 동영상 다운로드")
        
        # URL 입력
        url = st.text_input("YouTube URL을 입력하세요:")
        
        # 저장 경로 설정
        save_path = st.text_input("저장 경로를 입력하세요:", 
                                value=os.path.expanduser("~/Downloads"),
                                help="기본 경로는 '다운로드' 폴더입니다.")
        
        # 다운로드 버튼
        if st.button("다운로드", type="primary"):
            if url and save_path:
                with st.spinner('다운로드 중...'):
                    success, message = download_video(url, save_path)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
            else:
                st.warning("URL과 저장 경로를 모두 입력해주세요.")
    
    # 푸터
    st.markdown("---")
    st.caption("Copyright all reserved by 미라쿨")

if __name__ == "__main__":
    main()
