"""
FastAPI Backend for Keyword Analysis
Keyword Analyzer와 Notion DB를 연동하는 백엔드
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from keyword_analyzer import AdvancedKeywordAnalyzer, AdvancedKeywordDataExporter
from notion_db import NotionDB

# FastAPI 앱 초기화
app = FastAPI(
    title="YouTube Keyword Analyzer API",
    description="Advanced keyword analysis with Notion integration",
    version="2.0.0"
)

# CORS 설정 (Vercel 프론트엔드 접근 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 초기화
analyzer = AdvancedKeywordAnalyzer()
exporter = AdvancedKeywordDataExporter()

# Notion DB 초기화
NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN", "ntn_T84053591181vVGMJGrESxdEGryJX6sO9EZIeeQ4OzS2YJ")
notion_db = NotionDB(NOTION_API_TOKEN)

# 사용자가 설정해야 할 Database IDs
DB_IDS = {
    'keyword_analysis': os.getenv("NOTION_DB_KEYWORD_ANALYSIS", ""),
    'trend_data': os.getenv("NOTION_DB_TREND_DATA", ""),
    'recommendations': os.getenv("NOTION_DB_RECOMMENDATIONS", ""),
    'competitor_analysis': os.getenv("NOTION_DB_COMPETITOR", ""),
    'search_intent': os.getenv("NOTION_DB_INTENT", ""),
    'performance_prediction': os.getenv("NOTION_DB_PREDICTION", "")
}

notion_db.set_database_ids(DB_IDS)

# ==================== Pydantic Models ====================

class KeywordAnalysisRequest(BaseModel):
    keyword: str

class MultiKeywordRequest(BaseModel):
    keywords: List[str]
    channel_topic: Optional[str] = None

class RecommendationsRequest(BaseModel):
    keywords: List[str]
    channel_topic: Optional[str] = None

class CompetitorRequest(BaseModel):
    competitor_keywords: List[str]
    your_keywords: List[str]

class TrendRequest(BaseModel):
    keyword: str
    days: int = 30

class PredictionRequest(BaseModel):
    keyword: str
    months: int = 3

# ==================== API Routes ====================

@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "notion_connected": bool(DB_IDS['keyword_analysis'])
    }

# ==================== Keyword Analysis ====================

@app.post("/api/analyze")
async def analyze_keyword(request: KeywordAnalysisRequest):
    """
    단일 키워드 다중 포털 분석
    """
    try:
        keyword = request.keyword.strip()

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        # 분석 실행
        result = analyzer.analyze_multi_portal(keyword)

        # Notion에 저장 (백그라운드)
        save_to_notion_background(keyword, result)

        return {
            "success": True,
            "keyword": keyword,
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/compare")
async def compare_keywords(request: MultiKeywordRequest):
    """
    여러 키워드 비교 분석
    """
    try:
        keywords = [kw.strip() for kw in request.keywords if kw.strip()]

        if not keywords:
            raise HTTPException(status_code=400, detail="Keywords cannot be empty")

        if len(keywords) > 5:
            keywords = keywords[:5]

        # 비교 분석 실행
        comparison_df = analyzer.compare_keywords(keywords)

        # DataFrame을 딕셔너리로 변환
        result = {
            "keywords": keywords,
            "comparison": comparison_df.to_dict('records'),
            "timestamp": datetime.now().isoformat()
        }

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

# ==================== Advanced Features ====================

@app.post("/api/short-long-analysis")
async def analyze_short_long(request: KeywordAnalysisRequest):
    """
    숏/롱테일 키워드 분석
    """
    try:
        keyword = request.keyword.strip()

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        result = analyzer.analyze_short_long_keywords(keyword)

        return {
            "success": True,
            "keyword": keyword,
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationsRequest):
    """
    실시간 키워드 추천
    """
    try:
        keywords = [kw.strip() for kw in request.keywords if kw.strip()]

        if not keywords:
            raise HTTPException(status_code=400, detail="Keywords cannot be empty")

        recommendations = analyzer.get_realtime_recommendations(
            keywords,
            request.channel_topic or ""
        )

        # Notion에 저장 (백그라운드)
        for rec in recommendations:
            save_recommendation_to_notion(keywords[0], rec)

        return {
            "success": True,
            "base_keywords": keywords,
            "recommendations": recommendations,
            "count": len(recommendations),
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")

@app.post("/api/competitor-analysis")
async def analyze_competitors(request: CompetitorRequest):
    """
    경쟁사 키워드 분석
    """
    try:
        result = analyzer.analyze_competitor_keywords(
            request.competitor_keywords,
            request.your_keywords
        )

        return {
            "success": True,
            "analysis": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/search-intent")
async def analyze_intent(request: KeywordAnalysisRequest):
    """
    검색 의도 분석
    """
    try:
        keyword = request.keyword.strip()

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        result = analyzer.analyze_search_intent(keyword)

        return {
            "success": True,
            "keyword": keyword,
            "intent_analysis": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ==================== Performance & Trends ====================

@app.post("/api/trend-analysis")
async def analyze_trends(request: TrendRequest):
    """
    트렌드 분석 (N일간)
    """
    try:
        keyword = request.keyword.strip()
        days = max(7, min(90, request.days))  # 7-90일 범위

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        result = analyzer.get_trend_analysis(keyword, days)

        return {
            "success": True,
            "keyword": keyword,
            "days": days,
            "trend_analysis": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/seasonality")
async def detect_seasonality(request: KeywordAnalysisRequest):
    """
    계절성 패턴 감지 (365일)
    """
    try:
        keyword = request.keyword.strip()

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        result = analyzer.detect_seasonality(keyword, days=365)

        return {
            "success": True,
            "keyword": keyword,
            "seasonality": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/prediction")
async def predict_performance(request: PredictionRequest):
    """
    3개월 성능 예측
    """
    try:
        keyword = request.keyword.strip()
        months = max(1, min(6, request.months))  # 1-6개월 범위

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        result = analyzer.predict_keyword_performance(keyword, months)

        return {
            "success": True,
            "keyword": keyword,
            "months": months,
            "prediction": result,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# ==================== 데이터 내보내기 ====================

@app.post("/api/export")
async def export_analysis(request: KeywordAnalysisRequest):
    """
    분석 결과 내보내기 (JSON)
    """
    try:
        keyword = request.keyword.strip()

        if not keyword:
            raise HTTPException(status_code=400, detail="Keyword cannot be empty")

        analysis = analyzer.analyze_multi_portal(keyword)

        # 파일로 내보내기
        filename = f"analysis_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        exporter.export_to_json(analysis, filename)

        return {
            "success": True,
            "keyword": keyword,
            "filename": filename,
            "message": f"Analysis exported to {filename}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# ==================== Notion 동기화 헬퍼 ====================

def save_to_notion_background(keyword: str, analysis_result: dict):
    """Notion DB에 분석 결과 저장"""
    try:
        analysis_data = {
            'google_volume': analysis_result['portals'].get('Google', {}).get('estimated_search_volume', 0),
            'naver_volume': analysis_result['portals'].get('Naver', {}).get('estimated_search_volume', 0),
            'daum_volume': analysis_result['portals'].get('Daum', {}).get('estimated_search_volume', 0),
            'youtube_volume': analysis_result['portals'].get('YouTube', {}).get('estimated_search_volume', 0),
            'difficulty_score': analysis_result['portals'].get('Google', {}).get('keyword_difficulty_score', 0),
            'google_cpc': analysis_result['portals'].get('Google', {}).get('cpc', 0),
            'opportunity_score': analysis_result['portals'].get('Google', {}).get('opportunity_score', 0),
            'google_trend': analysis_result['portals'].get('Google', {}).get('trend', 'stable'),
            'search_intent': analysis_result['portals'].get('Google', {}).get('search_intent', {}).get('primary_intent', 'informational'),
            'status': 'active'
        }

        notion_db.sync_keyword_analysis(keyword, analysis_data)
    except Exception as e:
        print(f"Error saving to Notion: {str(e)}")

def save_recommendation_to_notion(base_keyword: str, recommendation: dict):
    """Notion DB에 추천 키워드 저장"""
    try:
        notion_db.add_recommendation(base_keyword, recommendation)
    except Exception as e:
        print(f"Error saving recommendation to Notion: {str(e)}")

# ==================== Root ====================

@app.get("/")
async def root():
    """API 루트"""
    return {
        "name": "YouTube Keyword Analyzer API",
        "version": "2.0.0",
        "docs_url": "/docs",
        "notion_integration": "enabled" if DB_IDS['keyword_analysis'] else "disabled"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
