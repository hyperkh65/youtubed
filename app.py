import streamlit as st
import yt_dlp
import os
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_channel_id(channel_url):
    """채널 URL에서 채널 ID를 추출하거나 조회합니다."""
    try:
        response = requests.get(channel_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 채널 ID가 포함된 메타 태그 찾기
            meta_tags = soup.find_all('meta', {'property': 'og:url'})
            for tag in meta_tags:
                content = tag.get('content', '')
                if 'channel/' in content:
                    return content.split('channel/')[-1]
    except Exception as e:
        st.error(f"채널 ID 조회 실패: {str(e)}")
    return None

def get_channel_info(channel_url):
    """채널 정보와 비디오 목록을 가져옵니다."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'no_warnings': True,
        'ignoreerrors': True
    }
    
    try:
        # 먼저 채널 ID 가져오기
        channel_id = get_channel_id(channel_url)
        if channel_id:
            channel_url = f"https://www.youtube.com/channel/{channel_id}/videos"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            if result and 'entries' in result:
                return result
            else:
                # 채널 URL로 시도
                result = ydl.extract_info(channel_url.replace("/videos", ""), download=False)
                return result
    except Exception as e:
        st.error(f"채널 정보 가져오기 실패: {str(e)}")
        return None

def format_duration(duration):
    """초 단위 시간을 MM:SS 형식으로 변환합니다."""
    if not duration:
        return "00:00"
    minutes = int(duration) // 60
    seconds = int(duration) % 60
    return f"{minutes}:{seconds:02d}"

def format_date(date_str):
    """YYYYMMDD 형식의 날짜를 YYYY-MM-DD 형식으로 변환합니다."""
    if not date_str or len(date_str) != 8:
        return "Unknown"
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

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
            channel_info = get_channel_info(channel_input)
            
            if not channel_info or 'entries' not in channel_info:
                st.error('채널 정보를 가져올 수 없습니다. 다른 URL 형식을 시도해보세요.')
                st.info('시도해볼 수 있는 URL 형식:\n1. https://www.youtube.com/@username\n2. https://www.youtube.com/c/channelname\n3. https://www.youtube.com/channel/channel_id')
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
                        'upload_date': format_date(entry.get('upload_date', 'Unknown'))
                    })
            
            if videos:
                df = pd.DataFrame(videos)
                st.dataframe(df)
                
                # 다운로드 옵션
                st.subheader('다운로드 옵션')
                col1, col2 = st.columns(2)
                with col1:
                    resolution = st.selectbox('해상도 선택:', 
                                           ['1080p', '720p', '480p', '360p'])
                with col2:
                    format_option = st.selectbox('포맷 선택:',
                                               ['mp4', 'mkv'])
                
                # 진행 상황 표시를 위한 상태 표시줄
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 다운로드 버튼
                if st.button('선택한 비디오 다운로드'):
                    total_videos = len(videos)
                    for i, video in enumerate(videos):
                        try:
                            ydl_opts = {
                                'format': f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]',
                                'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
                                'merge_output_format': format_option,
                                'quiet': True,
                            }
                            
                            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                status_text.text(f'다운로드 중: {video["title"]}')
                                ydl.download([video['url']])
                                progress = (i + 1) / total_videos
                                progress_bar.progress(progress)
                                st.success(f'다운로드 완료: {video["title"]}')
                                
                        except Exception as e:
                            st.error(f'다운로드 실패: {video["title"]} - {str(e)}')
                    
                    status_text.text('모든 다운로드가 완료되었습니다!')
            else:
                st.warning('비디오 정보를 가져올 수 없습니다.')
                    
    except Exception as e:
        st.error(f'에러가 발생했습니다: {str(e)}')
        st.info('올바른 채널 URL이나 username을 입력했는지 확인해주세요.')
