# 检测历史相关的数据模式
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from src.database.models import DetectionType


class DetectionHistoryBase(BaseModel):
    """检测历史基础模式"""

    # 定义检测历史的核心字段，
    # 不直接用pydantic_create_model()的原因：ORM使用对象关系(user的一对一关系，这在Schema里面最好自己定义),且ROM需要数据库兼容的JSONField字段，而pydantic_create_model()不支持
    detection_type: DetectionType
    model_used: str
    file_count: int
    conf_threshold: float
    detected_objects_count: Optional[int] = 0
    processing_time: Optional[float] = None
    file_names: List[str] = []
    output_files: List[str] = []


class DetectionHistoryCreate(DetectionHistoryBase):
    """创建检测历史记录的输入模式"""

    # 专门用于创建新记录的输入验证，用于POST请求的请求体验正
    user_id: int


class DetectionHistoryOut(DetectionHistoryBase):
    """检测历史输出模式"""

    # 定义API响应的数据结构，用于GET请求的响应格式
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # 允许从ORM对象自动转换


class UserStatsOut(BaseModel):
    """用户统计信息输出模式"""

    # 定义用户统计信息的输出模式，用于GET请求的响应格式，同样支持ORM转换，包含在具体函数里聚合计算的结果字段
    images_processed: int = 0
    videos_processed: int = 0
    total_detections: int = 0
    total_processing_time: float = 0.0
    last_detection: Optional[datetime] = None

    class Config:
        from_attributes = True
