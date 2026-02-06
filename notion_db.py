"""
Notion Database Integration Module
Notion API를 통한 키워드 분석 데이터 저장 및 관리
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time

class NotionDB:
    """Notion Database와의 연동을 관리합니다"""

    def __init__(self, api_token: str):
        """
        Args:
            api_token: Notion API Token (ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ)
        """
        self.api_token = api_token
        self.notion_version = "2022-06-28"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Notion-Version": self.notion_version,
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.notion.com/v1"

        # Database IDs (사용자가 설정해야 함)
        self.databases = {
            'keyword_analysis': None,  # 키워드 분석
            'trend_data': None,         # 트렌드 데이터
            'recommendations': None,    # 추천 키워드
            'competitor_analysis': None, # 경쟁사 분석
            'search_intent': None,      # 검색 의도
            'performance_prediction': None  # 성능 예측
        }

    def set_database_ids(self, db_ids: Dict[str, str]):
        """Database ID 설정"""
        self.databases.update(db_ids)

    # ==================== Keyword Analysis ====================

    def add_keyword_analysis(self, keyword: str, analysis_data: Dict) -> Dict:
        """포털별 키워드 분석 데이터를 Notion에 추가"""
        properties = {
            "Keyword": {
                "title": [{"text": {"content": keyword}}]
            },
            "Google Volume": {
                "number": analysis_data.get('google_volume', 0)
            },
            "Naver Volume": {
                "number": analysis_data.get('naver_volume', 0)
            },
            "Daum Volume": {
                "number": analysis_data.get('daum_volume', 0)
            },
            "YouTube Volume": {
                "number": analysis_data.get('youtube_volume', 0)
            },
            "Difficulty Score": {
                "number": analysis_data.get('difficulty_score', 0)
            },
            "Google CPC": {
                "number": analysis_data.get('google_cpc', 0)
            },
            "Naver CPC": {
                "number": analysis_data.get('naver_cpc', 0)
            },
            "Opportunity Score": {
                "number": analysis_data.get('opportunity_score', 0)
            },
            "Google Trend": {
                "select": {"name": analysis_data.get('google_trend', 'stable')}
            },
            "Naver Trend": {
                "select": {"name": analysis_data.get('naver_trend', 'stable')}
            },
            "Search Intent": {
                "select": {"name": analysis_data.get('search_intent', 'informational')}
            },
            "Status": {
                "select": {"name": analysis_data.get('status', 'active')}
            }
        }

        # 선택사항: 관련 키워드
        if 'related_keywords' in analysis_data:
            properties["Related Keywords"] = {
                "multi_select": [
                    {"name": kw} for kw in analysis_data['related_keywords'][:5]
                ]
            }

        return self._create_page(self.databases['keyword_analysis'], properties)

    def get_keyword_analysis(self, keyword: str) -> Optional[Dict]:
        """키워드 분석 데이터 조회"""
        response = self._query_database(
            self.databases['keyword_analysis'],
            filter_condition={
                "property": "Keyword",
                "title": {"equals": keyword}
            }
        )

        if response.get('results'):
            return self._parse_page(response['results'][0])
        return None

    def get_all_keywords(self, limit: int = 50) -> List[Dict]:
        """모든 활성 키워드 조회"""
        response = self._query_database(
            self.databases['keyword_analysis'],
            filter_condition={
                "property": "Status",
                "select": {"equals": "active"}
            },
            sorts=[
                {"property": "Updated Date", "direction": "descending"}
            ]
        )

        return [self._parse_page(page) for page in response.get('results', [])[:limit]]

    def update_keyword_analysis(self, page_id: str, updates: Dict) -> Dict:
        """키워드 분석 데이터 업데이트"""
        properties = {}

        if 'google_volume' in updates:
            properties["Google Volume"] = {"number": updates['google_volume']}
        if 'naver_volume' in updates:
            properties["Naver Volume"] = {"number": updates['naver_volume']}
        if 'opportunity_score' in updates:
            properties["Opportunity Score"] = {"number": updates['opportunity_score']}
        if 'status' in updates:
            properties["Status"] = {"select": {"name": updates['status']}}

        return self._update_page(page_id, properties)

    # ==================== Trend Data ====================

    def add_trend_data(self, keyword: str, trend_info: Dict) -> Dict:
        """트렌드 데이터 추가"""
        properties = {
            "Date": {
                "date": {"start": trend_info.get('date', datetime.now().isoformat())}
            },
            "Keyword": {
                "relation": [{"id": trend_info.get('keyword_page_id', '')}]
            },
            "Search Volume": {
                "number": trend_info.get('search_volume', 0)
            },
            "Interest Level": {
                "number": trend_info.get('interest_level', 0)
            },
            "Trend Direction": {
                "select": {"name": trend_info.get('trend_direction', 'stable')}
            },
            "Portal": {
                "select": {"name": trend_info.get('portal', 'Google')}
            },
            "Peak Day": {
                "checkbox": trend_info.get('peak_day', False)
            }
        }

        return self._create_page(self.databases['trend_data'], properties)

    def get_trend_history(self, keyword: str, days: int = 30) -> List[Dict]:
        """키워드의 트렌드 히스토리 조회"""
        start_date = (datetime.now() - timedelta(days=days)).isoformat()

        response = self._query_database(
            self.databases['trend_data'],
            filter_condition={
                "and": [
                    {
                        "property": "Keyword",
                        "relation": {"contains": keyword}
                    },
                    {
                        "property": "Date",
                        "date": {"after": start_date}
                    }
                ]
            },
            sorts=[
                {"property": "Date", "direction": "ascending"}
            ]
        )

        return [self._parse_page(page) for page in response.get('results', [])]

    # ==================== Recommendations ====================

    def add_recommendation(self, base_keyword: str, recommendation_data: Dict) -> Dict:
        """추천 키워드 추가"""
        properties = {
            "Recommendation": {
                "title": [{"text": {"content": recommendation_data.get('keyword', '')}}]
            },
            "Base Keyword": {
                "relation": [{"id": recommendation_data.get('base_keyword_id', '')}]
            },
            "Score": {
                "number": recommendation_data.get('score', 0)
            },
            "Type": {
                "select": {"name": recommendation_data.get('type', 'related')}
            },
            "Estimated Volume": {
                "number": recommendation_data.get('volume', 0)
            },
            "Difficulty": {
                "number": recommendation_data.get('difficulty', 0)
            },
            "Trend": {
                "select": {"name": recommendation_data.get('trend', 'stable')}
            },
            "Conversion Potential": {
                "number": recommendation_data.get('conversion_potential', 0)
            },
            "Status": {
                "select": {"name": "recommended"}
            },
            "Priority": {
                "number": recommendation_data.get('priority', 3)
            }
        }

        if 'reason' in recommendation_data:
            properties["Reason"] = {
                "text": [{"text": {"content": recommendation_data['reason']}}]
            }

        return self._create_page(self.databases['recommendations'], properties)

    def get_recommendations(self, base_keyword: str, limit: int = 20) -> List[Dict]:
        """추천 키워드 조회"""
        response = self._query_database(
            self.databases['recommendations'],
            filter_condition={
                "and": [
                    {
                        "property": "Base Keyword",
                        "relation": {"contains": base_keyword}
                    },
                    {
                        "property": "Status",
                        "select": {"equals": "recommended"}
                    }
                ]
            },
            sorts=[
                {"property": "Score", "direction": "descending"}
            ]
        )

        return [self._parse_page(page) for page in response.get('results', [])[:limit]]

    # ==================== Competitor Analysis ====================

    def add_competitor_analysis(self, analysis_data: Dict) -> Dict:
        """경쟁사 분석 추가"""
        properties = {
            "Analysis Name": {
                "title": [{"text": {"content": analysis_data.get('name', '')}}]
            },
            "Competitor Name": {
                "text": [{"text": {"content": analysis_data.get('competitor', '')}}]
            },
            "Our Channel Name": {
                "text": [{"text": {"content": analysis_data.get('our_channel', '')}}]
            },
            "Total Opportunities": {
                "number": analysis_data.get('opportunity_count', 0)
            },
            "Analysis Date": {
                "date": {"start": datetime.now().isoformat()}
            },
            "Next Review": {
                "date": {"start": (datetime.now() + timedelta(days=30)).isoformat()}
            }
        }

        if 'our_keywords' in analysis_data:
            properties["Our Keywords"] = {
                "multi_select": [
                    {"name": kw} for kw in analysis_data['our_keywords'][:5]
                ]
            }

        if 'competitor_keywords' in analysis_data:
            properties["Competitor Keywords"] = {
                "multi_select": [
                    {"name": kw} for kw in analysis_data['competitor_keywords'][:5]
                ]
            }

        if 'recommendations' in analysis_data:
            properties["Recommendations"] = {
                "text": [{"text": {"content": analysis_data['recommendations']}}]
            }

        return self._create_page(self.databases['competitor_analysis'], properties)

    # ==================== Search Intent Analysis ====================

    def add_search_intent(self, keyword: str, intent_data: Dict) -> Dict:
        """검색 의도 분석 추가"""
        properties = {
            "Keyword": {
                "relation": [{"id": intent_data.get('keyword_page_id', '')}]
            },
            "Primary Intent": {
                "select": {"name": intent_data.get('primary_intent', 'informational')}
            },
            "Intent Confidence": {
                "number": intent_data.get('confidence', 0)
            },
            "Informational Score": {
                "number": intent_data.get('informational_score', 0)
            },
            "Navigational Score": {
                "number": intent_data.get('navigational_score', 0)
            },
            "Commercial Score": {
                "number": intent_data.get('commercial_score', 0)
            },
            "Transactional Score": {
                "number": intent_data.get('transactional_score', 0)
            },
            "Suggested Format": {
                "select": {"name": intent_data.get('format', 'article')}
            },
            "Target Audience": {
                "text": [{"text": {"content": intent_data.get('audience', '')}}]
            }
        }

        if 'content_types' in intent_data:
            properties["Content Type Recommendation"] = {
                "multi_select": [
                    {"name": ct} for ct in intent_data['content_types'][:4]
                ]
            }

        return self._create_page(self.databases['search_intent'], properties)

    # ==================== Performance Prediction ====================

    def add_performance_prediction(self, keyword: str, prediction_data: Dict) -> Dict:
        """성능 예측 추가"""
        properties = {
            "Keyword": {
                "relation": [{"id": prediction_data.get('keyword_page_id', '')}]
            },
            "Current Volume": {
                "number": prediction_data.get('current_volume', 0)
            },
            "Predicted 1M Volume": {
                "number": prediction_data.get('pred_1m_volume', 0)
            },
            "Predicted 2M Volume": {
                "number": prediction_data.get('pred_2m_volume', 0)
            },
            "Predicted 3M Volume": {
                "number": prediction_data.get('pred_3m_volume', 0)
            },
            "Predicted Trend": {
                "select": {"name": prediction_data.get('trend', 'stable')}
            },
            "Growth Rate": {
                "number": prediction_data.get('growth_rate', 0)
            },
            "Confidence Level": {
                "select": {"name": prediction_data.get('confidence_level', 'medium')}
            },
            "Confidence Score": {
                "number": prediction_data.get('confidence_score', 0)
            },
            "Seasonality Strength": {
                "number": prediction_data.get('seasonality_strength', 0)
            },
            "Best Posting Day": {
                "select": {"name": prediction_data.get('best_day', 'Friday')}
            },
            "Best Posting Month": {
                "select": {"name": prediction_data.get('best_month', 'January')}
            },
            "Posting Frequency": {
                "select": {"name": prediction_data.get('frequency', 'Weekly')}
            },
            "ROI Estimate": {
                "number": prediction_data.get('roi_estimate', 0)
            }
        }

        if 'peak_seasons' in prediction_data:
            properties["Peak Season"] = {
                "multi_select": [
                    {"name": season} for season in prediction_data['peak_seasons'][:2]
                ]
            }

        if 'low_seasons' in prediction_data:
            properties["Low Season"] = {
                "multi_select": [
                    {"name": season} for season in prediction_data['low_seasons'][:2]
                ]
            }

        return self._create_page(self.databases['performance_prediction'], properties)

    # ==================== 유틸리티 메서드 ====================

    def _create_page(self, database_id: str, properties: Dict) -> Dict:
        """Notion에 새로운 페이지 생성"""
        url = f"{self.base_url}/pages"

        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error creating page: {response.status_code} - {response.text}")
            return {}

    def _query_database(self, database_id: str, filter_condition: Dict = None,
                       sorts: List[Dict] = None) -> Dict:
        """Notion Database 쿼리"""
        url = f"{self.base_url}/databases/{database_id}/query"

        payload = {}
        if filter_condition:
            payload["filter"] = filter_condition
        if sorts:
            payload["sorts"] = sorts

        response = requests.post(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error querying database: {response.status_code} - {response.text}")
            return {"results": []}

    def _update_page(self, page_id: str, properties: Dict) -> Dict:
        """Notion 페이지 업데이트"""
        url = f"{self.base_url}/pages/{page_id}"

        payload = {"properties": properties}

        response = requests.patch(url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error updating page: {response.status_code} - {response.text}")
            return {}

    def _parse_page(self, page: Dict) -> Dict:
        """Notion 페이지를 Python Dict로 변환"""
        parsed = {
            "page_id": page["id"],
            "created_time": page["created_time"],
            "last_edited_time": page["last_edited_time"],
            "properties": {}
        }

        for prop_name, prop_value in page["properties"].items():
            parsed["properties"][prop_name] = self._parse_property(prop_value)

        return parsed

    def _parse_property(self, prop: Dict) -> any:
        """Notion 속성 파싱"""
        prop_type = prop["type"]

        if prop_type == "title":
            return prop["title"][0]["text"]["content"] if prop["title"] else ""
        elif prop_type == "text":
            return prop["text"][0]["text"]["content"] if prop["text"] else ""
        elif prop_type == "number":
            return prop["number"]
        elif prop_type == "select":
            return prop["select"]["name"] if prop["select"] else None
        elif prop_type == "multi_select":
            return [item["name"] for item in prop["multi_select"]]
        elif prop_type == "date":
            return prop["date"]["start"] if prop["date"] else None
        elif prop_type == "checkbox":
            return prop["checkbox"]
        elif prop_type == "relation":
            return [item["id"] for item in prop["relation"]]
        elif prop_type == "formula":
            return prop["formula"]["string"] if prop["formula"]["type"] == "string" else prop["formula"]["number"]
        else:
            return None

    # ==================== 배치 작업 ====================

    def sync_keyword_analysis(self, keyword: str, analysis_data: Dict) -> bool:
        """키워드 분석 데이터 동기화"""
        try:
            # 기존 데이터 확인
            existing = self.get_keyword_analysis(keyword)

            if existing:
                # 업데이트
                self.update_keyword_analysis(
                    existing['page_id'],
                    analysis_data
                )
            else:
                # 신규 생성
                self.add_keyword_analysis(keyword, analysis_data)

            return True
        except Exception as e:
            print(f"Error syncing keyword analysis: {str(e)}")
            return False

    def batch_add_trend_data(self, keyword: str, trend_list: List[Dict]) -> int:
        """배치로 트렌드 데이터 추가"""
        count = 0
        for trend in trend_list:
            try:
                self.add_trend_data(keyword, trend)
                count += 1
                time.sleep(0.3)  # API Rate Limiting
            except Exception as e:
                print(f"Error adding trend data: {str(e)}")

        return count

    def batch_add_recommendations(self, keyword: str, recommendations: List[Dict]) -> int:
        """배치로 추천 키워드 추가"""
        count = 0
        for rec in recommendations:
            try:
                self.add_recommendation(keyword, rec)
                count += 1
                time.sleep(0.3)
            except Exception as e:
                print(f"Error adding recommendation: {str(e)}")

        return count
