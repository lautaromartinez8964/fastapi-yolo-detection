from tortoise.contrib.pydantic import pydantic_model_creator
#上面一句话的意思是从tortoise.contrib.pydantic模块中导入Tortoise的函数pydantic_model_creator函数，这个函数用于将Tortoise ORM模型转换为Pydantic模型，方便在FastAPI中进行数据验证和序列化。
#如果是fastapi的tutorial，则是from pydantic import BaseModel,但我们使用Tortoise ORM，所以用pydantic_model_creator
from src.database.models import Users

# 创建一个UserIn的Pydantic模型，用于表示用户输入的数据，不包括只读字段（如主键id和时间戳）
UserInSchema = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

# 创建一个UserOut的Pydantic模型，用于表示用户输出的数据，不包括密码及创建/修改时间
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=("password", "created_at", "modified_at")
)

# 创建一个用于检索要在应用程序中使用的用户信息，用于验证用户的Pydantic模型
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=("created_at", "modified_at")
)