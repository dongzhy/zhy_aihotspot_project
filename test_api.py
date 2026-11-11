"""API 测试脚本"""
import subprocess
import sys
import time
import urllib.request
import json
import signal
import os

PYTHON = r"c:\users\15922\appdata\local\programs\python\python38\python.exe"

def start_server():
    """启动后端服务器"""
    proc = subprocess.Popen(
        [PYTHON, "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        cwd=r"e:\ai_project",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    # 等待服务器启动
    time.sleep(3)
    return proc

def test_endpoint(path):
    """测试单个端点"""
    try:
        resp = urllib.request.urlopen(f"http://localhost:8000{path}", timeout=5)
        data = json.loads(resp.read().decode())
        return True, data
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("AI 热点话题监测看板 - API 测试")
    print("=" * 60)

    proc = start_server()

    try:
        endpoints = [
            ("GET", "/", "根路径"),
            ("GET", "/health", "健康检查"),
            ("GET", "/api/hotspots", "获取热点列表"),
            ("GET", "/api/trends", "获取趋势数据"),
            ("GET", "/api/categories", "获取分类统计"),
            ("GET", "/api/hotspots/1", "获取单个热点详情"),
            ("GET", "/api/report/daily", "生成每日 AI 报告"),
        ]

        all_passed = True
        for method, path, desc in endpoints:
            success, result = test_endpoint(path)
            status = "✓ 通过" if success else "✗ 失败"
            print(f"{status} {desc} ({method} {path})")
            if not success:
                print(f"   错误: {result}")
                all_passed = False
            else:
                # 显示简要信息
                if isinstance(result, dict):
                    if "items" in result:
                        print(f"   热点数量: {result.get('total', 0)}")
                    elif "report" in result:
                        print(f"   报告长度: {len(str(result.get('report', '')))} 字符")
                    elif "status" in result:
                        print(f"   状态: {result.get('status')}")
                    else:
                        print(f"   响应键: {list(result.keys())[:5]}")

        # 测试 POST 分析端点
        print(f"\n{'=' * 60}")
        print("测试 POST /api/analyze (OpenRouter AI 分析)")
        print(f"{'=' * 60}")
        try:
            data = json.dumps({"text": "人工智能技术发展迅速", "topic": "人工智能"}).encode("utf-8")
            req = urllib.request.Request(
                "http://localhost:8000/api/analyze",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.loads(resp.read().decode())
            print(f"✓ 通过 POST /api/analyze")
            print(f"   情感: {result.get('sentiment')}, 得分: {result.get('sentiment_score')}")
            print(f"   摘要: {result.get('summary', '')[:50]}...")
        except Exception as e:
            print(f"✗ 失败 POST /api/analyze: {e}")
            all_passed = False

        # 测试热点 AI 分析
        print(f"\n{'=' * 60}")
        print("测试 POST /api/hotspots/{id}/analyze")
        print(f"{'=' * 60}")
        try:
            req = urllib.request.Request(
                "http://localhost:8000/api/hotspots/1/analyze",
                data=b"",
                method="POST",
            )
            resp = urllib.request.urlopen(req, timeout=10)
            result = json.loads(resp.read().decode())
            print(f"✓ 通过 POST /api/hotspots/1/analyze")
            print(f"   分析结果: {result.get('analysis', {}).get('sentiment', 'N/A')}")
        except Exception as e:
            print(f"✗ 失败 POST /api/hotspots/1/analyze: {e}")
            all_passed = False

        print(f"\n{'=' * 60}")
        if all_passed:
            print("🎉 所有 API 测试通过！")
        else:
            print("⚠️  部分测试失败，请检查错误信息")
        print(f"{'=' * 60}")

    finally:
        proc.terminate()
        proc.wait()
        print("\n服务器已停止")

if __name__ == "__main__":
    main()