import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from backend.app.models import HotspotResponse, TrendDataPoint, CategoryStat


class DataService:
    """模拟数据服务（后续可替换为真实数据源）"""

    CATEGORIES = ["科技", "娱乐", "体育", "财经", "社会", "健康", "教育", "旅游"]

    MOCK_TOPICS = [
        "人工智能大模型新突破",
        "电动车补贴政策调整",
        "春节旅游预订火爆",
        "新冠疫情最新动态",
        "股市波动与投资建议",
        "电影春节档票房",
        "冬季流感高发预警",
        "元宇宙概念降温",
        "半导体产业链",
        "双十一购物节预热",
    ]

    def __init__(self):
        self.hotspots: List[Dict[str, Any]] = []
        self._init_mock_data()

    def _init_mock_data(self):
        """初始化模拟热点数据"""
        for i, topic in enumerate(self.MOCK_TOPICS):
            self.hotspots.append(
                {
                    "id": i + 1,
                    "title": topic,
                    "category": random.choice(self.CATEGORIES),
                    "heat_score": round(random.uniform(60, 98), 1),
                    "source": random.choice(["微博", "新闻", "抖音", "朋友圈", "知乎"]),
                    "url": f"https://example.com/topic/{i+1}",
                    "created_at": (datetime.now() - timedelta(hours=random.randint(0, 48))).isoformat(),
                    "sentiment": random.choice(["positive", "neutral", "negative"]),
                    "sentiment_score": round(random.uniform(-1, 1), 2),
                    "ai_summary": f"{topic} 相关讨论度较高，公众关注度上升。",
                }
            )

    def get_all_hotspots(self) -> List[Dict[str, Any]]:
        return sorted(self.hotspots, key=lambda x: x["heat_score"], reverse=True)

    def get_hotspot_by_id(self, hotspot_id: int) -> Optional[Dict[str, Any]]:
        for h in self.hotspots:
            if h["id"] == hotspot_id:
                return h
        return None

    def get_trend_data(self) -> List[TrendDataPoint]:
        """生成过去 7 天的趋势数据"""
        data = []
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            data.append(
                TrendDataPoint(
                    date=date,
                    heat_score=round(random.uniform(50, 90), 1),
                    topic_count=random.randint(5, 20),
                )
            )
        return data

    def get_category_stats(self) -> List[CategoryStat]:
        """按分类统计热点"""
        stats = []
        for cat in self.CATEGORIES:
            cat_hotspots = [h for h in self.hotspots if h["category"] == cat]
            if cat_hotspots:
                stats.append(
                    CategoryStat(
                        category=cat,
                        count=len(cat_hotspots),
                        avg_heat=round(
                            sum(h["heat_score"] for h in cat_hotspots)
                            / len(cat_hotspots),
                            1,
                        ),
                    )
                )
        return stats


# 单例实例
data_service = DataService()