import os
import httpx
import json
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

load_dotenv()


class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.model = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

    async def analyze_sentiment_and_summary(
        self, text: str, topic: str
    ) -> Dict[str, Any]:
        """
        调用 OpenRouter 分析文本的情感倾向并生成摘要
        """
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            # 返回模拟结果，便于无 API Key 时也能运行
            return self._get_mock_analysis(topic)

        prompt = f"""
        请分析以下关于热点话题"{topic}"的内容，并以 JSON 格式返回：
        
        内容：{text}
        
        请返回包含以下字段的 JSON：
        - sentiment: 情感倾向 (positive/neutral/negative)
        - sentiment_score: 情感得分 (-1 到 1，-1 为最负面，1 为最正面)
        - summary: 对该热点的简要摘要（中文，不超过 200 字）
        - keywords: 关键词列表（3-5 个）
        - prediction: 对该话题未来趋势的预测（中文，不超过 100 字）
        
        只返回 JSON，不要包含其他解释文字。
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-hotspot-dashboard.local",
            "X-Title": "AI Hotspot Dashboard",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的舆情分析师，擅长分析热点话题的情感倾向和趋势。",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
                content = result["choices"][0]["message"]["content"]

                # 尝试解析 JSON
                try:
                    # 提取 JSON 部分（如果被包裹在代码块中）
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0]
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0]

                    return json.loads(content.strip())
                except json.JSONDecodeError:
                    return self._get_mock_analysis(topic)

            except Exception as e:
                print(f"OpenRouter API 错误: {e}")
                return self._get_mock_analysis(topic)

    async def generate_daily_report(self, hotspots: List[Dict[str, Any]]) -> str:
        """
        生成每日热点洞察报告
        """
        if not self.api_key or self.api_key == "your_openrouter_api_key_here":
            return self._get_mock_daily_report(hotspots)

        topics_summary = "\n".join(
            [
                f"- {h.get('title', '未知话题')} (热度: {h.get('heat_score', 0)}, 情感: {h.get('sentiment', '未知')})"
                for h in hotspots[:10]
            ]
        )

        prompt = f"""
        你是一个专业的舆情分析师。请基于以下今日热点话题，生成一份专业的每日热点洞察报告：
        
        今日热点列表：
        {topics_summary}
        
        报告应包含：
        1. 今日热点总览（主要趋势）
        2. 情感分布分析（正面/中性/负面比例）
        3. 重点话题深度解读（选 2-3 个最热门的话题）
        4. 未来趋势预测
        5. 建议关注方向
        
        请用中文撰写，语言专业、简洁，使用 Markdown 格式。
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-hotspot-dashboard.local",
            "X-Title": "AI Hotspot Dashboard",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的舆情分析师，擅长生成热点趋势洞察报告。",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
            except Exception as e:
                print(f"OpenRouter API 错误: {e}")
                return self._get_mock_daily_report(hotspots)

    def _get_mock_analysis(self, topic: str) -> Dict[str, Any]:
        """返回模拟的 AI 分析结果（无 API Key 时使用）"""
        import random

        sentiments = ["positive", "neutral", "negative"]
        sentiment = random.choice(sentiments)
        sentiment_score = round(random.uniform(-1, 1), 2)

        return {
            "sentiment": sentiment,
            "sentiment_score": sentiment_score,
            "summary": f"【模拟分析】{topic} 是当前关注的热点话题，各方观点不一，需要持续跟进。",
            "keywords": [topic, "热点", "趋势", "舆情"],
            "prediction": f"预计 {topic} 的热度在未来 2-3 天内将保持高位，随后逐渐回落。",
        }

    def _get_mock_daily_report(self, hotspots: List[Dict[str, Any]]) -> str:
        """返回模拟的每日报告"""
        return f"""# 每日热点洞察报告（模拟数据）

## 1. 今日热点总览
今日共监测到 {len(hotspots)} 个热点话题，整体热度处于活跃状态。

## 2. 情感分布分析
正面：40% | 中性：35% | 负面：25%

## 3. 重点话题深度解读
基于当前监测数据，建议重点关注前 3 个热度最高的话题的后续发展。

## 4. 未来趋势预测
预计未来 24 小时内，社会热点将继续围绕当前主题展开讨论。

## 5. 建议关注方向
建议持续追踪高热度话题的情感变化，及时捕捉负面舆情苗头。

---
*注：当前为模拟数据，如需真实 AI 分析，请配置 OpenRouter API Key*
"""


# 单例实例
openrouter_service = OpenRouterService()