import streamlit as st
from pytube import Channel, YouTube
import os
import pandas as pd
from datetime import datetime

def get_video_info(video):
    try:
        return {
            'title': video.title,
            'url': video.watch_url,
            'views': video.views,
            'publish_date': video.publish_date.strftime('%Y-%m-%d') if video.publish_date else 'Unknown',
            'length': f'{video.length//60}:{video.length%60:02d}'
        }
    except Exception as e:
        st.warning(f"비디오 정보 가져오기 실패: {str(e)}")
        return None

st.title('YouTube Channel Video Downloader')

# 채널 URL 입력
channel_url = st.text_input('YouTube 채널 URL을 입력하세요:')

if channel_url:
    try:
        with st.spinner('채널 정보를 가져오는 중...'):
            # 채널 정보 가져오기
            channel = Channel(channel_url)
            
            # 첫 번째 비디오의 채널명으로 대체
            first_video = next(channel.videos)
            channel_name = first_video.author
            st.success(f'채널명: {channel_name}')
            
            # 다운로드 경로 설정
            download_path = st.text_input('다운로드 경로를 입력하세요:', value='downloads')
            if not os.path.exists(download_path):
                os.makedirs(download_path)
            
            # 비디오 정보 수집
            videos = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # channel.videos 반복자 재생성 (첫 번째 비디오를 이미 소비했으므로)
            channel = Channel(channel_url)
            video_list = list(channel.videos)
            total_videos = len(video_list)
            
            for i, video in enumerate(video_list):
                video_info = get_video_info(video)
                if video_info:
                    videos.append(video_info)
                progress = (i + 1) / total_videos
                progress_bar.progress(progress)
                status_text.text(f'비디오 정보 수집 중... {i+1}/{total_videos}개 완료')
            
            if videos:
                # 비디오 목록 표시
                df = pd.DataFrame(videos)
                st.dataframe(df)
                
                # 다운로드 버튼
                if st.button('선택한 비디오 다운로드'):
                    for url in df['url']:
                        try:
                            yt = YouTube(url)
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
        st.info('올바른 채널 URL을 입력했는지 확인해주세요. URL 형식: https://www.youtube.com/c/채널명 또는 https://www.youtube.com/@채널명')
