import pytest
from fastapi import HTTPException

from src.crud import users as users_crud
from src.schemas.users import UserInSchema, UserOutSchema
from src.database.models import Users
from src.schemas.Status import Status


@pytest.mark.asyncio
async def test_create_user_success(monkeypatch):
    # 测试正常情况下用户创建流程
    # Create input
    # 构建一个用户输入对象
    user_in = UserInSchema(username="alice", full_name="Alice", password="secret")

    # Call 调用
    out = await users_crud.create_user(user_in)

    # Assert 断言
    # 断言1: 输出类型正确，为UserOutSchema
    assert isinstance(out, UserOutSchema)
    # 断言2：数据库中确实创建了该用户,且密码已加密
    created = await Users.get(username="alice")
    assert created.password and created.password != "secret"


@pytest.mark.asyncio
async def test_create_user_conflicet(monkeypatch):
    # 测试创建重复用户名时的重复处理

    # 首先创建两个输入对象，用户名相同但其他信息不同
    user_in_1 = UserInSchema(username="bob", full_name="Bob", password="secret1")
    user_in_2 = UserInSchema(username="bob", full_name="Bob2",password="secret2")

    await users_crud.create_user(user_in_1)  # 先创建第一个用户

    with pytest.raises(HTTPException) as ei:
        await users_crud.create_user(
            user_in_2
        )  # 再创建第二个用户，预期会抛出HTTPException

    assert ei.value.status_code in (409, 401, 400)  # 断言异常的状态码为409或401


@pytest.mark.asyncio
async def test_delete_user_self_only(user_factory):
    # create two users
    me = await user_factory(username="me")
    other = await user_factory(username="other")

    # cannot delete other
    with pytest.raises(HTTPException) as ei:
        await users_crud.delete_user(other.id, current_user=me)
    assert ei.value.status_code in (403, 404)

    #can delete self
    result = await users_crud.delete_user(me.id, current_user=me)
    # 修复:检查返回的是Status对象
    assert isinstance(result, Status)
    assert "deleted" in result.message.lower() or "success" in result.message.lower()

    # verify deleted
    assert await Users.get_or_none(id=me.id) is None
