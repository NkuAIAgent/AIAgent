from pathlib import Path
from datetime import datetime
import re

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
KEY = "LAST_CRAWL_TIME"

def load_env_time(env_path=ENV_PATH, key=KEY) -> str:
    """从 .env 中读取时间字符串"""
    if not env_path.exists():
        raise FileNotFoundError(f".env 文件未找到: {env_path}")

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                return line.strip().split("=", 1)[-1]
    raise ValueError(f"未找到键: {key} in {env_path}")

def update_env_time(new_time: str, env_path=ENV_PATH, key=KEY):
    """更新 .env 中的时间"""
    lines = []
    updated = False

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith(f"{key}="):
                    lines.append(f"{key}={new_time}\n")
                    updated = True
                else:
                    lines.append(line)

    if not updated:
        lines.append(f"{key}={new_time}\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
