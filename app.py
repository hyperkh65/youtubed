import streamlit as st
import yt_dlp
import os
from datetime import datetime
import platform
from pathlib import Path
import re

# 다운로드 경로 가져오기 함수
def get_downloads_path():
    if platform.system() == 'Windows':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif platform.system() == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:  # Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

# 제품 키 검증 함수 (필요 시 추가)
def verify_product_key(product_key):
    # 예시로 단순한 키 검증 로직을 사용
    return product_key == "YOUR_PRODUCT_KEY"

# 로깅 클래스
class MyLogger:
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

# 채널 URL 확인 함수
def is_channel_url(url):
    return 'youtube.com/channel/' in url or 'youtube.com/c/' in url

# 진행 상황 업데이트 함수
def update_progress(d, progress_bar, status_text):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', None)
        downloaded_bytes = d.get('downloaded_bytes', None)
        if total_bytes is not None and downloaded_bytes is not None:
            progress = downloaded_bytes / total_bytes
            progress_bar.progress(progress)
            status_text.text(f"다운로드 중: {d['filename']} ({downloaded_bytes / 1024:.2f} KB / {total_bytes / 1024:.2f} KB)")

# 비디오 다운로드 함수
def download_video(url, output_path, progress_bar, status_text, quality_format, limit=None):
    """YouTube 비디오 또는 채널 다운로드 함수"""
    try:
        status_text.text("정보를 가져오는 중...")
        
        # `postprocessors`를 제거하여 ffmpeg 없이 동작하도록 설정
        ydl_opts = {
            'format': quality_format,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],
            'logger': MyLogger(),
            'verbose': True,
        }
        
        if is_channel_url(url):
            if limit:
                ydl_opts.update({'playlistend': limit})
            status_text.text("채널의 영상 목록을 가져오는 중...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if is_channel_url(url):
                channel_name = info.get('channel', 'Unknown Channel')
                total_videos = len(info['entries']) if limit is None else min(len(info['entries']), limit)
                status_text.text(f"'{channel_name}' 채널에서 {total_videos}개의 영상을 다운로드합니다...")
                
                for i, entry in enumerate(info['entries'][:total_videos], 1):
                    video_url = entry['webpage_url']
                    title = entry['title']
                    status_text.text(f"({i}/{total_videos}) '{title}' 다운로드 중...")
                    ydl.download([video_url])
                
                return True, f"채널 다운로드 완료: {channel_name} ({total_videos}개 영상)"
            else:
                title = info.get('title', 'video')
                status_text.text(f"'{title}' 다운로드 시작...")
                ydl.download([url])
                return True, f"다운로드 완료: {title}"
                
    except Exception as e:
        return False, f"다운로드 중 오류가 발생했습니다: {str(e)}"

# 품질 옵션 설정
quality_options = {
    "최고 품질 (비디오/오디오)": "best",
    "1080p (단일 파일)": "22",  # 22번 포맷은 720p+오디오 포함된 MP4
    "720p (단일 파일)": "22",   # 22번 포맷은 720p+오디오 포함된 MP4
    "360p (단일 파일)": "18"    # 18번 포맷은 360p+오디오 포함된 MP4
}

# Streamlit UI 구성
def main():
    st.title("YouTube 비디오 다운로드기")
    st.write("유튜브 비디오 및 채널을 다운로드합니다.")
    
    url = st.text_input("YouTube 비디오 또는 채널 URL:")
    output_path = get_downloads_path()
    quality_format = st.selectbox("다운로드 품질 선택", list(quality_options.keys()))
    selected_quality = quality_options[quality_format]
    limit = st.number_input("다운로드할 비디오 수 (0은 전체):", min_value=0, value=0, step=1)
    
    if st.button("다운로드 시작"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        if limit == 0:
            limit = None
        
        success, message = download_video(url, output_path, progress_bar, status_text, selected_quality, limit)
        
        if success:
            st.success(message)
        else:
            st.error(message)

if __name__ == "__main__":
    main()
