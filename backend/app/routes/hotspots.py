from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from backend.app.models import (
    HotspotResponse,
    HotspotList,
    AIAnalysisRequest,
    AIAnalysisResponse,
    TrendDataPoint,
    CategoryStat,
)
from backend.app.services.data_service import data_service
from backend.app.services.openrouter import openrouter_service

router = APIRouter(prefix="/api")


@router.get("/hotspots", response_model=HotspotList)
async def get_hotspots():
    """获取所有热点话题"""
    items = data_service.get_all_hotspots()
    return HotspotList(items=items, total=len(items))


@router.get("/hotspots/{hotspot_id}", response_model=HotspotResponse)
async def get_hotspot(hotspot_id: int):
    """获取单个热点详情"""
    hotspot = data_service.get_hotspot_by_id(hotspot_id)
    if not hotspot:
        raise HTTPException(status_code=404, detail="热点话题不存在")
    return hotspot


@router.post("/analyze", response_model=AIAnalysisResponse)
async def analyze_text(request: AIAnalysisRequest):
    """使用 OpenRouter AI 分析文本情感和摘要"""
    result = await openrouter_service.analyze_sentiment_and_summary(
        text=request.text, topic=request.topic
    )
    return AIAnalysisResponse(**result)


@router.get("/trends", response_model=List[TrendDataPoint])
async def get_trends():
    """获取热度趋势数据"""
    return data_service.get_trend_data()


@router.get("/categories", response_model=List[CategoryStat])
async def get_category_stats():
    """获取分类统计数据"""
    return data_service.get_category_stats()


@router.get("/report/daily")
async def get_daily_report():
    """生成每日 AI 洞察报告"""
    hotspots = data_service.get_all_hotspots()
    report = await openrouter_service.generate_daily_report(hotspots)
    return {"report": report, "generated_at": __import__("datetime").datetime.now().isoformat()}


@router.post("/hotspots/{hotspot_id}/analyze")
async def analyze_hotspot(hotspot_id: int):
    """对特定热点进行 AI 深度分析"""
    hotspot = data_service.get_hotspot_by_id(hotspot_id)
    if not hotspot:
        raise HTTPException(status_code=404, detail="热点话题不存在")

    result = await openrouter_service.analyze_sentiment_and_summary(
        text=hotspot.get("ai_summary", hotspot["title"]), topic=hotspot["title"]
    )

    # 更新热点数据
    hotspot["sentiment"] = result.get("sentiment")
    hotspot["sentiment_score"] = result.get("sentiment_score")
    hotspot["ai_summary"] = result.get("summary")

    return {
        "hotspot_id": hotspot_id,
        "analysis": result,
    }