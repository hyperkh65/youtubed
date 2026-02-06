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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    '📥 Video Downloader',
    '🔍 Keyword Analysis',
    '📊 Trend Analysis',
    '🎯 Advanced Features',
    '📈 Performance & History',
    '⚙️ Settings'
])

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

# Tab 4: Advanced Features
with tab4:
    st.header('🎯 고급 분석 기능')

    advanced_mode = st.radio('분석 유형 선택:',
                            ['숏/롱테일 키워드', '실시간 추천', '경쟁사 분석', '검색 의도 분석'],
                            horizontal=True)

    if advanced_mode == '숏/롱테일 키워드':
        st.subheader('📊 숏/롱테일 키워드 분석')
        st.markdown('**숏 키워드(1-2단어)와 롱테일 키워드(3단어+) 상세 분석**')

        keyword = st.text_input('분석할 키워드:', placeholder='예: 파이썬 프로그래밍 튜토리얼')

        if keyword:
            with st.spinner('🔄 숏/롱테일 분석 중...'):
                analysis = analyzer.analyze_short_long_keywords(keyword)

            col1, col2 = st.columns(2)

            with col1:
                st.write('### 📌 숏테일 키워드 (높은 검색량)')
                if analysis['short_keywords']:
                    for kw in analysis['short_keywords']:
                        st.write(f"""
                        **{kw['keyword']}**
                        - 검색량: {kw['volume']:,}
                        - 난이도: {kw['difficulty']}/100
                        """)

            with col2:
                st.write('### 🎯 롱테일 키워드 (낮은 경쟁도)')
                if analysis['long_keywords']:
                    for kw in analysis['long_keywords']:
                        st.write(f"""
                        **{kw['keyword']}**
                        - 검색량: {kw['volume']:,}
                        - 난이도: {kw['difficulty']}/100
                        - 전환 가능성: {kw['conversion_potential']:.1%}
                        """)

            # 비교 분석 시각화
            st.divider()
            st.subheader('📈 숏/롱테일 비교 분석')

            comparison = analysis['comparison']

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric('숏테일 평균 검색량', f"{comparison['short_tail_avg_volume']:.0f}")
            with col2:
                st.metric('롱테일 평균 검색량', f"{comparison['long_tail_avg_volume']:.0f}")
            with col3:
                st.metric('숏테일 난이도', f"{comparison['short_tail_avg_difficulty']:.0f}")
            with col4:
                st.metric('롱테일 난이도', f"{comparison['long_tail_avg_difficulty']:.0f}")

            st.info(f"💡 **추천:** {comparison['recommendation']}")

    elif advanced_mode == '실시간 추천':
        st.subheader('💡 실시간 키워드 추천')
        st.markdown('**다양한 알고리즘을 통한 최적의 키워드 추천**')

        col1, col2 = st.columns(2)
        with col1:
            keywords_input = st.text_area('기본 키워드들 (한 줄에 하나):',
                                         placeholder='파이썬\n머신러닝\n데이터과학',
                                         height=100)
        with col2:
            channel_topic = st.text_input('채널 주제 (선택사항):', placeholder='예: 기술/프로그래밍')

        if keywords_input and st.button('실시간 추천 생성'):
            keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]

            with st.spinner('🔄 최적의 키워드 추천 중...'):
                recommendations = analyzer.get_realtime_recommendations(keywords, channel_topic)

            st.success('✅ 추천 키워드가 생성되었습니다!')

            # 추천 결과 표시
            rec_df = pd.DataFrame([
                {
                    'Keyword': r['keyword'],
                    'Score': f"{r['score']:.1f}",
                    'Type': r.get('type', 'N/A'),
                    'Volume': f"{r.get('volume', 0):,}",
                    'Difficulty': r.get('difficulty', 0),
                    'Trend': r.get('trend', 'N/A')
                }
                for r in recommendations
            ])

            st.dataframe(rec_df, use_container_width=True)

            # 점수별 시각화
            fig = px.bar(
                pd.DataFrame(recommendations).sort_values('score'),
                x='keyword',
                y='score',
                title='키워드 추천 점수',
                color='score'
            )
            st.plotly_chart(fig, use_container_width=True)

    elif advanced_mode == '경쟁사 분석':
        st.subheader('⚔️ 경쟁사 키워드 분석')
        st.markdown('**경쟁사의 키워드 전략을 분석하고 기회 발굴**')

        col1, col2 = st.columns(2)

        with col1:
            competitor_input = st.text_area('경쟁사 키워드들:',
                                           placeholder='경쟁사1\n경쟁사2\n경쟁사3',
                                           height=120)

        with col2:
            your_input = st.text_area('우리의 키워드들:',
                                     placeholder='우리1\n우리2\n우리3',
                                     height=120)

        if competitor_input and your_input and st.button('경쟁사 분석 시작'):
            competitor_kws = [kw.strip() for kw in competitor_input.split('\n') if kw.strip()]
            your_kws = [kw.strip() for kw in your_input.split('\n') if kw.strip()]

            with st.spinner('🔄 경쟁 분석 중...'):
                comp_analysis = analyzer.analyze_competitor_keywords(competitor_kws, your_kws)

            # 결과 표시
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric('공통 키워드', len(comp_analysis['overlap_keywords']))
            with col2:
                st.metric('경쟁사 독점', len(comp_analysis['competitor_unique']))
            with col3:
                st.metric('우리 독점', len(comp_analysis['your_unique']))

            st.divider()

            # 발견된 기회
            st.subheader('🎯 발견된 기회 키워드')

            if comp_analysis['opportunities']:
                opp_df = pd.DataFrame([
                    {
                        'Keyword': opp['keyword'],
                        'Opportunity Score': f"{opp['opportunity_score']:.1f}",
                        'Search Volume': f"{opp['volume']:,}",
                        'Difficulty': f"{opp['difficulty']}/100"
                    }
                    for opp in comp_analysis['opportunities'][:10]
                ])

                st.dataframe(opp_df, use_container_width=True)

                # 기회 시각화
                fig = px.scatter(
                    pd.DataFrame(comp_analysis['opportunities'][:10]),
                    x='difficulty',
                    y='volume',
                    size='opportunity_score',
                    hover_data=['keyword'],
                    title='기회 키워드 매트릭스 (X: 난이도, Y: 검색량)',
                    labels={'difficulty': '난이도', 'volume': '검색량'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning('발견된 기회가 없습니다.')

    else:  # 검색 의도 분석
        st.subheader('🔍 검색 의도 분석')
        st.markdown('**Informational, Navigational, Commercial, Transactional**')

        keyword = st.text_input('키워드 입력:', placeholder='예: 최고의 노트북 가격 비교')

        if keyword:
            with st.spinner('🔄 검색 의도 분석 중...'):
                intent_analysis = analyzer.analyze_search_intent(keyword)

            intent_emoji = {
                'informational': '📚',
                'navigational': '🧭',
                'commercial': '🛍️',
                'transactional': '💳'
            }

            intent_names = {
                'informational': '정보 검색 (정보 얻기)',
                'navigational': '네비게이션 (사이트 찾기)',
                'commercial': '상업 (비교/리뷰)',
                'transactional': '거래 (구매)'
            }

            col1, col2 = st.columns(2)

            with col1:
                st.write('### 🎯 주요 검색 의도')
                primary = intent_analysis['primary_intent']
                st.success(f"{intent_emoji.get(primary, '')} {intent_names.get(primary, 'Unknown')}")
                st.write(f"신뢰도: {intent_analysis['confidence']:.1%}")

            with col2:
                st.write('### 📊 의도별 점수')
                scores = intent_analysis['intent_scores']

                fig = px.bar(
                    x=list(scores.keys()),
                    y=list(scores.values()),
                    title='검색 의도 분포',
                    labels={'x': '의도 유형', 'y': '점수'}
                )
                st.plotly_chart(fig, use_container_width=True)

# Tab 5: Performance & History
with tab5:
    st.header('📈 성능 예측 & 히스토리')

    perf_mode = st.radio('분석 선택:',
                        ['성능 예측', '계절성 감지', '키워드 히스토리'],
                        horizontal=True)

    if perf_mode == '성능 예측':
        st.subheader('🔮 향후 3개월 키워드 성능 예측')

        keyword = st.text_input('예측할 키워드:', placeholder='예: 인공지능 기초')

        if keyword:
            with st.spinner('🔄 성능 예측 중...'):
                prediction = analyzer.predict_keyword_performance(keyword, months=3)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric('현재 검색량', f"{prediction['current_volume']:.0f}")
            with col2:
                trend_emoji = '📈' if prediction['predicted_trend'] == 'increasing' else '📉'
                st.metric('예측 트렌드', f"{trend_emoji} {prediction['predicted_trend']}")
            with col3:
                st.metric('예측 신뢰도', f"{prediction['confidence']:.1f}%")

            # 예측 그래프
            st.subheader('📊 3개월 검색량 예측')

            pred_df = pd.DataFrame({
                'Date': prediction['prediction_dates'],
                'Predicted Volume': prediction['predicted_volumes']
            })

            fig = px.line(
                pred_df,
                x='Date',
                y='Predicted Volume',
                title=f'"{keyword}" 예상 검색량 변화',
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

    elif perf_mode == '계절성 감지':
        st.subheader('📅 계절성 패턴 분석')

        keyword = st.text_input('계절성을 분석할 키워드:', placeholder='예: 크리스마스')

        if keyword:
            with st.spinner('🔄 계절성 분석 중...'):
                seasonality = analyzer.detect_seasonality(keyword, days=365)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric('계절성 강도', f"{seasonality['seasonality_strength']:.2f}")
            with col2:
                st.write('**피크 월:**')
                for month in seasonality['peak_months']:
                    st.write(f"  • {month}")
            with col3:
                st.write('**저점 월:**')
                for month in seasonality['low_months']:
                    st.write(f"  • {month}")

            # 월별 패턴
            st.subheader('📈 월별 검색량 패턴')

            monthly_df = pd.DataFrame({
                'Month': list(seasonality['monthly_pattern'].keys()),
                'Search Volume': list(seasonality['monthly_pattern'].values())
            })

            fig = px.bar(
                monthly_df,
                x='Month',
                y='Search Volume',
                title='월별 평균 검색량',
                color='Search Volume'
            )
            st.plotly_chart(fig, use_container_width=True)

            # 포스팅 일정 추천
            st.divider()
            st.subheader('📅 최적 포스팅 일정')

            recommendation = seasonality['recommendation']

            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**최고의 달:** {recommendation['best_month']}")
                st.info(f"**최고의 요일:** {recommendation['best_day']}")
            with col2:
                st.warning(f"**피해야 할 달:** {', '.join(recommendation['avoid_months'])}")
                st.info(f"**추천 주기:** {recommendation['posting_frequency']}")

    else:  # 키워드 히스토리
        st.subheader('📜 키워드 분석 히스토리')

        col1, col2 = st.columns(2)

        with col1:
            keyword = st.text_input('검색 키워드:', placeholder='예: 파이썬')
            days = st.slider('조회 기간 (일):', 1, 90, 30)

        with col2:
            st.write('**유명 키워드 Top 10**')
            try:
                top_keywords = analyzer.db.get_top_keywords(10)
                if not top_keywords.empty:
                    for idx, row in top_keywords.iterrows():
                        st.write(f"{idx+1}. {row['keyword']} ({int(row['count'])}회)")
                else:
                    st.info('히스토리가 없습니다.')
            except:
                st.info('히스토리 데이터가 없습니다.')

        if keyword:
            try:
                history = analyzer.db.get_analysis_history(keyword, days)

                if not history.empty:
                    st.dataframe(history, use_container_width=True)

                    # 시간대별 추이
                    history_df = history.copy()
                    history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
                    history_df = history_df.sort_values('timestamp')

                    fig = px.line(
                        history_df,
                        x='timestamp',
                        y='search_volume',
                        color='portal',
                        title=f'"{keyword}" 히스토리'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info('분석 히스토리가 없습니다.')
            except Exception as e:
                st.warning(f'히스토리 조회 실패: {str(e)}')

# Tab 6: Settings
with tab6:
    st.header('⚙️ 설정 & 도구')

    settings_mode = st.radio('설정 선택:',
                            ['데이터 내보내기', '분석 리포트', '데이터베이스 정보'],
                            horizontal=True)

    if settings_mode == '데이터 내보내기':
        st.subheader('📥 키워드 분석 데이터 내보내기')

        keyword = st.text_input('내보낼 키워드:', placeholder='예: 파이썬 튜토리얼')

        if keyword:
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button('JSON 형식'):
                    analysis = analyzer.analyze_multi_portal(keyword)
                    msg = exporter.export_to_json(analysis, f'{keyword}_analysis.json')
                    st.success(msg)

            with col2:
                if st.button('CSV 형식'):
                    df = pd.DataFrame([
                        {
                            'Keyword': keyword,
                            'Analysis Date': datetime.now().isoformat()
                        }
                    ])
                    msg = exporter.export_to_csv(df, f'{keyword}_analysis.csv')
                    st.success(msg)

            with col3:
                if st.button('보고서 생성'):
                    analysis = analyzer.analyze_multi_portal(keyword)
                    msg = exporter.generate_report(analysis, f'{keyword}_report.json')
                    st.success(msg)

    elif settings_mode == '분석 리포트':
        st.subheader('📊 종합 분석 리포트 생성')

        keywords_input = st.text_area('분석할 키워드들 (한 줄에 하나):',
                                     placeholder='키워드1\n키워드2\n키워드3',
                                     height=100)

        if st.button('리포트 생성'):
            if keywords_input:
                keywords = [kw.strip() for kw in keywords_input.split('\n') if kw.strip()]

                with st.spinner('🔄 리포트 생성 중...'):
                    all_analysis = {}

                    for kw in keywords:
                        all_analysis[kw] = {
                            'multi_portal': analyzer.analyze_multi_portal(kw),
                            'short_long': analyzer.analyze_short_long_keywords(kw),
                            'intent': analyzer.analyze_search_intent(kw)
                        }

                    msg = exporter.generate_report(all_analysis, 'comprehensive_report.json')
                    st.success(msg)
                    st.info(f'✅ {len(keywords)}개 키워드에 대한 종합 리포트가 생성되었습니다.')
            else:
                st.warning('키워드를 입력해주세요.')

    else:  # 데이터베이스 정보
        st.subheader('💾 데이터베이스 정보')

        col1, col2 = st.columns(2)

        with col1:
            st.write('**데이터베이스 위치:**')
            st.code(analyzer.db.db_path, language='text')

            if st.button('🗑️ 데이터베이스 초기화'):
                try:
                    if os.path.exists(analyzer.db.db_path):
                        os.remove(analyzer.db.db_path)
                        st.success('✅ 데이터베이스가 초기화되었습니다.')
                    else:
                        st.info('데이터베이스가 없습니다.')
                except Exception as e:
                    st.error(f'초기화 실패: {str(e)}')

        with col2:
            st.write('**시스템 정보:**')
            st.write(f"- 분석 모듈: Advanced Keyword Analyzer v2.0")
            st.write(f"- 지원 포털: Google, Naver, Daum, YouTube")
            st.write(f"- 데이터 저장소: SQLite")
            st.write(f"- 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
