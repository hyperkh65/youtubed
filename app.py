import streamlit as st
import yt_dlp
import os
import platform

# 다운로드 경로 가져오기 함수
def get_downloads_path():
    if platform.system() == 'Windows':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif platform.system() == 'Darwin':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:  # Linux
        return os.path.join(os.path.expanduser('~'), 'Downloads')

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
def download_video(url, output_path, progress_bar, status_text):
    """YouTube 비디오 또는 채널 다운로드 함수"""
    try:
        status_text.text("정보를 가져오는 중...")
        
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [lambda d: update_progress(d, progress_bar, status_text)],
            'logger': MyLogger(),
            'verbose': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            format_options = {f"{f['format_id']} ({f['height']}p)": f['format_id'] for f in formats if 'height' in f}

            if not format_options:
                return False, "사용 가능한 형식이 없습니다."
            
            selected_format = st.selectbox("다운로드할 형식 선택", list(format_options.keys()))
            ydl_opts['format'] = format_options[selected_format]
            status_text.text(f"'{info.get('title', 'video')}' 다운로드 시작...")
            ydl.download([url])
            return True, f"다운로드 완료: {info.get('title', 'video')}"
    
    except Exception as e:
        return False, f"다운로드 중 오류가 발생했습니다: {str(e)}"

# Streamlit UI 구성
def main():
    st.title("YouTube 비디오 다운로드기")
    st.write("유튜브 비디오 및 채널을 다운로드합니다.")
    
    url = st.text_input("YouTube 비디오 또는 채널 URL:")
    output_path = get_downloads_path()
    
    if st.button("다운로드 시작"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        success, message = download_video(url, output_path, progress_bar, status_text)
        
        if success:
            st.success(message)
        else:
            st.error(message)

if __name__ == "__main__":
    main()
