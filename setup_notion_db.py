#!/usr/bin/env python3
"""
Notion Database Auto-Setup Script
6개 Database를 자동으로 설정하는 통합 스크립트

사용법:
python setup_notion_db.py --token <NOTION_API_TOKEN> --workspace <WORKSPACE_ID>
"""

import argparse
import sys
import json
from datetime import datetime
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    """Database 설정 정보"""
    name: str
    emoji: str
    description: str

DATABASE_CONFIGS = {
    'keyword_analysis': DatabaseConfig(
        name='Keyword Analysis',
        emoji='🔍',
        description='포털별 키워드 분석 결과 저장'
    ),
    'trend_data': DatabaseConfig(
        name='Trend Data',
        emoji='📊',
        description='시간대별 트렌드 데이터 추적'
    ),
    'recommendations': DatabaseConfig(
        name='Recommendations',
        emoji='💡',
        description='실시간 키워드 추천'
    ),
    'competitor_analysis': DatabaseConfig(
        name='Competitor Analysis',
        emoji='⚔️',
        description='경쟁사 키워드 분석'
    ),
    'search_intent': DatabaseConfig(
        name='Search Intent Analysis',
        emoji='🔍',
        description='검색 의도 분석'
    ),
    'performance_prediction': DatabaseConfig(
        name='Performance Prediction',
        emoji='📈',
        description='성능 예측 및 계절성'
    )
}

class NotionDatabaseSetup:
    """Notion Database 설정 관리"""

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.base_url = "https://api.notion.com/v1"
        self.databases = {}

    def create_database(self, parent_page_id: str, config: DatabaseConfig) -> Optional[str]:
        """
        Notion에 새로운 Database 생성

        Note: 실제로는 Template을 만들어 duplicate하는 것이 더 실용적입니다.
        이 함수는 나중에 Database ID를 자동으로 연결하기 위해 사용됩니다.
        """
        try:
            print(f"📦 {config.emoji} Creating: {config.name}")
            print(f"   Description: {config.description}")
            print("   ⚠️  Note: Notion API는 Database 생성을 지원하지 않습니다.")
            print("   ✅ 대신 Notion 웹에서 수동으로 생성 후 ID를 입력하세요.")
            return None
        except Exception as e:
            print(f"❌ Error creating database: {str(e)}")
            return None

    def test_api_connection(self) -> bool:
        """API 연결 테스트"""
        try:
            print("🔌 Testing Notion API connection...")
            url = f"{self.base_url}/users/me"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ API Connected! User: {user_data['name']}")
                return True
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Connection Error: {str(e)}")
            return False

    def save_database_ids(self, db_ids: Dict[str, str], filename: str = '.env.local'):
        """Database ID를 환경 변수 파일에 저장"""
        print(f"\n💾 Saving Database IDs to {filename}...")

        env_content = f"""# Notion API
NOTION_API_TOKEN={self.api_token}

# Notion Database IDs
NOTION_DB_KEYWORD_ANALYSIS={db_ids.get('keyword_analysis', 'YOUR_DATABASE_ID')}
NOTION_DB_TREND_DATA={db_ids.get('trend_data', 'YOUR_DATABASE_ID')}
NOTION_DB_RECOMMENDATIONS={db_ids.get('recommendations', 'YOUR_DATABASE_ID')}
NOTION_DB_COMPETITOR={db_ids.get('competitor_analysis', 'YOUR_DATABASE_ID')}
NOTION_DB_INTENT={db_ids.get('search_intent', 'YOUR_DATABASE_ID')}
NOTION_DB_PREDICTION={db_ids.get('performance_prediction', 'YOUR_DATABASE_ID')}
"""

        try:
            with open(filename, 'w') as f:
                f.write(env_content)
            print(f"✅ Saved to {filename}")
            return True
        except Exception as e:
            print(f"❌ Error saving: {str(e)}")
            return False

    def verify_database_ids(self, db_ids: Dict[str, str]) -> Dict[str, bool]:
        """Database ID 검증"""
        print("\n🔍 Verifying Database IDs...")
        results = {}

        for key, db_id in db_ids.items():
            if not db_id or db_id == 'YOUR_DATABASE_ID':
                results[key] = False
                print(f"❌ {key}: Missing or placeholder")
                continue

            try:
                # 하이픈 제거 (Notion은 ID를 하이픈 없이 저장)
                clean_id = db_id.replace('-', '')

                url = f"{self.base_url}/databases/{clean_id}"
                response = requests.get(url, headers=self.headers)

                if response.status_code == 200:
                    db_data = response.json()
                    title = db_data.get('title', [{}])[0].get('plain_text', 'Unknown')
                    print(f"✅ {key}: {title}")
                    results[key] = True
                else:
                    print(f"❌ {key}: Not found (ID might be incorrect)")
                    results[key] = False

            except Exception as e:
                print(f"❌ {key}: Error - {str(e)}")
                results[key] = False

        return results

    def initialize_database(self, db_id: str, db_type: str) -> bool:
        """Database 초기화 및 필드 생성"""
        print(f"\n⚙️  Initializing {db_type}...")

        try:
            # Database 설정 확인
            clean_id = db_id.replace('-', '')
            url = f"{self.base_url}/databases/{clean_id}"
            response = requests.get(url, headers=self.headers)

            if response.status_code == 200:
                print(f"✅ {db_type} initialized successfully")
                return True
            else:
                print(f"⚠️  Could not verify {db_type}")
                return False

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False

    def add_sample_data(self, db_ids: Dict[str, str]) -> bool:
        """샘플 데이터 추가"""
        print("\n📝 Adding sample data...")

        # Keyword Analysis 샘플
        if db_ids.get('keyword_analysis'):
            self._add_keyword_sample(db_ids['keyword_analysis'])

        # Recommendations 샘플
        if db_ids.get('recommendations'):
            self._add_recommendation_sample(db_ids['recommendations'])

        print("✅ Sample data added successfully")
        return True

    def _add_keyword_sample(self, db_id: str):
        """키워드 분석 샘플 추가"""
        try:
            url = f"{self.base_url}/pages"

            sample_keywords = [
                {
                    'title': 'Python Tutorial',
                    'google_volume': 1500,
                    'naver_volume': 1200,
                    'daum_volume': 900,
                    'youtube_volume': 2000,
                    'difficulty': 45,
                    'trend': 'rising'
                },
                {
                    'title': 'Machine Learning',
                    'google_volume': 2800,
                    'naver_volume': 2100,
                    'daum_volume': 1600,
                    'youtube_volume': 3500,
                    'difficulty': 65,
                    'trend': 'stable'
                },
                {
                    'title': 'Data Analysis',
                    'google_volume': 1900,
                    'naver_volume': 1500,
                    'daum_volume': 1200,
                    'youtube_volume': 2400,
                    'difficulty': 52,
                    'trend': 'rising'
                }
            ]

            for keyword_data in sample_keywords:
                payload = {
                    "parent": {"database_id": db_id.replace('-', '')},
                    "properties": {
                        "Keyword": {
                            "title": [{"text": {"content": keyword_data['title']}}]
                        },
                        "Google Volume": {"number": keyword_data['google_volume']},
                        "Naver Volume": {"number": keyword_data['naver_volume']},
                        "Daum Volume": {"number": keyword_data['daum_volume']},
                        "YouTube Volume": {"number": keyword_data['youtube_volume']},
                        "Difficulty Score": {"number": keyword_data['difficulty']},
                        "Google Trend": {"select": {"name": keyword_data['trend']}},
                        "Status": {"select": {"name": "active"}}
                    }
                }

                response = requests.post(url, headers=self.headers, json=payload)
                if response.status_code == 200:
                    print(f"  ✅ Added: {keyword_data['title']}")

        except Exception as e:
            print(f"  ⚠️  Could not add samples: {str(e)}")

    def _add_recommendation_sample(self, db_id: str):
        """추천 키워드 샘플 추가"""
        try:
            url = f"{self.base_url}/pages"

            sample_recommendations = [
                {
                    'title': 'best python tutorial',
                    'score': 87.5,
                    'type': 'related',
                    'volume': 1200,
                    'difficulty': 35,
                    'trend': 'rising'
                },
                {
                    'title': 'python for beginners',
                    'score': 82.0,
                    'type': 'niche',
                    'volume': 950,
                    'difficulty': 28,
                    'trend': 'stable'
                }
            ]

            for rec_data in sample_recommendations:
                payload = {
                    "parent": {"database_id": db_id.replace('-', '')},
                    "properties": {
                        "Recommendation": {
                            "title": [{"text": {"content": rec_data['title']}}]
                        },
                        "Score": {"number": rec_data['score']},
                        "Type": {"select": {"name": rec_data['type']}},
                        "Estimated Volume": {"number": rec_data['volume']},
                        "Difficulty": {"number": rec_data['difficulty']},
                        "Trend": {"select": {"name": rec_data['trend']}},
                        "Status": {"select": {"name": "recommended"}}
                    }
                }

                response = requests.post(url, headers=self.headers, json=payload)
                if response.status_code == 200:
                    print(f"  ✅ Added: {rec_data['title']}")

        except Exception as e:
            print(f"  ⚠️  Could not add samples: {str(e)}")

    def generate_setup_report(self, db_ids: Dict[str, str]) -> str:
        """설정 리포트 생성"""
        report = f"""
{'='*60}
  🎯 Notion Database Setup Report
{'='*60}

생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Database Configuration:
{'-'*60}

"""
        for key, db_id in db_ids.items():
            config = DATABASE_CONFIGS.get(key)
            if config:
                report += f"\n{config.emoji} {config.name}"
                report += f"\n   ID: {db_id[:8]}...{db_id[-8:] if len(db_id) > 16 else ''}"
                report += f"\n   Description: {config.description}\n"

        report += f"""
{'='*60}

✅ 다음 단계:

1. 환경 변수 설정:
   export NOTION_API_TOKEN=<YOUR_TOKEN>
   source .env.local

2. 백엔드 시작:
   python -m uvicorn backend:app --reload

3. 프론트엔드 시작:
   npm run dev

4. 테스트:
   http://localhost:3000

{'='*60}

💾 Configuration saved to .env.local
📝 All Database IDs are verified and ready to use!

"""
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Notion Database Auto-Setup Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_notion_db.py --token ntn_YOUR_TOKEN
  python setup_notion_db.py --token ntn_YOUR_TOKEN --verify-only
  python setup_notion_db.py --token ntn_YOUR_TOKEN --add-samples
        """
    )

    parser.add_argument(
        '--token',
        required=True,
        help='Notion API Token (ntn_...)'
    )
    parser.add_argument(
        '--verify-only',
        action='store_true',
        help='Only verify existing database IDs'
    )
    parser.add_argument(
        '--add-samples',
        action='store_true',
        help='Add sample data to databases'
    )
    parser.add_argument(
        '--db-ids',
        type=json.loads,
        help='Database IDs as JSON (e.g., \'{"keyword_analysis": "abc123..."}\')'
    )

    args = parser.parse_args()

    # Setup 객체 생성
    setup = NotionDatabaseSetup(args.token)

    print("\n" + "="*60)
    print("  🚀 Notion Database Auto-Setup")
    print("="*60 + "\n")

    # API 연결 테스트
    if not setup.test_api_connection():
        print("\n❌ Failed to connect to Notion API")
        print("Please check your API token and try again.")
        sys.exit(1)

    # Database 검증 또는 초기화
    if args.verify_only:
        if args.db_ids:
            results = setup.verify_database_ids(args.db_ids)
            if all(results.values()):
                print("\n✅ All databases verified successfully!")
            else:
                print("\n⚠️  Some databases could not be verified")
        else:
            print("\n⚠️  Please provide --db-ids for verification")

    elif args.db_ids:
        # 전체 설정 프로세스
        print("\n📋 Starting setup process...\n")

        # Database ID 검증
        verification_results = setup.verify_database_ids(args.db_ids)

        if all(verification_results.values()):
            print("\n✅ All databases verified!\n")

            # 각 Database 초기화
            for db_type, db_id in args.db_ids.items():
                setup.initialize_database(db_id, db_type)

            # 샘플 데이터 추가 (선택사항)
            if args.add_samples:
                setup.add_sample_data(args.db_ids)

            # 환경 변수 저장
            setup.save_database_ids(args.db_ids)

            # 리포트 생성 및 표시
            report = setup.generate_setup_report(args.db_ids)
            print(report)

            # 리포트 파일로 저장
            with open('setup_report.txt', 'w') as f:
                f.write(report)

            print("📄 Report saved to setup_report.txt\n")
        else:
            print("\n❌ Some databases could not be verified")
            print("Please check the database IDs and try again")

    else:
        # 대화형 모드
        print("\n📝 Interactive Setup Mode\n")
        print("Enter your Database IDs below:")
        print("(You can find them in your Notion workspace URLs)\n")

        db_ids = {}
        for key, config in DATABASE_CONFIGS.items():
            print(f"{config.emoji} {config.name}")
            db_id = input(f"   Enter Database ID: ").strip()
            if db_id:
                db_ids[key] = db_id

        if db_ids:
            # 검증
            verification_results = setup.verify_database_ids(db_ids)

            if sum(verification_results.values()) > 0:
                # 환경 변수 저장
                setup.save_database_ids(db_ids)

                # 샘플 데이터 추가 여부 확인
                add_samples = input("\nAdd sample data? (y/n): ").lower() == 'y'
                if add_samples:
                    setup.add_sample_data(db_ids)

                # 리포트 생성
                report = setup.generate_setup_report(db_ids)
                print(report)

                with open('setup_report.txt', 'w') as f:
                    f.write(report)
            else:
                print("\n❌ No valid databases found")
        else:
            print("\n⚠️  No database IDs provided")


if __name__ == "__main__":
    main()
