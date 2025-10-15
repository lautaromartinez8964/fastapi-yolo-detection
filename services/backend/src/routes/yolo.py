from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List
import os  # 用于路径操作
import shutil  # 用于文件操作
import time  # 用于计时
from src.yolo.detector import Detector  # 导入YOLO检测类
from src.auth.jwthandler import get_current_user  # JWT验证用户函数
from src.schemas.detection import DetectionHistoryCreate, UserStatsOut
from src.database.models import DetectionType
from src.crud.detection import create_detection_record, get_user_stats  # CRUD操作函数

router = APIRouter(
    prefix="/yolo", tags=["yolo"]
)  # 创建路由器，所有端点前缀为[/yolo],标签为yolo用于API文档分组

# 初始化YOLO目标检测器
model_path = "src/yolo/models/yolo11n.pt"
detector = Detector(model_path)  # 创建全局检测器实例，所有请求共享同一个检测器


# 1.图片检测端点
@router.post("/detect_picture")
async def detect_picture(
    files: List[UploadFile] = File(
        ...
    ),  # 接收多个上传文件,使用Fastapi的UploadFile(异步文件上传）作为输入类型
    conf_threshold: float = Form(0.25),  # 置信度阈值，默认0.25
    current_user=Depends(get_current_user),  # 获取当前用户
):
    """
    图像目标检测-支持多个图片上传
    先把图片保存到本地，然后调用YOLO检测器进行检测,并记录到用户统计中
    Args:
        files (List[UploadFile]): 上传的图像文件列表
        conf_threshold (float): 置信度阈值，默认0.25
        current_user:当前登录用户
    Returns:
    """

    start_time = time.time()  # 记录开始时间
    try:
        save_dir = "src/yolo/uploads/images"
        os.makedirs(save_dir, exist_ok=True)  # 创建保存上传文件的目录

        file_paths = []
        file_names = []

        for i, file in enumerate(files):
            # 保存原始文件
            file_path = os.path.join(
                save_dir, file.filename
            )  # 构建文件保存路径,获取文件完整路径
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)  # 将上传的文件内容写入本地文件
            file_paths.append(file_path)  # 保存文件路径到列表
            file_names.append(file.filename)  # 保存文件名到列表,记录处理的文件数量

        # 进行目标检测
        detector.detect_picture(file_paths, conf_threshold)

        # 计算处理时间
        processing_time = time.time() - start_time

        # 返回正确的处理后的图片文件名（与detector.py中保存的格式匹配)
        output_images = [
            f"detected_{i}.jpg" for i in range(len(files))
        ]  # 这里的名字要与检测函数里detect_picture保存的名字对应，是detected_{i}就不能写成image_{i}

        # 统计检测到的目标数量（这里需要从检测结果中获取实际数量)
        detected_objects_count = 0
        if (
            hasattr(detector, "results") and detector.results
        ):  # 检查目标检测器detector对象是否有results属性，并且results不为空
            for result in (
                detector.results
            ):  # 遍历所有检测结果（每个result代表了一张图片的检测结果）
                if result.boxes is not None:
                    detected_objects_count += len(
                        result.boxes
                    )  # 若当前检测结果result对象的boxes属性不为空，将当前目标检测的目标数量（一张图片的所有目标框）加到总计数中

        # 记录检测历史
        detection_record = DetectionHistoryCreate(
            user_id=current_user.id,
            detection_type=DetectionType.IMAGE,
            model_used=os.path.basename(detector.model_path),
            file_count=len(files),
            conf_threshold=conf_threshold,
            detected_objects_count=detected_objects_count,
            processing_time=processing_time,
            file_names=file_names,
            output_files=output_images,
        )

        # 创建检测记录
        await create_detection_record(current_user.id, detection_record)

        return {
            "message": "Detection completed successfully",
            "output_images": output_images,  # 返回处理后的图片文件名列表
            "processing_time": round(processing_time, 2),  # 返回处理时间的秒数
            "detected_objects": detected_objects_count,  # 返回检测到的目标数量
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # 捕获所有异常并返回HTTP 500错误，包含异常信息


# 2.视频检测端点
@router.post("/detect_video")
async def detect_video(
    file: UploadFile = File(...),  # 接收单个上传文件
    conf_threshold: float = Form(0.25),  # 置信度阈值，默认0.25
    current_user=Depends(get_current_user),  # 获取当前用户
):
    """
    视频目标检测
    先把视频保存到本地，然后调用YOLO检测器进行检测，并记录到用户统计中
    Args:
        file (UploadFile): 上传的视频文件
        conf_threshold (float): 置信度阈值，默认0.25
        current_user:当前登录用户
    Returns:
    """
    start_time = time.time()

    try:
        save_dir = "src/yolo/uploads/videos"
        os.makedirs(save_dir, exist_ok=True)  # 创建保存上传文件的目录

        # 保存原始文件
        file_path = os.path.join(
            save_dir, file.filename
        )  # 构建文件保存路径,获取文件完整路径
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)  # 将上传的文件内容写入本地文件

        # 进行目标检测
        output_video_path = detector.detect_video(file_path, conf_threshold)

        # 计算处理时间
        processing_time = time.time() - start_time

        # 记录检测历史（视频检测的目标数量较难统计，暂时设为0或者可以从检测器中获取）
        detection_record = DetectionHistoryCreate(
            user_id=current_user.id,
            detection_type=DetectionType.VIDEO,
            model_used=os.path.basename(detector.model_path),
            file_count=1,
            conf_threshold=conf_threshold,
            detected_objects_count=0,  # 视频检测的目标统计比较复杂，暂时设为0
            processing_time=processing_time,
            file_names=[file.filename],
            output_files=[os.path.basename(output_video_path)],
        )

        await create_detection_record(
            current_user.id, detection_record
        )  # 通过crud操作创建检测记录，通过ORM插入数据库

        return {
            "message": "Detection completed successfully",
            "output_video": os.path.basename(
                output_video_path
            ),  # 返回处理后的视频文件名
            "processing_time": round(processing_time, 2),
            "detected_objects": 0,  # 暂且设为0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # 捕获所有异常并返回HTTP 500错误，包含异常信息


# 3.切换模型端点
@router.post("/change_model")
async def change_model(
    model_path: str = Form(...),  # 接收新模型的路径
):
    """
    切换当前使用的YOLO模型
    Args:
        model_path (str): 新模型的文件路径
    Returns:
        JSONResponse: 包含切换结果的JSON响应
    """
    try:
        detector.change_model(model_path)
        return {"message": f"Model changed successfully to {model_path}"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # 捕获所有异常并返回HTTP 500错误，包含异常信息


# 4.获取所有模型路由
@router.get("/available_models")
async def get_available_models():
    """
    获取所有可用的YOLO模型
    Returns:

    """
    try:
        models_dir = "src/yolo/models"
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        # 获取所有模型文件夹里面的.pt文件
        models = [f for f in os.listdir(models_dir) if f.endswith(".pt")]

        # 获取当前正在使用的模型名称
        current_model = os.path.basename(detector.model_path)

        # 返回模型列表和当前模型的JSON响应
        return {"models": models, "current_model": current_model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # 捕获所有异常并返回HTTP 500错误，包含异常信息


# 5.获取用户统计信息路由
@router.get("/user_stats", response_model=UserStatsOut)
async def get_user_detection_stats(current_user=Depends(get_current_user)):
    """
    获取当前用户的检测统计信息
    包括处理的图片数、视频数、检测目标总数等
    Args:
        current_user: 当前登录用户
    Returns:
        UserStatsOut: 用户统计信息
    """
    try:
        # 获取用户的检测统计信息
        user_stats = await get_user_stats(current_user.id)
        return user_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        # 捕获所有异常并返回HTTP 500错误，包含异常信息
