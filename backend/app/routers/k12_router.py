# 兼容转发：router 对象统一在 app/routers/k12.py 定义（见 routers/__init__.py）
from app.routers.k12 import router  # noqa: F401
