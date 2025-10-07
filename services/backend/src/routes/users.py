from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm  # 标准的用户名/密码登录表单
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import (
    HTTPNotFoundError,
)  # Tortoise ORM的HTTP 404错误模型，用于API文档
from src.auth.user import validate_user  # 用户验证函数
import src.crud.users as crud  # 用户CRUD操作模块
from src.schemas.Status import Status  # 状态响应模型
from src.schemas.users import UserInSchema, UserOutSchema  # 用户输入/输出数据模型

from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)  # JWT处理模块

# 创建一个FastAPI路由器

router = APIRouter(tags=["users"])  # tags用于API文档分组


# 1.用户注册路由
@router.post("/register", response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    """
    创建新用户 HTTP方法-Post
    Args:
        user (UserInSchema): 用户输入数据模型
    Returns:
        UserOutSchema: 创建成功的用户数据模型
    """
    return await crud.create_user(user)


# 2.用户登录路由
@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    """
    处理用户登录 HTTP方法-Post
    Args:
        user (OAuth2PasswordRequestForm): 通过依赖注入获取的用户登录表单数据，包含用户名和密码
    Returns:
        JSONResponse:包含登录信息和访问令牌的JSON响应
    """

    # validate_user失败会直接抛出HTTPException，不需要额外检查
    validated_user = await validate_user(user)

    access_token_expires = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )  # 设置令牌过期时间
    access_token = create_access_token(
        data={"sub": validated_user.username}, expires_delta=access_token_expires
    )  # 创建JWT访问令牌

    token = jsonable_encoder(access_token)  # 将令牌编码为JSON可序列化格式
    content = {"message": "You've successfully logged in"}  # 创建成功消息
    response = JSONResponse(content=content)  # 构造JSON响应对象

    response.set_cookie(
        "Authorization",  # 设置cookie的键为"Authorization"
        value=f"Bearer {token}",  # 设置cookie的值为Bearer访问令牌 中间需要有一个空格
        httponly=True,
        max_age=1800,  # 设置cookie的最大存活时间为1800秒（30分钟）
        expires=1800,
        samesite="lax",  # 防止CSRF攻击
        secure=False,  # 本地运行是False,在生产环境中应设置为True以确保通过HTTPS传输
    )
    return response


# 3.获取当前用户信息路由
@router.get(
    "/users/whoami",
    response_model=UserOutSchema,
    dependencies=[
        Depends(get_current_user),
    ],
    summary="Get current user",
    description="Need user login to access",
)  # 第一层注入：装饰器中的依赖声明。依赖注入get_current_user函数，验证请求中的cookie，确保只有已登录用户才能访问 以及写上API文档声明
async def read_users_me(
    current_user: UserOutSchema = Depends(get_current_user),
) -> UserOutSchema:
    """
    获取当前登录用户的信息 HTTP方法-Get
    Args:
        current_user (UserOutSchema): 通过依赖注入获取的当前登录用户对象
    Returns:
        UserOutSchema: 当前用户的数据模型
    """
    return current_user


# 4.删除用户路由
@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[
        Depends(get_current_user),
    ],  # 依赖注入，确保只有登录用户才能访问
    summary="Delete a user",
    description="Need user login to access, only can delete yourself",
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    """
    删除指定ID的用户 HTTP方法-Delete
    Args:
        user_id (int): 要删除的用户ID，从路径参数获取
        current_user (UserOutSchema): 通过依赖注入获取的当前登录用户对象
    Returns:
        Status: 删除操作的状态信息
    """
    return await crud.delete_user(user_id, current_user)
