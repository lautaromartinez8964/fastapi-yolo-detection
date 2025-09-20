from typing import Optional
from tortoise import Tortoise

def register_tortoise(
    app,
    config:Optional[dict] = None,
    generate_schemas:bool = False,
)->None:
    """
    初始化并注册Tortoise ORM到FastAPI应用中

    Args:
        app: FastAPI应用实例
        config: Tortoise ORM配置字典，可以不提供，为默认配置
        generate_schemas: 是否在启动时生成数据库模式
    Returns:
        None
    """
    @app.on_event("startup")
    async def init_orm():
        """
        在应用启动时初始化Tortoise ORM
        Return:
            None
        """
        await Tortoise.init(config=config)
        if generate_schemas:
            await Tortoise.generate_schemas()
    
    @app.on_event("shutdown")
    async def close_orm():
        """
        在应用关闭时关闭Tortoise ORM连接
        Return:
            None
        """
        await Tortoise.close_connections()
        
    
  