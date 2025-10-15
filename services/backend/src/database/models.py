# 数据库模型 有用户模型(id为主键),与检测历史模型(id为主键)
from tortoise import fields, models
from enum import Enum


# 一个表示检测类型的枚举
class DetectionType(str, Enum):
    """检测类型枚举"""

    IMAGE = "image"
    VIDEO = "video"


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return f"{self.username}, {self.full_name} on {self.created_at}"


# def __str__(self)函数:
#   是py的“魔术方法”，用于定义对象的字符串表示形式，当打印对象或将对象转换为字符串时，该方法会被调用，方便调试和日志记录
class DetectionHistory(models.Model):
    """用户检测记录模型"""

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.Users", related_name="detection_history", on_delete=fields.CASCADE
    )  # 外键：一对一关系，关联到Users模型
    detection_type = fields.CharEnumField(
        DetectionType, description="detection type:image or video"
    )
    model_used = fields.CharField(max_length=50, description="model used name")
    file_count = fields.IntField(
        description="numbers of files processed one-time, image may many, video only one"
    )
    conf_threshold = fields.FloatField(description="confidence threshold")
    detected_objects_count = fields.IntField(description="detected objects count")
    processing_time = fields.FloatField(description="processing time in seconds")
    file_names = fields.JSONField(
        description="list of processed file names"
    )  # 用JSON存储文件名列表，是因为文件名数量不固定，JsonField可以存储任意JSON数据
    output_files = fields.JSONField(description="list of output file names")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        # 设置数据库表名
        table = "detection_history"
        ordering = ["-created_at"]  # 默认按创建时间降序排列

    def __str__(self):
        return f"{self.user.username} - {self.detection_type} on {self.created_at}"
