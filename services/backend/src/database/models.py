# 数据库模型 只有用户模型，id为主键，
from tortoise import fields, models

class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    full_name = fields.CharField(max_length=50, null=True)
    password = fields.CharField(max_length=128, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at =  fields.DatetimeField(auto_now = True)
    
    def __str__(self):
        return f"{self.username}, {self.full_name} on {self.created_at}"