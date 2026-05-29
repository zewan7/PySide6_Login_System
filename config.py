import redis
import os
import time

# 是否使用本地 SQLite 数据库 (True: SQLite, False: MySQL)
USE_SQLITE = True

# 是否使用 Redis (True: 使用 Redis, False: 使用本地内存字典代替)
USE_REDIS = False

# 登陆界面图片更换时间间隔(ms)
IMGS_TIME = 5000

config = {
    "db_params": {    # mysql数据库配置
        "user": "root",
        "port": 3306,
        "host": "47.xxx.xxx.xxx",
        "password": "xxxxxx",
        "db": "xxx",
    },

    "redis": {      # redis
        "host": '47.xxx.xxx.xxx',
        "port": 6379,
        "password": 'xxxxxx',
        "db": 1,
        "decode_responses": True
    },

    "email": {
        "host": "smtp.qq.com",
        "smtp_ssl": True,
        "port": 465,
        "user": "cukuangren@qq.com",
        "password": "mebjltnndclpbhjh"
    },
}

config["redis_url"] = "redis://:{password}@{host}:{port}/1".format(**config["redis"])

if USE_SQLITE:
    import sys
    # 获取真正的运行目录（兼容 PyInstaller 打包后的环境）
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(__file__)
        
    sqlite_path = os.path.join(base_dir, "local_data.db")
    config["db_url"] = f"sqlite:///{sqlite_path}"
else:
    config["db_url"] = "mysql+pymysql://{user}:{password}@{host}:{port}/{db}?charset=utf8mb4".format(**config["db_params"])

class LocalCache:
    """本地内存字典，用来替代 Redis 存储验证码及其过期时间"""
    def __init__(self):
        self.store = {}

    def set(self, key, value, ex=None):
        # ex 表示过期的秒数
        expire_at = time.time() + ex if ex else None
        self.store[key] = {'value': str(value), 'expire_at': expire_at}

    def get(self, key):
        if key in self.store:
            item = self.store[key]
            if item['expire_at'] is None or time.time() < item['expire_at']:
                return item['value']
            else:
                # 已经过期，删除并返回 None
                del self.store[key]
                return None
        return None

if USE_REDIS:
    # 可能会因为没有安装 redis 库而报错，如果不装可以注释掉上面 import redis
    redis_conn = redis.Redis(**config["redis"])
else:
    # 零依赖本地缓存
    redis_conn = LocalCache()
