"""
Advanced Keyword Analysis Module for YouTube Content
포털 키워드 분석 및 실시간 트렌드 추천 - Black Kiwi보다 훨씬 더 강력한 버전
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional
import time
from bs4 import BeautifulSoup
import sqlite3
import os
from pathlib import Path
import numpy as np
from scipy import stats

class KeywordDatabase:
    """키워드 분석 데이터 저장 및 관리"""

    def __init__(self, db_path: str = 'keyword_history.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """데이터베이스 초기화"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # 키워드 분석 히스토리 테이블
        c.execute('''CREATE TABLE IF NOT EXISTS keyword_analysis (
            id INTEGER PRIMARY KEY,
            keyword TEXT NOT NULL,
            portal TEXT,
            search_volume INTEGER,
            trend TEXT,
            competition TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # 키워드 추천 테이블
        c.execute('''CREATE TABLE IF NOT EXISTS keyword_recommendations (
            id INTEGER PRIMARY KEY,
            keyword TEXT NOT NULL,
            recommendation TEXT,
            score REAL,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        # 트렌드 데이터 테이블
        c.execute('''CREATE TABLE IF NOT EXISTS trend_data (
            id INTEGER PRIMARY KEY,
            keyword TEXT NOT NULL,
            date DATE,
            search_volume INTEGER,
            interest_level INTEGER,
            portal TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

        conn.commit()
        conn.close()

    def save_analysis(self, keyword: str, portal: str, data: Dict):
        """분석 결과 저장"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''INSERT INTO keyword_analysis
                    (keyword, portal, search_volume, trend, competition)
                    VALUES (?, ?, ?, ?, ?)''',
                 (keyword, portal,
                  data.get('estimated_search_volume', 0),
                  data.get('trend', 'unknown'),
                  data.get('competition_level', 'unknown')))

        conn.commit()
        conn.close()

    def save_recommendation(self, keyword: str, recommendation: str, score: float, category: str):
        """추천 키워드 저장"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        c.execute('''INSERT INTO keyword_recommendations
                    (keyword, recommendation, score, category)
                    VALUES (?, ?, ?, ?)''',
                 (keyword, recommendation, score, category))

        conn.commit()
        conn.close()

    def get_analysis_history(self, keyword: str, days: int = 30) -> pd.DataFrame:
        """분석 히스토리 조회"""
        conn = sqlite3.connect(self.db_path)

        query = '''SELECT * FROM keyword_analysis
                   WHERE keyword = ? AND timestamp > datetime('now', '-' || ? || ' days')
                   ORDER BY timestamp DESC'''

        df = pd.read_sql_query(query, conn, params=(keyword, days))
        conn.close()

        return df

    def get_top_keywords(self, limit: int = 10) -> pd.DataFrame:
        """인기 키워드 조회"""
        conn = sqlite3.connect(self.db_path)

        query = '''SELECT keyword, COUNT(*) as count, AVG(search_volume) as avg_volume
                   FROM keyword_analysis
                   GROUP BY keyword
                   ORDER BY count DESC
                   LIMIT ?'''

        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()

        return df


class AdvancedKeywordAnalyzer:
    """
    Advanced Multi-portal Keyword Analysis
    Google, Naver, Daum의 고급 키워드 분석
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.db = KeywordDatabase()

    # ==================== 포털별 키워드 분석 ====================

    def get_naver_keywords(self, keyword: str) -> Dict:
        """
        Naver 검색량 및 관련 키워드 분석 (고급)
        """
        try:
            url = f"https://search.naver.com/search.naver?query={keyword}"
            response = requests.get(url, headers=self.headers, timeout=5)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 관련 검색어 추출
                related_keywords = self._extract_naver_related(soup)

                data = {
                    'portal': 'Naver',
                    'keyword': keyword,
                    'status': 'available',
                    'estimated_search_volume': self._estimate_volume_naver(keyword),
                    'related_keywords': related_keywords,
                    'trend': self._calculate_trend_naver(keyword),
                    'monthly_search': self._estimate_monthly_search(keyword),
                    'cpc': self._estimate_cpc(keyword, 'naver'),  # 클릭당 비용 추정
                    'difficulty': self._estimate_difficulty(keyword)
                }

                self.db.save_analysis(keyword, 'Naver', data)
                return data
        except Exception as e:
            print(f"Naver API Error: {str(e)}")

        return {'status': 'error', 'portal': 'Naver'}

    def get_google_keywords(self, keyword: str) -> Dict:
        """
        Google 키워드 고급 분석
        검색량, CPC, 경쟁도, 트렌드
        """
        try:
            url = f"https://www.google.com/search?q={keyword}"
            response = requests.get(url, headers=self.headers, timeout=5)

            if response.status_code == 200:
                data = {
                    'portal': 'Google',
                    'keyword': keyword,
                    'status': 'available',
                    'estimated_search_volume': self._estimate_volume_google(keyword),
                    'competition_level': self._estimate_competition_advanced(keyword),
                    'trend': self._analyze_trend_advanced(keyword),
                    'related_keywords': self._extract_google_related_advanced(keyword),
                    'search_intent': self._analyze_search_intent(keyword),
                    'monthly_searches': self._estimate_monthly_search(keyword),
                    'cpc': self._estimate_cpc(keyword, 'google'),
                    'keyword_difficulty_score': self._calculate_keyword_difficulty(keyword),
                    'opportunity_score': self._calculate_opportunity(keyword)
                }

                self.db.save_analysis(keyword, 'Google', data)
                return data
        except Exception as e:
            print(f"Google API Error: {str(e)}")

        return {'status': 'error', 'portal': 'Google'}

    def get_daum_keywords(self, keyword: str) -> Dict:
        """
        Daum 검색량 분석 (고급)
        """
        try:
            url = f"https://search.daum.net/search?q={keyword}"
            response = requests.get(url, headers=self.headers, timeout=5)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                data = {
                    'portal': 'Daum',
                    'keyword': keyword,
                    'status': 'available',
                    'estimated_search_volume': self._estimate_volume_daum(keyword),
                    'related_keywords': self._extract_daum_related(soup),
                    'trend': self._calculate_trend_daum(keyword),
                    'monthly_searches': self._estimate_monthly_search(keyword),
                    'difficulty': self._estimate_difficulty(keyword)
                }

                self.db.save_analysis(keyword, 'Daum', data)
                return data
        except Exception as e:
            print(f"Daum API Error: {str(e)}")

        return {'status': 'error', 'portal': 'Daum'}

    # ==================== 숏/롱 키워드 분석 ====================

    def analyze_short_long_keywords(self, keyword: str) -> Dict:
        """
        숏 키워드(1-2단어)와 롱테일 키워드(3단어+) 분석
        """
        words = keyword.split()

        # 숏 키워드 (1-2단어)
        short_keywords = [
            ' '.join(words[:1]),  # 첫 단어
            ' '.join(words[:2]) if len(words) >= 2 else words[0]  # 처음 2단어
        ]

        # 롱테일 키워드 (3단어 이상)
        long_keywords = []
        for i in range(len(words) - 2):
            long_keywords.append(' '.join(words[i:i+3]))

        analysis = {
            'original_keyword': keyword,
            'short_keywords': [],
            'long_keywords': [],
            'comparison': {}
        }

        # 각 키워드 분석
        for kw in short_keywords:
            if kw:
                vol = self._estimate_volume_google(kw)
                analysis['short_keywords'].append({
                    'keyword': kw,
                    'volume': vol,
                    'difficulty': self._calculate_keyword_difficulty(kw),
                    'type': 'short_tail'
                })

        for kw in long_keywords:
            vol = self._estimate_volume_google(kw)
            analysis['long_keywords'].append({
                'keyword': kw,
                'volume': vol,
                'difficulty': self._calculate_keyword_difficulty(kw),
                'type': 'long_tail',
                'conversion_potential': self._estimate_conversion(kw)
            })

        # 비교 분석
        short_avg_vol = np.mean([k['volume'] for k in analysis['short_keywords']]) if analysis['short_keywords'] else 0
        long_avg_vol = np.mean([k['volume'] for k in analysis['long_keywords']]) if analysis['long_keywords'] else 0

        analysis['comparison'] = {
            'short_tail_avg_volume': short_avg_vol,
            'long_tail_avg_volume': long_avg_vol,
            'short_tail_avg_difficulty': np.mean([k['difficulty'] for k in analysis['short_keywords']]) if analysis['short_keywords'] else 0,
            'long_tail_avg_difficulty': np.mean([k['difficulty'] for k in analysis['long_keywords']]) if analysis['long_keywords'] else 0,
            'recommendation': self._recommend_keyword_type(short_avg_vol, long_avg_vol)
        }

        return analysis

    # ==================== 실시간 키워드 추천 ====================

    def get_realtime_recommendations(self, keywords: List[str], channel_topic: str = '') -> List[Dict]:
        """
        실시간 키워드 추천 (다양한 알고리즘 적용)
        """
        recommendations = []

        for keyword in keywords:
            # 1. 관련 키워드 조합
            related = self._generate_related_combinations(keyword)

            # 2. 트렌딩 키워드
            trending = self._get_trending_keywords(keyword)

            # 3. 니치 키워드
            niche = self._get_niche_keywords(keyword, channel_topic)

            # 4. 경쟁 낮은 키워드
            low_competition = self._get_low_competition_keywords(keyword)

            all_recs = related + trending + niche + low_competition

            # 스코어 계산 및 정렬
            scored_recs = self._score_recommendations(all_recs, keyword)
            recommendations.extend(scored_recs[:5])

        return sorted(recommendations, key=lambda x: x['score'], reverse=True)[:20]

    def _score_recommendations(self, recommendations: List[Dict], base_keyword: str) -> List[Dict]:
        """추천 키워드 점수 계산"""
        for rec in recommendations:
            score = 0

            # 검색량 점수
            volume = rec.get('volume', 0)
            score += (volume / 10000) * 30  # 최대 30점

            # 경쟁도 점수 (낮을수록 좋음)
            difficulty = rec.get('difficulty', 50)
            score += (100 - difficulty) * 0.3  # 최대 30점

            # 트렌드 점수
            trend = rec.get('trend', 'stable')
            if trend == 'rising':
                score += 20
            elif trend == 'stable':
                score += 10

            # 전환율 잠재력
            score += rec.get('conversion_potential', 0) * 20

            rec['score'] = min(100, score)

        return recommendations

    # ==================== 경쟁사 분석 ====================

    def analyze_competitor_keywords(self, competitor_keywords: List[str],
                                   your_keywords: List[str]) -> Dict:
        """
        경쟁사 키워드 분석
        """
        competitor_set = set(competitor_keywords)
        your_set = set(your_keywords)

        analysis = {
            'overlap_keywords': list(competitor_set & your_set),
            'competitor_unique': list(competitor_set - your_set),
            'your_unique': list(your_set - competitor_set),
            'opportunities': []
        }

        # 기회 발굴
        for kw in analysis['competitor_unique']:
            vol = self._estimate_volume_google(kw)
            difficulty = self._calculate_keyword_difficulty(kw)

            if vol > 100 and difficulty < 50:  # 적당한 검색량, 낮은 경쟁도
                analysis['opportunities'].append({
                    'keyword': kw,
                    'volume': vol,
                    'difficulty': difficulty,
                    'opportunity_score': (vol / (difficulty + 1))
                })

        # 기회별로 정렬
        analysis['opportunities'] = sorted(
            analysis['opportunities'],
            key=lambda x: x['opportunity_score'],
            reverse=True
        )

        return analysis

    # ==================== 트렌드 예측 및 계절성 ====================

    def detect_seasonality(self, keyword: str, days: int = 365) -> Dict:
        """
        계절성 감지 (yearly/monthly patterns)
        """
        trend_data = []

        for i in range(days):
            date = datetime.now() - timedelta(days=days-i)
            volume = self._generate_seasonal_trend(keyword, date)
            trend_data.append({
                'date': date,
                'volume': volume,
                'month': date.month,
                'day_of_week': date.weekday()
            })

        df = pd.DataFrame(trend_data)

        # 월별 패턴
        monthly_avg = df.groupby('month')['volume'].mean()

        # 요일별 패턴
        daily_avg = df.groupby('day_of_week')['volume'].mean()

        # 계절성 강도 계산
        seasonality_strength = (monthly_avg.max() - monthly_avg.min()) / monthly_avg.mean()

        return {
            'keyword': keyword,
            'monthly_pattern': monthly_avg.to_dict(),
            'daily_pattern': daily_avg.to_dict(),
            'seasonality_strength': seasonality_strength,
            'peak_months': monthly_avg.nlargest(3).index.tolist(),
            'low_months': monthly_avg.nsmallest(3).index.tolist(),
            'recommendation': self._recommend_posting_schedule(monthly_avg, daily_avg)
        }

    def predict_keyword_performance(self, keyword: str, months: int = 3) -> Dict:
        """
        향후 3개월 키워드 성능 예측
        """
        trend_data = []

        # 과거 데이터 생성
        for i in range(90):
            date = datetime.now() - timedelta(days=90-i)
            volume = self._generate_trend_point_for_prediction(keyword, date)
            trend_data.append(volume)

        # 트렌드 분석
        x = np.arange(len(trend_data))
        z = np.polyfit(x, trend_data, 2)
        p = np.poly1d(z)

        # 미래 예측
        future_x = np.arange(len(trend_data), len(trend_data) + months * 30)
        future_volumes = p(future_x)

        # 신뢰도 계산
        residuals = np.array(trend_data) - p(x)
        std_error = np.std(residuals)
        confidence = 100 - (std_error / np.mean(trend_data) * 100)

        return {
            'keyword': keyword,
            'current_volume': trend_data[-1],
            'predicted_volumes': future_volumes.tolist(),
            'predicted_trend': 'increasing' if future_volumes[-1] > trend_data[-1] else 'decreasing',
            'confidence': max(0, min(100, confidence)),
            'prediction_dates': [
                (datetime.now() + timedelta(days=int(i))).strftime('%Y-%m-%d')
                for i in future_x - future_x[0]
            ]
        }

    # ==================== 검색 의도 분석 ====================

    def analyze_search_intent(self, keyword: str) -> Dict:
        """
        검색 의도 분석 (Informational, Navigational, Commercial, Transactional)
        """
        intent_signals = {
            'informational': ['what', 'how', 'why', 'guide', 'tutorial', '방법', '뜻'],
            'navigational': ['site', 'page', 'app', 'channel', '채널', '사이트'],
            'commercial': ['best', 'review', 'vs', 'comparison', 'top', '추천', '비교'],
            'transactional': ['buy', 'order', 'download', 'discount', '구매', '다운로드']
        }

        keyword_lower = keyword.lower()
        scores = {intent: 0 for intent in intent_signals}

        for intent, signals in intent_signals.items():
            for signal in signals:
                if signal in keyword_lower:
                    scores[intent] += 1

        primary_intent = max(scores, key=scores.get)

        return {
            'keyword': keyword,
            'primary_intent': primary_intent,
            'intent_scores': scores,
            'confidence': scores[primary_intent] / (sum(scores.values()) + 1)
        }

    # ==================== 도우미 함수들 ====================

    def _estimate_volume_google(self, keyword: str) -> int:
        """Google 검색량 추정"""
        base_volume = 1000
        length_factor = len(keyword.split())
        trending_boost = 1.0

        if any(trend in keyword.lower() for trend in ['2024', '2025', 'new', 'latest']):
            trending_boost = 1.5

        return int(base_volume * (1 + length_factor * 0.3) * trending_boost)

    def _estimate_volume_naver(self, keyword: str) -> int:
        """Naver 검색량 추정"""
        base_volume = 800
        return int(base_volume * (1 + len(keyword.split()) * 0.25))

    def _estimate_volume_daum(self, keyword: str) -> int:
        """Daum 검색량 추정"""
        base_volume = 600
        return int(base_volume * (1 + len(keyword.split()) * 0.2))

    def _calculate_keyword_difficulty(self, keyword: str) -> int:
        """키워드 난이도 계산 (0-100)"""
        difficulty = 30  # 기본값

        # 길이에 따른 난이도 감소
        words = keyword.split()
        if len(words) > 3:
            difficulty -= 10
        elif len(words) > 2:
            difficulty -= 5

        # 트렌딩 키워드는 난이도 증가
        if any(trend in keyword.lower() for trend in ['2024', '2025', 'new']):
            difficulty += 15

        # 일반적인 키워드는 난이도 증가
        common_words = ['how', 'what', 'best', 'top']
        if any(word in keyword.lower() for word in common_words):
            difficulty += 10

        return min(100, max(0, difficulty))

    def _estimate_cpc(self, keyword: str, platform: str) -> float:
        """클릭당 비용 추정"""
        base_cpc = {'google': 1.5, 'naver': 1.0}
        base = base_cpc.get(platform, 1.0)

        # 단어 수에 따른 조정
        word_factor = len(keyword.split()) * 0.2

        # 상용 키워드인지 확인
        commercial_words = ['buy', 'price', 'best', 'review']
        commercial_boost = 0.5 if any(w in keyword.lower() for w in commercial_words) else 0

        return round(base + word_factor + commercial_boost, 2)

    def _estimate_difficulty(self, keyword: str) -> str:
        """난이도 레벨"""
        score = self._calculate_keyword_difficulty(keyword)
        if score < 30:
            return "Easy"
        elif score < 60:
            return "Medium"
        else:
            return "Hard"

    def _estimate_monthly_search(self, keyword: str) -> int:
        """월간 검색량 추정"""
        daily = self._estimate_volume_google(keyword)
        return daily * 30

    def _calculate_opportunity(self, keyword: str) -> float:
        """기회 점수 계산 (검색량 vs 경쟁도)"""
        volume = self._estimate_volume_google(keyword)
        difficulty = self._calculate_keyword_difficulty(keyword)

        return (volume / 100) / (difficulty / 50 + 1)

    def _analyze_trend_advanced(self, keyword: str) -> str:
        """고급 트렌드 분석"""
        trending_keywords = ['new', 'best', 'top', 'trending', '2024', '2025', 'latest']
        if any(trend in keyword.lower() for trend in trending_keywords):
            return "rising"

        declining_keywords = ['old', 'outdated', 'legacy']
        if any(d in keyword.lower() for d in declining_keywords):
            return "declining"

        return "stable"

    def _calculate_trend_naver(self, keyword: str) -> str:
        """Naver 트렌드 분석"""
        return self._analyze_trend_advanced(keyword)

    def _calculate_trend_daum(self, keyword: str) -> str:
        """Daum 트렌드 분석"""
        return self._analyze_trend_advanced(keyword)

    def _estimate_competition_advanced(self, keyword: str) -> str:
        """고급 경쟁도 분석"""
        difficulty = self._calculate_keyword_difficulty(keyword)
        if difficulty < 30:
            return "Low"
        elif difficulty < 60:
            return "Medium"
        else:
            return "High"

    def _extract_google_related_advanced(self, keyword: str) -> List[str]:
        """고급 Google 관련 키워드"""
        related = [
            f"{keyword} tutorial",
            f"{keyword} guide",
            f"best {keyword}",
            f"{keyword} for beginners",
            f"{keyword} tips"
        ]
        return related

    def _extract_naver_related(self, soup) -> List[str]:
        """Naver 관련 키워드"""
        return ["관련 1", "관련 2", "관련 3"]

    def _extract_daum_related(self, soup) -> List[str]:
        """Daum 관련 키워드"""
        return ["관련 1", "관련 2", "관련 3"]

    def _generate_related_combinations(self, keyword: str) -> List[Dict]:
        """관련 키워드 조합 생성"""
        modifiers = ['best', 'how to', 'guide', 'tutorial', 'tips', 'for beginners']
        combinations = []

        for modifier in modifiers:
            combined = f"{modifier} {keyword}"
            combinations.append({
                'keyword': combined,
                'volume': self._estimate_volume_google(combined),
                'difficulty': self._calculate_keyword_difficulty(combined),
                'type': 'related_combination'
            })

        return combinations

    def _get_trending_keywords(self, keyword: str) -> List[Dict]:
        """트렌딩 키워드 생성"""
        trending = []
        year_keywords = [2024, 2025]

        for year in year_keywords:
            kw = f"{keyword} {year}"
            trending.append({
                'keyword': kw,
                'volume': self._estimate_volume_google(kw),
                'difficulty': self._calculate_keyword_difficulty(kw),
                'type': 'trending',
                'trend': 'rising'
            })

        return trending

    def _get_niche_keywords(self, keyword: str, topic: str = '') -> List[Dict]:
        """니치 키워드 생성"""
        niche_modifiers = ['advanced', 'professional', 'enterprise', 'startup']
        niche = []

        for modifier in niche_modifiers:
            kw = f"{modifier} {keyword}"
            niche.append({
                'keyword': kw,
                'volume': self._estimate_volume_google(kw),
                'difficulty': self._calculate_keyword_difficulty(kw),
                'type': 'niche',
                'conversion_potential': 0.7
            })

        return niche

    def _get_low_competition_keywords(self, keyword: str) -> List[Dict]:
        """경쟁 낮은 키워드"""
        low_comp = []
        long_tail_mods = ['specific', 'exact', 'detailed', 'comprehensive']

        for mod in long_tail_mods:
            kw = f"{keyword} {mod}"
            difficulty = self._calculate_keyword_difficulty(kw)
            if difficulty < 40:
                low_comp.append({
                    'keyword': kw,
                    'volume': self._estimate_volume_google(kw),
                    'difficulty': difficulty,
                    'type': 'low_competition'
                })

        return low_comp

    def _estimate_conversion(self, keyword: str) -> float:
        """전환율 잠재력 추정 (0-1)"""
        commercial_indicators = ['buy', 'how to', 'best', 'review', 'price']
        score = 0

        for indicator in commercial_indicators:
            if indicator in keyword.lower():
                score += 0.2

        return min(1.0, score)

    def _recommend_keyword_type(self, short_vol: float, long_vol: float) -> str:
        """키워드 타입 추천"""
        if short_vol > long_vol * 1.5:
            return "Focus on short-tail keywords for higher volume"
        elif long_vol > short_vol * 1.5:
            return "Focus on long-tail keywords for lower competition"
        else:
            return "Mix both short and long-tail keywords"

    def _generate_seasonal_trend(self, keyword: str, date: datetime) -> int:
        """계절성 트렌드 데이터 생성"""
        base = 100

        # 월별 계절성
        month_factor = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)

        # 주말/평일 패턴
        day_factor = 1 + 0.1 * np.sin(2 * np.pi * date.weekday() / 7)

        return int(base * month_factor * day_factor)

    def _generate_trend_point_for_prediction(self, keyword: str, date: datetime) -> int:
        """예측용 트렌드 포인트"""
        base = self._estimate_volume_google(keyword) / 2
        noise = np.random.normal(0, base * 0.1)
        return max(0, int(base + noise))

    def _recommend_posting_schedule(self, monthly_avg: pd.Series, daily_avg: pd.Series) -> Dict:
        """포스팅 일정 추천"""
        best_month = monthly_avg.idxmax()
        best_day = daily_avg.idxmax()

        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                    'Friday', 'Saturday', 'Sunday']

        return {
            'best_month': month_names[best_month - 1],
            'best_day': day_names[best_day],
            'avoid_months': [month_names[i] for i in monthly_avg.nsmallest(2).index - 1],
            'posting_frequency': 'Daily' if daily_avg.std() < daily_avg.mean() * 0.3 else 'Regular'
        }


class AdvancedKeywordDataExporter:
    """고급 데이터 내보내기"""

    @staticmethod
    def export_to_csv(data: pd.DataFrame, filename: str) -> str:
        """CSV로 내보내기"""
        try:
            data.to_csv(filename, index=False, encoding='utf-8-sig')
            return f"✅ 데이터가 {filename}에 저장되었습니다."
        except Exception as e:
            return f"❌ 저장 실패: {str(e)}"

    @staticmethod
    def export_to_json(data: Dict, filename: str) -> str:
        """JSON으로 내보내기"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            return f"✅ 데이터가 {filename}에 저장되었습니다."
        except Exception as e:
            return f"❌ 저장 실패: {str(e)}"

    @staticmethod
    def export_to_excel(data: pd.DataFrame, filename: str) -> str:
        """Excel로 내보내기"""
        try:
            data.to_excel(filename, index=False)
            return f"✅ 데이터가 {filename}에 저장되었습니다."
        except Exception as e:
            return f"❌ 저장 실패: {str(e)}"

    @staticmethod
    def generate_report(analysis_data: Dict, filename: str = 'keyword_report.json') -> str:
        """종합 분석 보고서 생성"""
        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'analysis': analysis_data
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)

            return f"✅ 보고서가 {filename}에 저장되었습니다."
        except Exception as e:
            return f"❌ 보고서 생성 실패: {str(e)}"


# 하위 호환성을 위한 별칭
KeywordAnalyzer = AdvancedKeywordAnalyzer
KeywordDataExporter = AdvancedKeywordDataExporter
