import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel  # OAuth2流程模型
from fastapi.security import OAuth2  # OAuth2安全类
from fastapi.security.utils import get_authorization_scheme_param  # 获取授权方案参数
from jose import JWTError, jwt  # JWT核心功能库与
from tortoise.exceptions import DoesNotExist

from src.schemas.Status import TokenData
from src.schemas.users import UserOutSchema
from src.database.models import Users

# 从环境变量中获取密钥，用于加密和解密JWT
SECRET_KEY = os.environ.get("SECRET_KEY")

ALGORITHM = "HS256"  # 指定JWT的加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 令牌30分钟过期


# 定义一个自定义的OAuth2类，支持从Cookie中获取令牌
# FastAPI默认从HTTP Header读取Token，这里要从Cookie读取
class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        token_Url: str,  # 登陆接口地址
        scheme_name: Optional[str] = None,  # 认证方案名称
        scopes: Optional[dict] = None,  # 权限范围
        auto_error: bool = True,  # 是否自动抛出错误
    ):
        if not scopes:
            scopes = {}  # 如果没有传入权限范围，设为空字典 避免None值导致错误
        # 创建OAuth2流程配置，指定密码模式的令牌URL和权限范围
        flows = OAuthFlowsModel(password={"tokenUrl": token_Url, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    # 核心方法：从Cookie获取Token
    async def __call__(
        self, request: Request
    ) -> Optional[str]:  # 唤起函数，创建一个实例时调用__call__，从请求中获取Token
        authorization: str = request.cookies.get(
            "Authorization"
        )  # 从请求的Cookie中获取Authorizatrion字段
        # 如果Cookie是：Authorization=Bearer abc123
        # 则authorization = "Bearer abc123"
        scheme, param = get_authorization_scheme_param(
            authorization
        )  # 解析授权方案和参数
        # 输入："Bearer abc123"
        # 输出：scheme="Bearer", param="abc123"
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:  # 如果没有提供授权信息，且设置了自动错误
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None  # 否则返回None，表示没有认证信息
        return param  # 返回解析出的Token字符串 即实际的param部分


security = OAuth2PasswordBearerCookie(
    token_Url="/login"
)  # 创建认证实例，实例化自定义的OAuth2类，指定登录接口地址为/login


# Token生成函数
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Args:
        data (dict): 要编码到JWT中的数据，即放入Token的用户信息，通常包含用户标识等信息
        expires_delta (Optional[timedelta]): 令牌的过期时间，如果未提供则使用默认值
    Return:
        str: 生成的JWT令牌字符串
    """
    to_encode = (
        data.copy()
    )  # 复制数据，避免修改原始数据 Py中字典是引用类型，直接修改会影响原数据

    # 如果传入自定义过期时间，使用自定义时间，否则默认15分钟后过期
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})  # 在数据中添加过期时间字段 exp

    # 生成JWT过程：将数据转为JSON， 用密钥加密， 生成最终的JWT字符串
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  # 返回生成的JWT字符串


# 通过token进行用户认证函数
async def get_current_user(token: str = Depends(security)):
    """
    Args:
        token (str): 通过依赖注入获取的JWT令牌字符串，默认从Cookie中读取
    Returns:
        UserOutSchema: 认证成功后返回的用户信息对象
    """
    # 定义一个HTTPException, 用于在认证失败时抛出异常
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # 解码JWT，获取其中的数据 验证过程:1.检查签名是否正确 2.检查是否过期 3.检查算法是否匹配
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 从解码后的数据获取用户名
        username: str = payload.get("sub")  # JWT标准中，sub字段通常存放用户名或用户ID
        if username is None:
            raise credentials_exception  # 如果没有用户名，抛出认证失败异常
        token_data = TokenData(username=username)  # 将用户名封装到TokenData对象中
    except JWTError as e:
        print(f"JWTError: {e}")  # 记录具体的JWT错误信息，用于调试
        raise credentials_exception  # 如果解码失败，抛出认证失败异常

    # 查询用户信息
    try:
        user = await UserOutSchema.from_queryset_single(
            Users.get(username=token_data.username)
        )
    except DoesNotExist:
        raise credentials_exception  # 如果用户不存在，抛出认证失败异常

    return user  # 返回查询到的用户信息
