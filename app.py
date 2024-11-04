import streamlit as st
from pytube import Channel, YouTube
import os
import pandas as pd
from datetime import datetime
import requests
import re
from bs4 import BeautifulSoup

def get_channel_videos(channel_url):
    """채널의 모든 비디오 URL을 가져옵니다."""
    try:
        html = requests.get(channel_url + "/videos").text
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        return [f"https://www.youtube.com/watch?v={vid}" for vid in dict.fromkeys(video_ids)]
    except Exception as e:
        st.error(f"비디오 URL 가져오기 실패: {str(e)}")
        return []

def get_video_info(url):
    """비디오 URL로부터 정보를 가져옵니다."""
    try:
        yt = YouTube(url)
        return {
            'title': yt.title,
            'url': url,
            'views': yt.views,
            'author': yt.author,
            'publish_date': yt.publish_date.strftime('%Y-%m-%d') if yt.publish_date else 'Unknown',
            'length': f'{yt.length//60}:{yt.length%60:02d}'
        }
    except Exception as e:
        st.warning(f"비디오 정보 가져오기 실패: {str(e)}")
        return None

st.title('YouTube Channel Video Downloader')

# 채널 URL 또는 username 입력
channel_input = st.text_input('YouTube 채널 URL 또는 username을 입력하세요:', 
                            help='예: https://www.youtube.com/@Seul_Ku 또는 Seul_Ku')

if channel_input:
    try:
        with st.spinner('채널 정보를 가져오는 중...'):
            # URL 형식 확인 및 변환
            if not channel_input.startswith('http'):
                if channel_input.startswith('@'):
                    channel_input = f"https://www.youtube.com/{channel_input}"
                else:
                    channel_input = f"https://www.youtube.com/@{channel_input}"

            # 비디오 URL 목록 가져오기
            video_urls = get_channel_videos(channel_input)
            
            if not video_urls:
                st.error('채널에서 비디오를 찾을 수 없습니다.')
                st.stop()
            
            # 다운로드 경로 설정
            download_path = st.text_input('다운로드 경로를 입력하세요:', value='downloads')
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            
            # 비디오 정보 수집
            videos = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_videos = len(video_urls)
            
            for i, url in enumerate(video_urls):
                video_info = get_video_info(url)
                if video_info:
                    videos.append(video_info)
                    if not videos[-1].get('author', ''):
                        videos[-1]['author'] = video_info.get('author', 'Unknown')
                progress = (i + 1) / total_videos
                progress_bar.progress(progress)
                status_text.text(f'비디오 정보 수집 중... {i+1}/{total_videos}개 완료')
            
            if videos:
                # 채널명 표시
                st.success(f'채널명: {videos[0]["author"]}')
                
                # 비디오 목록을 DataFrame으로 변환하고 표시
                df = pd.DataFrame(videos)
                st.dataframe(df)
                
                # 다운로드 옵션
                st.subheader('다운로드 옵션')
                resolution = st.selectbox('해상도 선택:', 
                                       ['최고 화질', '720p', '480p', '360p'])
                
                # 다운로드 버튼
                if st.button('선택한 비디오 다운로드'):
                    for url in df['url']:
                        try:
                            yt = YouTube(url)
                            # 선택된 해상도에 따라 스트림 선택
                            if resolution == '최고 화질':
                                video_stream = yt.streams.get_highest_resolution()
                            else:
                                video_stream = yt.streams.filter(
                                    progressive=True, 
                                    resolution=resolution
                                ).first()
                                
                            if not video_stream:
                                st.warning(f'{yt.title}: 선택한 해상도를 찾을 수 없습니다. 대신 가능한 최고 화질로 다운로드합니다.')
                                video_stream = yt.streams.get_highest_resolution()
                            
                            st.write(f'다운로드 중: {yt.title}')
                            video_stream.download(output_path=download_path)
                            st.success(f'다운로드 완료: {yt.title}')
                        except Exception as e:
                            st.error(f'다운로드 실패: {yt.title} - {str(e)}')
            else:
                st.warning('비디오 정보를 가져올 수 없습니다.')
                    
    except Exception as e:
        st.error(f'에러가 발생했습니다: {str(e)}')
        st.info('올바른 채널 URL이나 username을 입력했는지 확인해주세요.')
