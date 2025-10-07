from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise
from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

from src.routes import users, yolo  # 导入路由模块

# 初始化模型，以确保app能读取模型之间的关系
Tortoise.init_models(["src.database.models"], "models")

app = FastAPI()

# 添加中间件，解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8081",
        "http://127.0.0.1:8081",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(yolo.router)

# 添加静态文件路由，用于提供检测结果图片和视频
app.mount(
    "/static/outputs", StaticFiles(directory="src/yolo/output"), name="static_outputs"
)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/")
def home():
    return "Hello,World!"
