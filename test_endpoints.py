import urllib.request
import json

base = "http://localhost:8000"

def get(path):
    resp = urllib.request.urlopen(base + path, timeout=5)
    return json.loads(resp.read().decode())

print("=== 测试热点列表 ===")
data = get("/api/hotspots")
print("总数:", data["total"])
for item in data["items"][:5]:
    print("  #%d %s - 热度: %.1f - %s - %s" % (item["id"], item["title"], item["heat_score"], item["category"], item["source"]))

print("\n=== 测试趋势数据 ===")
data = get("/api/trends")
for d in data:
    print("  %s: 热度=%.1f, 话题数=%d" % (d["date"], d["heat_score"], d["topic_count"]))

print("\n=== 测试分类统计 ===")
data = get("/api/categories")
for d in data:
    print("  %s: %d 个话题, 平均热度=%.1f" % (d["category"], d["count"], d["avg_heat"]))

print("\n=== 测试单个热点详情 ===")
data = get("/api/hotspots/1")
print("标题:", data["title"])
print("类别:", data["category"])
print("情感:", data.get("sentiment", "未分析"))

print("\n=== 测试每日报告 ===")
data = get("/api/report/daily")
report = data.get("report", "")
print("报告长度:", len(report), "字符")
print("前200字:", report[:200])

print("\n=== 测试 POST 分析 ===")
import urllib.parse
payload = json.dumps({"text": "人工智能技术发展迅速", "topic": "人工智能"}).encode("utf-8")
req = urllib.request.Request(
    base + "/api/analyze",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
resp = urllib.request.urlopen(req, timeout=15)
result = json.loads(resp.read().decode())
print("情感:", result.get("sentiment"))
print("得分:", result.get("sentiment_score"))
print("摘要:", result.get("summary", "")[:80])
print("关键词:", result.get("keywords", []))

print("\n=== 测试热点 AI 分析 ===")
req = urllib.request.Request(
    base + "/api/hotspots/1/analyze",
    data=b"",
    method="POST",
)
resp = urllib.request.urlopen(req, timeout=15)
result = json.loads(resp.read().decode())
print("热点ID:", result.get("hotspot_id"))
analysis = result.get("analysis", {})
print("情感:", analysis.get("sentiment"))
print("得分:", analysis.get("sentiment_score"))

print("\n=== 所有测试通过！ ===")