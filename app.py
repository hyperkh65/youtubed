import streamlit as st
import yt_dlp
import os
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_channel_info(url):
    """채널 정보와 비디오 목록을 가져옵니다."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(url, download=False)
            return result
        except Exception as e:
            st.error(f"채널 정보 가져오기 실패: {str(e)}")
            return None

def format_duration(duration):
    """초 단위 시간을 MM:SS 형식으로 변환합니다."""
    minutes = duration // 60
    seconds = duration % 60
    return f"{minutes}:{seconds:02d}"

st.title('YouTube Channel Video Downloader')

# 채널 URL 또는 username 입력
channel_input = st.text_input('YouTube 채널 URL 또는 username을 입력하세요:', 
                            help='예: https://www.youtube.com/@Seul_Ku 또는 @Seul_Ku')

if channel_input:
    try:
        with st.spinner('채널 정보를 가져오는 중...'):
            # URL 형식 확인 및 변환
            if not channel_input.startswith('http'):
                if not channel_input.startswith('@'):
                    channel_input = f"@{channel_input}"
                channel_input = f"https://www.youtube.com/{channel_input}"

            # 채널 정보 가져오기
            channel_info = get_channel_info(channel_input + "/videos")
            
            if not channel_info or 'entries' not in channel_info:
                st.error('채널 정보를 가져올 수 없습니다.')
                st.stop()
            
            # 채널명 표시
            st.success(f'채널명: {channel_info.get("uploader", "Unknown")}')
            
            # 다운로드 경로 설정
            download_path = st.text_input('다운로드 경로를 입력하세요:', value='downloads')
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            
            # 비디오 정보를 DataFrame으로 변환
            videos = []
            for entry in channel_info['entries']:
                if entry:
                    videos.append({
                        'title': entry.get('title', 'Unknown'),
                        'url': f"https://www.youtube.com/watch?v={entry['id']}",
                        'duration': format_duration(entry.get('duration', 0)),
                        'view_count': entry.get('view_count', 0),
                        'upload_date': entry.get('upload_date', 'Unknown')
                    })
            
            if videos:
                df = pd.DataFrame(videos)
                st.dataframe(df)
                
                # 다운로드 옵션
                st.subheader('다운로드 옵션')
                resolution = st.selectbox('해상도 선택:', 
                                       ['1080p', '720p', '480p', '360p'])
                
                # 다운로드 버튼
                if st.button('선택한 비디오 다운로드'):
                    for video in videos:
                        try:
                            ydl_opts = {
                                'format': f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]',
                                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                                'quiet': True,
                                'progress_hooks': [lambda d: 
                                    st.write(f"다운로드 중: {d['filename']} - {d.get('_percent_str', '0%')}")
                                    if d['status'] == 'downloading' else None],
                            }
                            
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                st.write(f'다운로드 시작: {video["title"]}')
                                ydl.download([video['url']])
                                st.success(f'다운로드 완료: {video["title"]}')
                                
                        except Exception as e:
                            st.error(f'다운로드 실패: {video["title"]} - {str(e)}')
            else:
                st.warning('비디오 정보를 가져올 수 없습니다.')
                    
    except Exception as e:
        st.error(f'에러가 발생했습니다: {str(e)}')
        st.info('올바른 채널 URL이나 username을 입력했는지 확인해주세요.')
