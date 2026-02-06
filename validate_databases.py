#!/usr/bin/env python3
"""
Database Validation & Testing Script
모든 Database를 검증하고 테스트합니다.

사용법:
python validate_databases.py --config .env.local
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from notion_db import NotionDB
from datetime import datetime
import json

class DatabaseValidator:
    """Database 검증 클래스"""

    def __init__(self, api_token: str, db_ids: dict):
        self.notion_db = NotionDB(api_token)
        self.notion_db.set_database_ids(db_ids)
        self.db_ids = db_ids
        self.results = {}

    def validate_all(self) -> bool:
        """모든 Database 검증"""
        print("\n" + "="*60)
        print("  🔍 Database Validation")
        print("="*60 + "\n")

        databases = {
            'keyword_analysis': 'Keyword Analysis 🔍',
            'trend_data': 'Trend Data 📊',
            'recommendations': 'Recommendations 💡',
            'competitor_analysis': 'Competitor Analysis ⚔️',
            'search_intent': 'Search Intent 🔍',
            'performance_prediction': 'Performance Prediction 📈'
        }

        for db_key, display_name in databases.items():
            print(f"📋 Validating {display_name}...")
            self.results[db_key] = self._validate_database(db_key)
            print()

        return self._print_validation_summary()

    def _validate_database(self, db_key: str) -> dict:
        """개별 Database 검증"""
        db_id = self.db_ids.get(db_key)

        if not db_id:
            return {'status': False, 'error': 'Database ID not found'}

        try:
            # 기본 연결 테스트
            response = self.notion_db._query_database(db_id)

            if 'results' not in response:
                return {'status': False, 'error': 'Invalid response'}

            result_count = len(response.get('results', []))

            # 상세 검증
            validation = {
                'status': True,
                'db_id': db_id[:16] + '...',
                'total_pages': result_count,
                'has_data': result_count > 0,
                'properties': self._count_properties(response),
                'timestamp': datetime.now().isoformat()
            }

            print(f"  ✅ Connected")
            print(f"  📊 Total pages: {result_count}")
            print(f"  🔧 Properties: {validation['properties']}")

            if result_count > 0:
                print(f"  ✅ Has data")
            else:
                print(f"  ⚠️  No data yet")

            return validation

        except Exception as e:
            error_msg = str(e)
            print(f"  ❌ Error: {error_msg}")
            return {'status': False, 'error': error_msg}

    def _count_properties(self, response: dict) -> int:
        """속성 개수 카운트"""
        if response.get('results'):
            first_page = response['results'][0]
            return len(first_page.get('properties', {}))
        return 0

    def _print_validation_summary(self) -> bool:
        """검증 결과 요약"""
        print("="*60)
        print("  📊 Validation Summary")
        print("="*60 + "\n")

        success_count = sum(1 for r in self.results.values() if r.get('status', False))
        total_count = len(self.results)

        print(f"Overall: {success_count}/{total_count} databases validated\n")

        for db_name, result in self.results.items():
            status_icon = "✅" if result.get('status', False) else "❌"
            db_display = db_name.replace('_', ' ').title()

            if result.get('status', False):
                print(f"{status_icon} {db_display}")
                print(f"   Pages: {result.get('total_pages', 0)}")
                print(f"   Properties: {result.get('properties', 0)}")
            else:
                print(f"{status_icon} {db_display}")
                print(f"   Error: {result.get('error', 'Unknown error')}")
            print()

        print("="*60 + "\n")

        return all(r.get('status', False) for r in self.results.values())

    def test_api_operations(self) -> bool:
        """API 작업 테스트"""
        print("="*60)
        print("  🧪 API Operations Test")
        print("="*60 + "\n")

        tests = {
            '📝 Add Keyword Analysis': self._test_add_keyword,
            '💡 Add Recommendation': self._test_add_recommendation,
            '📊 Query Database': self._test_query,
            '📈 Update Record': self._test_update,
        }

        test_results = {}

        for test_name, test_func in tests.items():
            print(f"Testing: {test_name}")
            try:
                result = test_func()
                test_results[test_name] = result
                status = "✅" if result else "❌"
                print(f"{status} {test_name}\n")
            except Exception as e:
                test_results[test_name] = False
                print(f"❌ {test_name}")
                print(f"   Error: {str(e)}\n")

        # 테스트 요약
        print("="*60)
        print("  🧪 Test Summary")
        print("="*60 + "\n")

        passed = sum(1 for v in test_results.values() if v)
        total = len(test_results)

        print(f"Passed: {passed}/{total}\n")

        for test_name, result in test_results.items():
            status = "✅" if result else "❌"
            print(f"{status} {test_name}")

        print("\n" + "="*60 + "\n")

        return all(test_results.values())

    def _test_add_keyword(self) -> bool:
        """키워드 추가 테스트"""
        try:
            self.notion_db.add_keyword_analysis('Test Keyword', {
                'google_volume': 1000,
                'naver_volume': 800,
                'daum_volume': 600,
                'youtube_volume': 1500,
                'difficulty_score': 50,
                'google_trend': 'stable'
            })
            return True
        except:
            return False

    def _test_add_recommendation(self) -> bool:
        """추천 추가 테스트"""
        try:
            self.notion_db.add_recommendation('Test Keyword', {
                'keyword': 'test recommendation',
                'score': 80.0,
                'type': 'related',
                'volume': 500,
                'difficulty': 30,
                'trend': 'rising'
            })
            return True
        except:
            return False

    def _test_query(self) -> bool:
        """쿼리 테스트"""
        try:
            db_id = self.db_ids.get('keyword_analysis')
            response = self.notion_db._query_database(db_id)
            return 'results' in response
        except:
            return False

    def _test_update(self) -> bool:
        """업데이트 테스트"""
        try:
            db_id = self.db_ids.get('keyword_analysis')
            response = self.notion_db._query_database(db_id)

            if response.get('results'):
                page_id = response['results'][0]['id']
                self.notion_db._update_page(page_id, {
                    "Status": {"select": {"name": "active"}}
                })
                return True
        except:
            return False

    def generate_report(self) -> str:
        """검증 리포트 생성"""
        report = f"""
{'='*60}
  📋 Database Validation Report
{'='*60}

생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Validation Results:
{'-'*60}

"""
        for db_name, result in self.results.items():
            status = "✅" if result.get('status', False) else "❌"
            report += f"\n{status} {db_name.upper()}\n"

            if result.get('status', False):
                report += f"   Database ID: {result.get('db_id', 'N/A')}\n"
                report += f"   Total Pages: {result.get('total_pages', 0)}\n"
                report += f"   Properties: {result.get('properties', 0)}\n"
            else:
                report += f"   Error: {result.get('error', 'Unknown')}\n"

        report += f"""
{'='*60}

✅ 검증 완료!

다음 단계:
1. 프론트엔드 실행: npm run dev
2. 백엔드 실행: python -m uvicorn backend:app --reload
3. 브라우저: http://localhost:3000

{'='*60}

"""
        return report


def main():
    parser = argparse.ArgumentParser(
        description='Database Validation & Testing Script'
    )

    parser.add_argument(
        '--config',
        default='.env.local',
        help='Configuration file path'
    )
    parser.add_argument(
        '--test-api',
        action='store_true',
        help='Run API operation tests'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Run full validation including API tests'
    )

    args = parser.parse_args()

    # 환경 변수 로드
    if not os.path.exists(args.config):
        print(f"❌ Config file not found: {args.config}")
        sys.exit(1)

    load_dotenv(args.config)

    api_token = os.getenv('NOTION_API_TOKEN')
    db_ids = {
        'keyword_analysis': os.getenv('NOTION_DB_KEYWORD_ANALYSIS'),
        'trend_data': os.getenv('NOTION_DB_TREND_DATA'),
        'recommendations': os.getenv('NOTION_DB_RECOMMENDATIONS'),
        'competitor_analysis': os.getenv('NOTION_DB_COMPETITOR'),
        'search_intent': os.getenv('NOTION_DB_INTENT'),
        'performance_prediction': os.getenv('NOTION_DB_PREDICTION')
    }

    if not api_token:
        print("❌ NOTION_API_TOKEN not found")
        sys.exit(1)

    # Validator 생성
    validator = DatabaseValidator(api_token, db_ids)

    # 기본 검증
    basic_ok = validator.validate_all()

    # API 테스트 (선택사항)
    if args.test_api or args.full:
        api_ok = validator.test_api_operations()
    else:
        api_ok = True

    # 리포트 생성
    report = validator.generate_report()
    print(report)

    # 리포트 저장
    with open('validation_report.txt', 'w') as f:
        f.write(report)

    print("📄 Report saved to validation_report.txt")

    # 종료 코드
    sys.exit(0 if (basic_ok and api_ok) else 1)


if __name__ == "__main__":
    main()
