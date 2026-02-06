import streamlit as st
import yt_dlp
import os
import pandas as pd
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from keyword_analyzer import KeywordAnalyzer, KeywordDataExporter
import plotly.express as px
import plotly.graph_objects as go

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

st.set_page_config(page_title='YouTube Channel Manager', layout='wide')
st.title('🎬 YouTube Channel Manager - Video Downloader & Keyword Analysis')

# Create tabs
tab1, tab2, tab3 = st.tabs(['📥 Video Downloader', '🔍 Keyword Analysis', '📊 Trend Analysis'])

# Initialize keyword analyzer
analyzer = KeywordAnalyzer()
exporter = KeywordDataExporter()

with tab1:

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

# Tab 2: Keyword Analysis
with tab2:
    st.header('🔍 포털 키워드 분석')
    st.markdown('**Google, Naver, Daum의 키워드 검색량 분석 (Black Kiwi보다 향상된 분석)**')

    analysis_mode = st.radio('분석 모드 선택:',
                            ['단일 키워드 분석', '여러 키워드 비교', '채널 기반 키워드 추천'],
                            horizontal=True)

    if analysis_mode == '단일 키워드 분석':
        st.subheader('단일 키워드 분석')
        keyword = st.text_input('분석할 키워드를 입력하세요:', placeholder='예: 파이썬 튜토리얼')

        if keyword:
            with st.spinner('🔄 다중 포털 분석 중...'):
                analysis_result = analyzer.analyze_multi_portal(keyword)

            # 결과 표시
            col1, col2, col3, col4 = st.columns(4)

            portals = ['Google', 'Naver', 'Daum', 'YouTube']
            for idx, portal in enumerate(portals):
                portal_data = analysis_result['portals'].get(portal, {})
                with [col1, col2, col3, col4][idx]:
                    st.metric(
                        portal,
                        f"{portal_data.get('estimated_search_volume', 0):,}",
                        delta=portal_data.get('trend', 'N/A')
                    )

            st.divider()

            # 상세 분석
            for portal in portals:
                with st.expander(f'📊 {portal} 상세 분석'):
                    portal_data = analysis_result['portals'].get(portal, {})
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**검색량:** {portal_data.get('estimated_search_volume', 'N/A'):,}")
                        st.write(f"**트렌드:** {portal_data.get('trend', 'N/A')}")
                        if portal == 'Google':
                            st.write(f"**경쟁도:** {portal_data.get('competition_level', 'N/A')}")

                    with col2:
                        if 'related_keywords' in portal_data:
                            st.write("**관련 키워드:**")
                            for kw in portal_data.get('related_keywords', []):
                                st.write(f"  • {kw}")

            # 데이터 내보내기
            st.divider()
            st.subheader('📥 데이터 내보내기')
            col1, col2 = st.columns(2)

            with col1:
                if st.button('JSON으로 내보내기'):
                    result_msg = exporter.export_to_json(analysis_result, f'keyword_analysis_{keyword}.json')
                    st.info(result_msg)

            with col2:
                if st.button('CSV로 내보내기'):
                    df = pd.DataFrame([
                        {
                            'Keyword': keyword,
                            'Portal': portal,
                            'Search Volume': analysis_result['portals'].get(portal, {}).get('estimated_search_volume', 0),
                            'Trend': analysis_result['portals'].get(portal, {}).get('trend', 'N/A')
                        }
                        for portal in portals
                    ])
                    result_msg = exporter.export_to_csv(df, f'keyword_analysis_{keyword}.csv')
                    st.info(result_msg)

    elif analysis_mode == '여러 키워드 비교':
        st.subheader('여러 키워드 비교 분석')
        keywords_input = st.text_area('비교할 키워드들을 입력하세요 (한 줄에 하나씩):',
                                     placeholder='키워드1\n키워드2\n키워드3')

        if keywords_input:
            keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]

            if st.button('비교 분석 시작'):
                with st.spinner('🔄 비교 분석 중...'):
                    comparison_df = analyzer.compare_keywords(keywords)

                st.dataframe(comparison_df, use_container_width=True)

                # 시각화
                st.subheader('📈 비교 차트')

                # 포털별 검색량 비교
                fig = px.bar(
                    comparison_df,
                    x='Keyword',
                    y=['Google Volume', 'Naver Volume', 'Daum Volume', 'YouTube Volume'],
                    title='포털별 검색량 비교',
                    barmode='group'
                )
                st.plotly_chart(fig, use_container_width=True)

                # 평균 검색량 비교
                fig2 = px.bar(
                    comparison_df,
                    x='Keyword',
                    y='Average',
                    title='평균 검색량 비교',
                    color='Average'
                )
                st.plotly_chart(fig2, use_container_width=True)

                # 데이터 내보내기
                st.divider()
                if st.button('비교 결과를 CSV로 내보내기'):
                    result_msg = exporter.export_to_csv(comparison_df, 'keyword_comparison.csv')
                    st.info(result_msg)

    else:  # 채널 기반 키워드 추천
        st.subheader('채널 기반 키워드 추천')
        channel_name = st.text_input('채널명을 입력하세요:', placeholder='예: 파이썬 튜토리얼 채널')
        video_titles_input = st.text_area('비디오 제목들을 입력하세요 (한 줄에 하나씩):',
                                         placeholder='파이썬 기초\n파이썬 중급\n파이썬 고급')

        if channel_name and video_titles_input:
            video_titles = [title.strip() for title in video_titles_input.split('\n') if title.strip()]

            if st.button('추천 키워드 생성'):
                with st.spinner('🔄 추천 키워드 생성 중...'):
                    recommended_keywords = analyzer.get_keyword_recommendations(channel_name, video_titles)

                st.success('✅ 추천 키워드가 생성되었습니다!')

                # 추천 키워드 표시
                st.subheader('추천 키워드')
                cols = st.columns(3)
                for idx, keyword in enumerate(recommended_keywords):
                    with cols[idx % 3]:
                        st.write(f"🎯 `{keyword}`")

# Tab 3: Trend Analysis
with tab3:
    st.header('📊 트렌드 분석 (Advanced)')
    st.markdown('**Black Kiwi보다 향상된 30일 트렌드 분석**')

    keyword = st.text_input('트렌드를 분석할 키워드를 입력하세요:',
                           placeholder='예: 인공지능')
    days = st.slider('분석 기간 (일수):', min_value=7, max_value=90, value=30, step=7)

    if keyword:
        with st.spinner(f'🔄 {days}일간의 트렌드 분석 중...'):
            trend_analysis = analyzer.get_trend_analysis(keyword, days)

        # 요약 정보
        st.subheader('📈 트렌드 요약')
        summary = trend_analysis['summary']

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric('평균 검색량', f"{summary['average_volume']:.0f}")
        with col2:
            st.metric('피크 검색량', f"{summary['peak_volume']:.0f}")
        with col3:
            st.metric('최소 검색량', f"{summary['min_volume']:.0f}")
        with col4:
            st.metric('평균 관심도', f"{summary['average_interest']:.0f}")
        with col5:
            st.metric('변동성', f"{summary['volatility']:.0f}")

        # 트렌드 라인 차트
        st.subheader('📉 검색량 추이')
        trend_df = pd.DataFrame(trend_analysis['data'])

        fig = px.line(
            trend_df,
            x='date',
            y='search_volume',
            title=f'"{keyword}" 키워드 {days}일 검색량 추이',
            markers=True,
            labels={'date': '날짜', 'search_volume': '검색량'}
        )
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        # 관심도 추이
        st.subheader('💡 관심도 추이')
        fig2 = px.area(
            trend_df,
            x='date',
            y='interest_level',
            title=f'"{keyword}" 키워드 {days}일 관심도 추이',
            labels={'date': '날짜', 'interest_level': '관심도'}
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 트렌드 예측
        st.divider()
        st.subheader('🔮 트렌드 예측')
        prediction = trend_analysis['prediction']

        col1, col2, col3 = st.columns(3)
        with col1:
            trend_emoji = '📈' if prediction['predicted_trend'] == 'increasing' else ('📉' if prediction['predicted_trend'] == 'decreasing' else '➡️')
            st.metric('예측 트렌드', f"{trend_emoji} {prediction['predicted_trend']}")
        with col2:
            st.metric('성장률', f"{prediction['growth_rate']:.2f}%")
        with col3:
            st.metric('신뢰도', prediction['confidence'])

        # 상세 데이터 테이블
        st.subheader('📋 상세 데이터')
        st.dataframe(trend_df, use_container_width=True)

        # 데이터 내보내기
        st.divider()
        if st.button('트렌드 분석을 JSON으로 내보내기'):
            result_msg = exporter.export_to_json(trend_analysis, f'trend_analysis_{keyword}.json')
            st.info(result_msg)

        if st.button('트렌드 데이터를 CSV로 내보내기'):
            result_msg = exporter.export_to_csv(trend_df, f'trend_analysis_{keyword}.csv')
            st.info(result_msg)
