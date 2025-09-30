import os

# 配置数据库，包括连接信息和模型位置

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")}, #从环境变量获取数据库连接URL
    "apps": {
        "models": {
            "models": [
                "src.database.models", "aerich.models"
            ],
            "default_connection": "default"
        }
    }
}