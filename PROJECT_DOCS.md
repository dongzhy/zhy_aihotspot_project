# AI 热点话题监测看板 - 项目文档

## 1. 项目概述

### 1.1 项目名称
AI 热点话题监测看板（AI Hotspot Radar Dashboard）

### 1.2 项目目标
构建一个基于 OpenRouter AI 的热点话题监测与分析系统，实现：
- 实时监测互联网热点话题
- AI 驱动的情感倾向分析
- 热度趋势可视化
- 每日 AI 洞察报告生成

### 1.3 核心特色
- **独特前端设计**：玻璃拟态（Glassmorphism）+ 动态渐变背景 + 深色主题
- **OpenRouter AI 接入**：支持多模型 AI 分析，无 API Key 时自动降级为模拟数据
- **前后端分离**：FastAPI 后端 + 原生 JavaScript 前端
## 2. 架构设计

### 2.1 技术栈

| 层级 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 前端 | HTML5 + Tailwind CSS + Vanilla JS + Chart.js | - | 玻璃拟态 UI，响应式布局 |
| 后端 | Python + FastAPI | 3.8+ | 轻量级 REST API |
| AI 服务 | OpenRouter | - | GPT-3.5/4 等多模型支持 |
| 数据 | 模拟数据（可扩展） | - | 后续可接入真实 API |

### 2.2 系统架构图

```
┌─────────────────────────────────────────────────────────┐
│                    前端页面 (frontend/)                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │ 热点列表     │  │ 热度趋势图  │  │ 分类分布图  │    │
│  │ 情感标签     │  │ Chart.js    │  │ 环形图      │    │
│  │ AI 报告模态  │  │ 响应式布局   │  │ 玻璃拟态    │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   后端 API (backend/app/)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
## 3. 项目结构

```
e:\ai_project\
├── .env.example                    # 环境变量配置模板
├── requirements.txt                # Python 依赖列表
├── start.bat                       # 后端启动脚本
├── test_api.py                     # 综合 API 测试脚本
├── test_endpoints.py               # 端点详细测试脚本
├── PROJECT_DOCS.md                 # 项目文档 (本文件)
│
├── backend\
│   └── app\
│       ├── __init__.py
│       ├── main.py                 # FastAPI 主入口 (CORS, 路由注册)
│       ├── models.py               # Pydantic 数据模型
│       ├── routes\
│       │   └── hotspots.py         # API 路由定义
│       └── services\
│           ├── data_service.py     # 模拟数据服务 (DataService)
│           └── openrouter.py       # OpenRouter AI 服务
│
├── frontend\
│   ├── index.html                  # 前端主页面
│   ├── css\
│   │   └── style.css               # 自定义样式 (玻璃拟态、动画)
│   └── js\
## 4. 功能模块

### 4.1 热点雷达 (Hotspot Radar)
- 显示实时热点话题列表
- 每个话题显示：标题、分类、热度得分 (0-100)、数据来源、情感标签
- 热度条可视化显示
- 点击话题可查看 AI 深度分析

### 4.2 热度趋势图 (Trend Chart)
- 过去 7 天热度变化折线图
- Chart.js 渲染，支持悬停提示
- 动态数据更新

### 4.3 分类分布 (Category Distribution)
- 话题分类环形图 (Doughnut Chart)
- 显示各分类的话题数量
- 不同颜色区分分类

### 4.4 AI 情感分析 (AI Sentiment Analysis)
- 调用 OpenRouter 分析文本情感倾向
- 返回：情感 (positive/neutral/negative)、情感得分 (-1 到 1)、摘要、关键词、预测
- 支持单条文本分析和热点深度分析

### 4.5 每日 AI 洞察报告 (Daily AI Report)
- 生成 Markdown 格式的每日报告
- 包含：热点总览、情感分布、重点话题解读、趋势预测、建议关注方向
- 模态框展示

### 4.6 统计看板 (Stats Dashboard)
- 监测热点总数
- 平均热度得分
## 5. API 接口文档

### 5.1 基础信息
- **基础 URL**: `http://localhost:8000`
- **API 文档**: `http://localhost:8000/docs` (Swagger UI)
- **健康检查**: `GET /health`

### 5.2 接口列表

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 根路径 | GET | `/` | 欢迎信息 |
| 健康检查 | GET | `/health` | 服务状态 |
| 获取热点 | GET | `/api/hotspots` | 获取所有热点话题列表 |
| 热点详情 | GET | `/api/hotspots/{id}` | 获取单个热点详情 |
| 趋势数据 | GET | `/api/trends` | 获取 7 天热度趋势 |
| 分类统计 | GET | `/api/categories` | 获取分类统计数据 |
| 每日报告 | GET | `/api/report/daily` | 生成 AI 每日洞察报告 |
| 文本分析 | POST | `/api/analyze` | OpenRouter AI 分析文本 |
| 热点分析 | POST | `/api/hotspots/{id}/analyze` | 对特定热点进行 AI 深度分析 |

### 5.3 请求/响应示例

#### GET /api/hotspots
```json
{
  "items": [
    {
      "id": 1,
      "title": "人工智能大模型新突破",
      "category": "科技",
      "heat_score": 92.5,
      "source": "新闻",
      "sentiment": "positive",
      "sentiment_score": 0.48,
      "ai_summary": "AI 大模型技术取得重要进展...",
      "created_at": "2026-11-11T10:00:00"
    }
  ],
  "total": 10
}
## 6. 前端设计说明

### 6.1 设计理念
- **玻璃拟态 (Glassmorphism)**: 毛玻璃背景 + 半透明边框 + 背景模糊
- **深色主题**: Slate-900 基础色，减少视觉疲劳
- **动态渐变**: 6 个彩色模糊球体背景动画漂浮
- **渐变文字**: 主标题采用青紫粉三色渐变
- **响应式**: Grid 网格布局，适配移动端

### 6.2 页面布局
```
┌─────────────────────────────────────────────────────────┐
│  导航栏 (固定顶部)                                        │
│  [AI 热点雷达]  [系统运行中] [刷新数据]                    │
├─────────────────────────────────────────────────────────┤
│  欢迎标题                                                │
│  实时热点监测                                            │
├──────────────┬──────────────┬──────────────┬────────────┤
│  统计卡片     │  统计卡片     │  统计卡片     │  统计卡片   │
│  热点总数     │  平均热度     │  正面占比     │  AI 报告   │
├──────────────┴──────────────┴──────────────┴────────────┤
│  主内容区 (左 2/3)       │  图表区 (右 1/3)               │
│  热点话题列表             │  热度趋势图 (7天)              │
│  [卡片1] [卡片2] ...       │  分类分布图 (环形)             │
│                           │                                │
│  AI 报告模态框 (覆盖全屏)   │                                │
└─────────────────────────────────────────────────────────┘
```

### 6.3 交互功能
- 刷新数据按钮：手动重新加载所有接口
- 自动刷新：每 30 秒自动更新数据
- 点击热点卡片：弹出 AI 深度分析对话框
- 查看 AI 报告：打开模态框显示每日洞察报告
- 离线模式：后端未启动时显示友好提示
---
```

#### GET /api/trends
```json
[
## 7. OpenRouter AI 集成

### 7.1 配置
创建 `.env` 文件（基于 `.env.example`）：

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-3.5-turbo
```

### 7.2 服务类 (OpenRouterService)

**方法**: `analyze_sentiment_and_summary(text, topic)`
- 输入：待分析文本、话题标题
- 输出：情感、情感得分、摘要、关键词、预测
- 实现：调用 OpenRouter Chat Completions API

**方法**: `generate_daily_report(hotspots)`
- 输入：热点列表
- 输出：Markdown 格式每日报告
- 实现：基于热点数据生成专业分析报告

### 7.3 模拟降级机制
当 `OPENROUTER_API_KEY` 未配置或为默认值时，系统自动返回模拟数据：
- 情感：随机正面/中性/负面
- 摘要：固定模板文本
- 报告：固定 Markdown 模板

这确保了系统在没有 API Key 时也能正常运行和演示。
---
## 8. 部署与启动

### 8.1 环境要求
- Python 3.8+
- 现代浏览器 (支持 ES6+、Fetch API、CSS Grid)

### 8.2 安装依赖
```bash
cd e:\ai_project
pip install -r requirements.txt
```

### 8.3 启动后端
```bash
# 方式 1：双击运行
start.bat

# 方式 2：命令行
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 8.4 打开前端
直接在浏览器中打开：
```
e:\ai_project\frontend\index.html
```

### 8.5 访问地址
| 服务 | 地址 |
|------|------|
## 9. 测试报告

### 9.1 测试环境
- Python 3.8.2
- FastAPI 0.124.4
- Uvicorn 0.33.0
- Windows 11 / PowerShell

### 9.2 测试结果（全部通过 ✅）

| 测试项 | 端点 | 状态 | 备注 |
|--------|------|------|------|
| 健康检查 | GET /health | ✅ | {"status":"healthy"} |
| 热点列表 | GET /api/hotspots | ✅ | 返回 10 个热点 |
| 趋势数据 | GET /api/trends | ✅ | 返回 7 天数据 |
| 分类统计 | GET /api/categories | ✅ | 返回 5 个分类 |
| 热点详情 | GET /api/hotspots/1 | ✅ | 返回单个热点详情 |
| 每日报告 | GET /api/report/daily | ✅ | 287 字 Markdown 报告 |
| 文本分析 | POST /api/analyze | ✅ | 返回情感分析结果 |
| 热点深度分析 | POST /api/hotspots/1/analyze | ✅ | 返回 AI 分析 |

### 9.3 测试脚本
- `test_api.py`：综合测试 (启动服务 + 测试所有端点)
- `test_endpoints.py`：端点详细测试 (需服务已启动)
---
| 前端页面 | 浏览器打开 index.html |
| 后端 API | http://localhost:8000 |
| API 文档 | http://localhost:8000/docs |
---
  {"date": "2026-11-05", "heat_score": 60.9, "topic_count": 5},
  {"date": "2026-11-06", "heat_score": 54.3, "topic_count": 11}
## 10. 下一步：Agent Skills 开发计划

根据项目要求，网页版已完成并验收通过。接下来进入 Agent Skills 开发阶段：

### 10.1 计划中的 Agent Skills

| Skill | 说明 | 优先级 |
|-------|------|--------|
| 热点自动抓取 | 接入社交媒体/新闻 API 自动获取热点 | 高 |
| 定时报告推送 | 定时生成 AI 报告并推送 (邮件/钉钉/企业微信) | 高 |
| 内容创作建议 | 基于热点自动生成文章/视频脚本创意 | 中 |
| 多平台数据聚合 | 聚合微博、抖音、知乎、新闻等多源数据 | 中 |
| 情感趋势预测 | 基于历史数据预测热点未来走势 | 中 |
| 负面舆情预警 | 监测负面情感并实时预警 | 高 |

### 10.2 开发顺序
1. 数据源抓取 Skill
2. 定时报告生成 Skill
3. 负面舆情预警 Skill
4. 内容创作建议 Skill
---
]
```

#### POST /api/analyze
**请求体**:
```json
{
  "text": "人工智能技术发展迅速",
  "topic": "人工智能"
}
## 11. 备注

- 当前使用模拟数据，生产环境需接入真实数据源
- OpenRouter API Key 未配置时系统自动降级为模拟模式
- 前端为纯静态页面，可部署到任何静态托管服务 (GitHub Pages、Vercel 等)
- 后端支持 CORS，可跨域访问

---

**文档生成日期**: 2026-11-11  
**项目状态**: 网页版已完成，待开发 Agent Skills  
**维护者**: Cline AI 编程助手
```

**响应**:
```json
{
  "sentiment": "positive",
  "sentiment_score": 0.48,
  "summary": "【模拟分析】人工智能是当前关注的热点话题...",
  "keywords": ["人工智能", "热点", "趋势", "舆情"],
  "prediction": "预计未来 2-3 天热度将保持高位"
}
---
- 正面情感占比
- AI 报告生成状态
---
│       └── app.js                  # 前端逻辑 (API 调用、Chart.js 图表)
│
└── tests\                          # 测试目录 (预留)
---
│  │ 路由层       │  │ 模型层      │  │ 服务层      │    │
│  │ hotspots.py │  │ models.py   │  │ data_service│    │
│  │             │  │             │  │ openrouter  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    OpenRouter AI 服务                       │
│  - 情感分析 (analyze_sentiment_and_summary)              │
│  - 每日报告 (generate_daily_report)                       │
│  - 模拟降级 (无 API Key 时自动返回模拟数据)                │
└─────────────────────────────────────────────────────────┘
---
- **可扩展架构**：模块化设计，易于接入真实数据源和 Agent Skills

---