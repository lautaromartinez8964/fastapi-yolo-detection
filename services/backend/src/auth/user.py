from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from src.database.models import Users
from src.schemas.users import UserDatabaseSchema

# 密码处理配置
# 使用passlib的CryptContext来管理密码哈希,构造一个CryptContext对象
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 1.验证明文密码是否与哈希密码匹配
def verify_password(plain_password, hashed_password):
    """
    验证明文密码是否与哈希密码匹配
    Args:
        plain_password (str): 明文密码
        hashed_password (str): 哈希密码
    Returns:
        bool: 如果匹配返回True,否则返回False

    为什么不能简单比较字符串：
      哈希算法有随机盐值，每次生成的哈希都不同，需要CryptContext对象进行专门的验证算法
    """
    return pwd_context.verify(plain_password, hashed_password)


# 2.获取密码的哈希值
def get_password_hash(password):
    """
    利用CryptContext对象的hash方法，获取密码的哈希值
    Args:
        password (str): 明文密码
    Returns:
        str: 哈希后的密码字符串
    """
    return pwd_context.hash(password)


# 3.用户查询函数
async def get_user(username: str):
    """
    根据用户名从数据库中查询用户
    Args:
        username (str): 用户名
    Returns:
        UserDatabaseSchema | None: 如果找到用户，返回UserDatabaseSchema对象，否则返回None
    """
    return await UserDatabaseSchema.from_queryset_single(Users.get(username=username))


# 4.用户验证主函数
async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    """
    验证用户的用户名和密码
    Args:
        user (OAuth2PasswordRequestForm): 通过依赖注入获取的用户登录表单数据，包含用户名和密码
    Returns:
        UserDatabaseSchema | None: 如果验证成功，返回用户对象，否则返回None

    关于OAuth2PasswordRequestForm：
        这是FastAPI提供的一个类，用于处理OAuth2密码模式的登录请求。
        它会自动从请求中提取用户名和密码，并将其封装到该对象中，方便在路径操作函数中使用。
        1.用户POST登录表单数据
        2.Fastapi自动解析表单，创建OAuth2PasswordRequestForm对象
        3.通过Depends将user对象传递给Validate_user函数
    """
    try:
        # 从数据库中获取用户
        db_user = await get_user(user.username)
    except DoesNotExist:
        # 如果用户不存在，抛出 HTTP 401 错误
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 验证密码是否正确
    if not verify_password(user.password, db_user.password):
        # 如果密码不正确，抛出 HTTP 401 错误
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # 返回验证通过的用户
    return db_user
