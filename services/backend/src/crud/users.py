from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.users import UserOutSchema
from src.schemas.Status import Status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #一个哈希对象

async def create_user(user) ->UserOutSchema:
    """
    创建一个新用户
    Args:
         user(UserInSchema): 包含用户信息的Pydantic模型
    Returns:
        UserOutSchema: 创建成功后返回的用户信息，不包含密码
    Raises:
        HTTPException: 如果用户名已存在，返回400错误
    """
    user.password = pwd_context.hash(user.password) #对密码进行哈希处理
    
    try:
        user_newobj = await Users.create(**user.dict(exclude_unset=True)) #通过Tortoise ORM的create()创建用户
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    return await UserOutSchema.from_tortoise_orm(user_newobj) #将Tortoise ORM模型转换为Pydantic模型返回

async def delete_user(user_id, current_user) -> Status:
    """
    删除指定id的用户
    Args:
        user_id(int): 要删除的用户ID
        current_user(Users): 当前登录的用户对象
    Returns:
        Status: 删除操作的状态信息
    Raises:
        HTTPException: 如果用户不存在或尝试删除自己，返回相应的错误
    """
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail="User not found")
        return Status(message="User deleted successfully")
    else:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this user")

