# 检测历史记录的CRUD操作
from typing import List, Optional
from src.database.models import DetectionHistory, DetectionType, Users
from src.schemas.detection import DetectionHistoryCreate, UserStatsOut


async def create_detection_record(
    user_id: int, detection_data: DetectionHistoryCreate
) -> DetectionHistory:
    """
    创建检测历史记录

    Args:
        user_id: 用户ID
        detection_data: 检测数据,要求是Schemas里定义的DetectionHistoryCreate类型

    Returns:
        DetectionHistory: 创建的检测记录
    """
    # 确保用户存在
    user = await Users.get(id=user_id)

    # 创建检测记录,直接通过Tortoise ORM数据库对象类来创建
    detection_record = await DetectionHistory.create(
        user=user,
        detection_type=detection_data.detection_type,
        model_used=detection_data.model_used,
        file_count=detection_data.file_count,
        conf_threshold=detection_data.conf_threshold,
        detected_objects_count=detection_data.detected_objects_count,
        processing_time=detection_data.processing_time,
        file_names=detection_data.file_names,
        output_files=detection_data.output_files,
    )

    return detection_record


async def get_user_stats(user_id: int) -> UserStatsOut:
    """
    获取用户的检测统计信息

    Args:
        user_id: 用户ID

    Returns:
        UserStatsOut: 用户统计信息
    """
    # 确保用户存在
    await Users.get(id=user_id)

    # 获取图片处理次数
    images_processed = await DetectionHistory.filter(
        user_id=user_id, detection_type=DetectionType.IMAGE
    ).count()

    # 获取视频处理次数
    videos_processed = await DetectionHistory.filter(
        user_id=user_id, detection_type=DetectionType.VIDEO
    ).count()

    # 获取总检测目标数量 - 使用原生查询
    # 不能在第一句最后直接用aggregate(Sum(...))，因为queryset对象没有aggregate方法，需要转换为list
    records_with_objects = await DetectionHistory.filter(user_id=user_id).all()
    total_detections = sum(
        record.detected_objects_count for record in records_with_objects
    )

    # 获取总处理时间 - 使用原生查询
    records_with_time = await DetectionHistory.filter(
        user_id=user_id, processing_time__isnull=False
    ).all()
    total_processing_time = sum(record.processing_time for record in records_with_time)

    # 获取最后一次检测时间
    last_record = (
        await DetectionHistory.filter(user_id=user_id).order_by("-created_at").first()
    )

    # 处理最后一次检测时间
    last_detection_time = last_record.created_at if last_record else None

    # 返回Schemas定义的UserStatsOut类型
    return UserStatsOut(
        images_processed=images_processed,
        videos_processed=videos_processed,
        total_detections=total_detections,
        total_processing_time=total_processing_time,
        last_detection=last_detection_time,
    )


async def get_all_user_detection_history(
    user_id: int,
    limit: Optional[int] = 50,
    detection_type: Optional[DetectionType] = None,
) -> List[DetectionHistory]:
    """
    获取用户的检测历史记录

    Args:
        user_id: 用户ID
        limit: 限制返回的记录数量，默认为50
        detection_type: 检测类型，可以是IMAGE或VIDEO，默认为None

    Returns:
        List[DetectionHistory]: 检测历史记录列表
    """
    # 因为从src.models引入了检测历史模型，可以通过ORM，直接去数据库里查询对应的表并返回结果
    # filter()方法是Tortoise ORM的查询过滤器方法，返回的是QuerySet对象，不是立刻查询
    # 实际查询，在调用await时执行，比如最后一句return await query.order_by时才执行
    user_detect_query = DetectionHistory.filter(user_id=user_id)

    if detection_type:
        user_detect_query = user_detect_query.filter(detection_type=detection_type)

    if limit:
        user_detect_query = user_detect_query.limit(limit)

    return await user_detect_query.order_by("-created_at").all()
