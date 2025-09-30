import os
import cv2  # opencv图像处理库
import random  # 生成随机数（用于随机选择颜色）
import torch  # PyTorch深度学习框架
from typing import List, Optional  # 用于类型注解
from ultralytics import YOLO  # Ultralytics YOLO模型 官方实现库
from pathlib import Path
from dataclasses import dataclass


@dataclass  # 使用dataclass简化类的定义
class DetectorCOnfig:
    """检测器配置类-集中管理所有配置参数
    使用@dataclass装饰器的优势：
    1. 自动生成__init__方法
    2. 自动生成__repr__方法
    3. 类型安全
    4. 代码更简洁
    """

    default_conf_threshold: float = (
        0.25  # 默认置信度阈值：超过25%的检测结果才被认为是有效的
    )
    default_imgsz: int = 640  # YOLO模型的标准输入尺寸，所有输入图片都会被缩放到640x640像素(精度和速度的平衡点)
    output_image_dir: str = (
        "src/yolo/output/images"  # 图片输出目录：处理后的图片保存位置
    )
    output_video_dir: str = (
        "src/yolo/output/videos"  # 视频输出目录：处理后的视频保存位置
    )
    models_dir: str = "src/yolo/models"  # 模型目录：存放YOLO模型文件的位置


# 自定义一个Dector类，用于目标检测
class Detector:
    """
    YOLO 目标检测器主类
    这个类就像一个"AI检测专家":
    1.初始化时选择工作设备(CPU,GPU)
    2.加载专业技能(YOLO模型)
    3.接收工作任务
    4.输出检测报告
    """

    def __init__(
        self,
        model_path: str = "src/yolo/models/yolo11n.pt",
        config: Optional[DetectorCOnfig] = None,
    ):
        """
        初始化检测器，加载YOLO模型。

        参数:
        - model_path: YOLO模型的路径，默认为"src/yolo/models/yolo11n.pt"
                      n表示nano，最小最快的版本
          config:配置对象，如果为None则使用默认配置
        """
        self.config = config or DetectorCOnfig()  # 如果没有提供配置对象，创建默认配置
        self.model_path = model_path  # 保存模型路径
        self.device = self._get_device()  # 确定使用GPU还是CPU
        self.load_model()  # 加载模型
        self.results = []  # 存储检测结果

    def _get_device(self) -> str:
        """
        确定使用GPU还是CPU进行计算。

        返回:
        - "cuda" 如果有可用的GPU，否则返回 "cpu"
        """
        return "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self):
        """
        从类构造函数定义的模型路径中加载YOLO模型
        Return:
           设置self.model为YOLO模型
        """
        if not os.path.exists(self.model_path):  # 检查文件存在
            raise FileNotFoundError(f"Model file not found at {self.model_path}")

        print(f"正在加载模型: {self.model_path}")
        # 使用YOLO类加载模型文件
        self.model = YOLO(model=self.model_path)
        # 上一行代码做了很多工作：
        # 1.读取.pt文件（Pytorch模型文件）
        # 2.解析模型结构和权重
        # 3.初始化神经网络
        # 4.加载训练好的参数
        # 5.准备模型用于推理
        self.model_name = Path(
            self.model_path
        ).stem  # 提取模型名称（不含扩展名） stem()是提取单个文件的名称
        print(f"模型名称: {self.model_name}加载成功！")

    def detect_picture(
        self,
        image_path: List[str],
        conf_threshold: float = None,
        output_dir: str = "src/yolo/output/images",
    ):
        """
        对输入图像进行目标检测 - 支持进度回调

        参数:
        - image_path: 图像文件路径列表
        - conf_threshold: 置信度阈值，默认为0.25
        - output_dir: 检测结果图像的输出目录，默认为'src/yolo/output/images'

        返回:
        - output_dir: 保存检测结果图像的目录路径
        """

        # 支持进度回调 定义内部进度报告函数 待完成

        # 参数处理：如果没有指定阈值，使用配置中的默认值
        conf_threshold = conf_threshold or self.config.default_conf_threshold

        # 参数处理：如果没有指定输出目录，使用配置中的默认值
        output_dir = output_dir or self.config.output_image_dir

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.results = self.model.predict(
            source=image_path,  # 输入图像路径
            conf=conf_threshold,  # 置信度阈值
            save=False,  # 保存检测结果图像
            device=self.device,  # 使用的设备
            show=False,  # 不显示检测窗口
            imgsz=self.config.default_imgsz,  # 将图片缩放到640x640
        )

        print("检测完成，正在保存结果...")
        self.save_picture_result(output_dir)  # 保存检测结果图像
        print(f"结果已保存到:{output_dir}")
        return output_dir

    def detect_video(
        self, video_path: str, conf_threshold: float = None, output_dir: str = None
    ):
        """
        逐帧处理视频目标检测
        1.打开视频文件
        2.逐帧读取视频内容
        3.对每一帧进行物体检测
        4.在帧上绘制检测结果

        参数:
        - video_path(str): 视频文件路径
        - conf_threshold(float): 置信度阈值，默认为DetectorConfig里面的0.25
        - output_dir(str): 输出视频文件的目录，默认为DetectorConfig里面的'src/yolo/output/videos'
        返回:
        - output_video_path(str): 保存检测结果视频的完整路径
        """
        # 参数处理：使用配置默认值
        conf_threshold = conf_threshold or self.config.default_conf_threshold
        output_dir = output_dir or self.config.output_video_dir

        print(f"开始处理视频: {video_path}")
        print(f"置信度阈值: {conf_threshold}")

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"创建输出目录:{output_dir}")

        # 打开视频文件
        cap = cv2.VideoCapture(video_path)

        # 检查视频是否成功打开
        if not cap.isOpened():
            error_msg = f"无法打开视频文件:{video_path}"
            print(error_msg)
            return ValueError(error_msg)

        # 获取视频属性信息
        fps = int(cap.get(cv2.CAP_PROP_FPS))  # 帧率(每秒帧数) 每秒播放多少帧
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 视频宽度(px)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频高度(px)

        print(f"视频信息: {width}x{height} @ {fps}FPS")

        # 设置视频编码格式
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 使用mp4编码 兼容性较好

        # 生成输出视频文件名
        video_name = Path(video_path).stem
        output_video_path = os.path.join(
            output_dir, f"{video_name}_{self.model_name}_detected.mp4"
        )
        print(f"输出视频路径:{output_video_path}")

        # 创建视频写入对象
        out = cv2.VideoWriter(output_video_path, fourcc, fps, {width, height})

        # 检查视频写入对象是否创建成功
        if not out.isOpened():
            raise RuntimeError(f"无法创建输出视频文件:{output_video_path}")

        # 颜色字典：为不同类别的物体分配不同颜色
        colors = {}

        frame_count = 0  # 帧计数器，在处理过程中统计处理了多少帧

        # 开始逐帧处理视频
        print("开始逐帧处理..")
        while cap.isOpened():
            # 读取下一帧
            ret, frame = cap.read()

            # 检查是否成功读取帧
            if not ret:
                print("视频处理完成")
                break

            frame_count += 1  #

            # 每处理100帧显示一次进度
            if frame_count % 100 == 0:
                print(f"已处理{frame_count}帧...")

            results = self.model.predict(
                frame,
                device=self.device,
                conf=conf_threshold,
                imgsz=self.config.default_imgsz,
            )

            for result in results:  # 针对所有处理帧里面的每一帧
                if result.boxes is not None:  # 添加安全检查
                    for box in result.boxes:  # 针对每一帧里面的每一个检测框
                        x1, y1, x2, y2 = map(
                            int, box.xyxy[0]
                        )  # 提取边界框坐标并转换为整数
                        conf = box.conf[0].item()  # 从box的conf属性中提取置信度
                        class_id = int(
                            box.cls[0].item()
                        )  # 从box的cls属性中提取类别ID并转换为整数
                        class_name = result.names[
                            class_id
                        ]  # 从result的names属性中提取类别名称

                        if conf >= conf_threshold:  # 只处理置信度高于阈值的检测结果
                            # 为每个类别分配随机颜色
                            if class_id not in colors:
                                colors[class_id] = (
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                    random.randint(0, 255),
                                )  # 生成随机颜色

                            color = colors[class_id]
                            label = f"{class_name} {conf:.2f}"  # 标签文本 包含类别名称和置信度
                            # 在帧上绘制边界框和标签
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            cv2.putText(
                                frame,
                                label,
                                (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                color,
                                2,
                            )

            # 将处理后的帧写入输出视频
            out.write(frame)

        cap.release()  # 释放视频捕获对象
        out.release()  # 释放视频写入对象

        print(f"视频处理完成，共处理{frame_count}帧")
        return output_video_path

    def change_model(self, new_model_path: str):
        """
        切换一个新的YOLO模型
        Args:
            new_model_path (str): 新模型的路径
        """
        pre_path = self.config.models_dir
        full_path = pre_path + new_model_path
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Model file not found at {full_path}")

        self.model_path = full_path
        self.load_model()

    def save_picture_result(self, output_dir: str = "src/core/yolo/output/images"):
        """
        保存检测结果为图片
        Args:
            output_dir (str): 输出目录
        """
        for i, r in enumerate(
            self.results
        ):  # 遍历所有检测结果 返回第一个值是索引，第二个值是真正的每个结果
            img_with_boxes = r.plot(labels=True, line_width=2)  # 在图像上绘制检测框
            cv2.imwrite(output_dir + f"/detected_{i}.jpg", img_with_boxes)  # 保存图像


# 简单测试代码，测试图像可以传入yolo/test_image文件夹里
if __name__ == "__main__":
    print("开始测试YOLO检测器...")

    # 使用相对路径
    model_path = "src/yolo/models/yolo11n.pt"
    test_image_dir = "src/yolo/test_image"

    try:
        # 检查模型文件和测试文件夹是否存在
        if not os.path.exists(model_path) or not os.path.exists("src/yolo/test_image"):
            raise FileNotFoundError(
                f"模型或测试文件夹不存在，请检查路径: {model_path} 或 src/yolo/test_images"
            )

        # 获取测试图片列表
        image_extensions = [".jpg", ".jpeg", ".png", "bmp"]
        test_images = []

        # 遍历测试文件夹，收集所有图片文件
        for file in os.listdir(test_image_dir):  # 这里的file是子文件名
            if any(file.lower().endswith(ext) for ext in image_extensions):
                test_images.append(
                    os.path.join(test_image_dir, file)
                )  # 把测试图片的路径拼成完整路径

        if not test_images:
            print(f"错误：在 {test_image_dir} 目录下没有找到图片文件")
            print(f"支持的格式: {', '.join(image_extensions)}")
            exit(1)

        print(f"找到 {len(test_images)} 张测试图片:")
        for img in test_images:
            print(f"  - {img}")

        # 创建检测器
        print(f"\n正在加载模型: {model_path}")
        detector = Detector(model_path)
        print(f"✅ 检测器初始化成功，使用设备: {detector.device}")

        # 执行图片检测
        print(f"\n🔍 开始检测 {len(test_images)} 张图片...")
        output_dir = detector.detect_picture(test_images, conf_threshold=0.25)
        print(f"✅ 图片检测完成，结果保存至: {output_dir}")

        # 显示结果统计
        if os.path.exists(output_dir):
            result_files = [f for f in os.listdir(output_dir) if f.endswith(".jpg")]
            print(f"📊 生成了 {len(result_files)} 个结果文件:")
            for result_file in result_files:
                print(f"  - {os.path.join(output_dir, result_file)}")

        print("\n🎉 测试完成！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()
