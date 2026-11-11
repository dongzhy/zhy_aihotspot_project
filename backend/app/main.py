from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes import hotspots

app = FastAPI(
    title="AI 热点话题监测看板",
    description="基于 OpenRouter AI 的热点话题监测与分析系统",
    version="1.0.0",
)

# CORS 配置，允许前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(hotspots.router)


@app.get("/")
async def root():
    return {
        "message": "AI 热点话题监测看板 API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)