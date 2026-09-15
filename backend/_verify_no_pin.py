"""验证：小孩无需密码（创建可无 PIN；登录无 PIN 放行；提供错误 PIN 仍拒绝）"""
import os
import sys
import tempfile

_tmp = tempfile.mktemp(suffix=".db")
os.environ["DB_PATH"] = _tmp
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import httpx

from app.database import Base, engine
from app.main import app

Base.metadata.create_all(bind=engine)


async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # admin 登录（默认密码 32167）
        r = await client.post("/api/auth/login", json={"username": "admin", "password": "32167"})
        print("admin login:", r.status_code)
        assert r.status_code == 200, r.text
        token = r.json()["token"]

        # 创建小孩（无 PIN）
        r = await client.post(
            "/api/users",
            json={"username": "kid_a", "role": "child", "display_name": "小明"},
            headers={"Authorization": f"Bearer {token}"},
        )
        print("create kid:", r.status_code, r.text[:120])
        assert r.status_code == 200, r.text

        # 小孩登录：不传 PIN -> 成功
        r = await client.post("/api/auth/login", json={"username": "kid_a"})
        print("kid login (no pin):", r.status_code)
        assert r.status_code == 200, r.text

        # 小孩登录：传错误 PIN -> 拒绝（兼容旧 PIN 逻辑）
        r = await client.post("/api/auth/login", json={"username": "kid_a", "pin": "9999"})
        print("kid login (wrong pin):", r.status_code)
        assert r.status_code == 401, r.text

        # 小孩登录：空 PIN 串 -> 成功
        r = await client.post("/api/auth/login", json={"username": "kid_a", "pin": ""})
        print("kid login (empty pin):", r.status_code)
        assert r.status_code == 200, r.text

        print("PASS: 小孩无需密码")


import asyncio

asyncio.run(main())
