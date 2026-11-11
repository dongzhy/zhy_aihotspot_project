import sys
sys.path.insert(0, '.')
from app.main import app
print("模块导入成功")
print("路由数量:", len(app.routes))