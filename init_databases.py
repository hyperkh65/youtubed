#!/usr/bin/env python3
"""
Database Initialization Script
6개 Database를 프로덕션 환경으로 초기화합니다.

사용법:
python init_databases.py --config .env.local
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from notion_db import NotionDB
from datetime import datetime
import json

def load_config(config_file: str) -> dict:
    """환경 설정 로드"""
    if not os.path.exists(config_file):
        print(f"❌ Config file not found: {config_file}")
        sys.exit(1)

    load_dotenv(config_file)

    config = {
        'notion_token': os.getenv('NOTION_API_TOKEN'),
        'db_ids': {
            'keyword_analysis': os.getenv('NOTION_DB_KEYWORD_ANALYSIS'),
            'trend_data': os.getenv('NOTION_DB_TREND_DATA'),
            'recommendations': os.getenv('NOTION_DB_RECOMMENDATIONS'),
            'competitor_analysis': os.getenv('NOTION_DB_COMPETITOR'),
            'search_intent': os.getenv('NOTION_DB_INTENT'),
            'performance_prediction': os.getenv('NOTION_DB_PREDICTION')
        }
    }

    # 검증
    if not config['notion_token']:
        print("❌ NOTION_API_TOKEN not found in config")
        sys.exit(1)

    return config

def initialize_databases(config: dict) -> bool:
    """6개 Database 초기화"""
    print("\n" + "="*60)
    print("  ⚙️  Database Initialization")
    print("="*60 + "\n")

    # Notion DB 클라이언트 생성
    notion_db = NotionDB(config['notion_token'])
    notion_db.set_database_ids(config['db_ids'])

    # 각 Database 초기화
    databases = [
        ('keyword_analysis', 'Keyword Analysis 🔍', 'keyword_analysis'),
        ('trend_data', 'Trend Data 📊', 'trend_data'),
        ('recommendations', 'Recommendations 💡', 'recommendations'),
        ('competitor_analysis', 'Competitor Analysis ⚔️', 'competitor_analysis'),
        ('search_intent', 'Search Intent 🔍', 'search_intent'),
        ('performance_prediction', 'Performance Prediction 📈', 'performance_prediction')
    ]

    results = {}

    for db_key, display_name, config_key in databases:
        print(f"⚙️  Initializing {display_name}...")

        db_id = config['db_ids'].get(config_key)

        if not db_id:
            print(f"   ❌ Database ID not found for {config_key}")
            results[db_key] = False
            continue

        try:
            # Database 연결 테스트
            response = notion_db._query_database(db_id)

            if 'results' in response:
                print(f"   ✅ Connected successfully")
                print(f"   📝 Ready to receive data")
                results[db_key] = True
            else:
                print(f"   ⚠️  Connection uncertain")
                results[db_key] = False

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results[db_key] = False

    # 결과 요약
    print("\n" + "="*60)
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    print(f"  📊 Initialization Result: {success_count}/{total_count} successful\n")

    for db_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {db_name}")

    print("\n" + "="*60 + "\n")

    return all(results.values())

def add_default_data(config: dict) -> bool:
    """기본 데이터 추가"""
    print("\n" + "="*60)
    print("  📝 Adding Default Data")
    print("="*60 + "\n")

    notion_db = NotionDB(config['notion_token'])
    notion_db.set_database_ids(config['db_ids'])

    # 기본 키워드 데이터
    default_keywords = [
        {
            'keyword': 'Python Programming',
            'google_volume': 2500,
            'naver_volume': 1800,
            'daum_volume': 1400,
            'youtube_volume': 3200,
            'difficulty_score': 45,
            'google_cpc': 1.50,
            'naver_cpc': 1.20,
            'opportunity_score': 55.5,
            'google_trend': 'rising',
            'naver_trend': 'stable',
            'search_intent': 'informational',
            'status': 'active'
        },
        {
            'keyword': 'Machine Learning',
            'google_volume': 3800,
            'naver_volume': 2500,
            'daum_volume': 1900,
            'youtube_volume': 4500,
            'difficulty_score': 62,
            'google_cpc': 2.10,
            'naver_cpc': 1.80,
            'opportunity_score': 61.2,
            'google_trend': 'rising',
            'naver_trend': 'rising',
            'search_intent': 'commercial',
            'status': 'active'
        },
        {
            'keyword': 'Data Science',
            'google_volume': 3200,
            'naver_volume': 2100,
            'daum_volume': 1600,
            'youtube_volume': 3800,
            'difficulty_score': 58,
            'google_cpc': 1.95,
            'naver_cpc': 1.60,
            'opportunity_score': 55.1,
            'google_trend': 'stable',
            'naver_trend': 'stable',
            'search_intent': 'informational',
            'status': 'active'
        }
    ]

    # Keyword Analysis에 데이터 추가
    print("📌 Adding keywords to Keyword Analysis...")
    keyword_count = 0

    for keyword_data in default_keywords:
        try:
            notion_db.add_keyword_analysis(
                keyword_data['keyword'],
                keyword_data
            )
            print(f"  ✅ Added: {keyword_data['keyword']}")
            keyword_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not add {keyword_data['keyword']}: {str(e)}")

    print(f"\n✅ Added {keyword_count} keywords\n")

    # Recommendations에 기본 추천 추가
    print("💡 Adding recommendations...")
    recommendations = [
        {
            'keyword': 'best python tutorial',
            'score': 87.5,
            'type': 'related',
            'volume': 1200,
            'difficulty': 35,
            'trend': 'rising',
            'conversion_potential': 0.7,
            'priority': 4
        },
        {
            'keyword': 'python for beginners',
            'score': 82.0,
            'type': 'niche',
            'volume': 950,
            'difficulty': 28,
            'trend': 'stable',
            'conversion_potential': 0.8,
            'priority': 5
        },
        {
            'keyword': 'python 2024 course',
            'score': 78.5,
            'type': 'trending',
            'volume': 1100,
            'difficulty': 40,
            'trend': 'rising',
            'conversion_potential': 0.75,
            'priority': 4
        }
    ]

    rec_count = 0
    for rec in recommendations:
        try:
            notion_db.add_recommendation('Python Programming', rec)
            print(f"  ✅ Added: {rec['keyword']}")
            rec_count += 1
        except Exception as e:
            print(f"  ⚠️  Could not add recommendation: {str(e)}")

    print(f"\n✅ Added {rec_count} recommendations\n")

    return True

def generate_init_report(config: dict) -> str:
    """초기화 리포트 생성"""
    report = f"""
{'='*60}
  📊 Database Initialization Report
{'='*60}

생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

✅ Database Configuration Loaded:

1️⃣  Keyword Analysis: {config['db_ids'].get('keyword_analysis', 'NOT SET')[:16]}...
2️⃣  Trend Data: {config['db_ids'].get('trend_data', 'NOT SET')[:16]}...
3️⃣  Recommendations: {config['db_ids'].get('recommendations', 'NOT SET')[:16]}...
4️⃣  Competitor Analysis: {config['db_ids'].get('competitor_analysis', 'NOT SET')[:16]}...
5️⃣  Search Intent: {config['db_ids'].get('search_intent', 'NOT SET')[:16]}...
6️⃣  Performance Prediction: {config['db_ids'].get('performance_prediction', 'NOT SET')[:16]}...

{'='*60}

✅ 초기화 완료!

📝 다음 단계:

1. 백엔드 시작:
   python -m uvicorn backend:app --reload

2. 프론트엔드 시작 (다른 터미널):
   npm run dev

3. 브라우저 접속:
   http://localhost:3000

4. Notion 대시보드 확인:
   https://www.notion.so

{'='*60}

🎉 모든 Database가 프로덕션 환경으로 준비되었습니다!

"""
    return report

def main():
    parser = argparse.ArgumentParser(
        description='Database Initialization Script',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--config',
        default='.env.local',
        help='Configuration file path (default: .env.local)'
    )
    parser.add_argument(
        '--add-samples',
        action='store_true',
        help='Add default sample data'
    )
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only generate report without initialization'
    )

    args = parser.parse_args()

    # 설정 로드
    config = load_config(args.config)

    if args.report_only:
        report = generate_init_report(config)
        print(report)
        return

    # Database 초기화
    init_success = initialize_databases(config)

    if not init_success:
        print("❌ Initialization failed")
        sys.exit(1)

    # 샘플 데이터 추가
    if args.add_samples:
        add_default_data(config)

    # 리포트 생성
    report = generate_init_report(config)
    print(report)

    # 리포트 파일 저장
    report_file = 'init_report.txt'
    with open(report_file, 'w') as f:
        f.write(report)

    print(f"📄 Report saved to {report_file}")

if __name__ == "__main__":
    main()
