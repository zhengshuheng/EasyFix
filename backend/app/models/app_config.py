# -*- coding: utf-8 -*-
"""运营配置表 app_config（key/value 扁平结构）。

配置键（默认值见 app/config_defaults.py，启动时播种）：
- trial_days        体验期天数（默认 15）
- online_price      云端正式版价格（元/年，默认 100）
- local_price       本地版价格（元，默认 50）
- local_download_url   本地版下载包链接（官网/升级页用）
- local_guide_url      本地版安装指引链接
- ops_password      运营后台口令（默认 easyfix-ops）
"""
from sqlalchemy import Column, Integer, String, DateTime, func

from app.database import Base
from app.utils.timeutil import now_local


class AppConfig(Base):
    __tablename__ = "app_config"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(64), nullable=False, unique=True)
    value = Column(String(500), nullable=False, default="")
    updated_at = Column(DateTime, default=now_local, server_default=func.now(), onupdate=now_local)
