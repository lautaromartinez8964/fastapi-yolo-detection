# 基于官方PyTorch镜像，包含CUDA支持
FROM cnstark/pytorch:2.3.1-py3.10.15-ubuntu22.04 

# 创建并设置工作目录
RUN mkdir app
WORKDIR /app

# 设置环境变量，确保pip安装的包在PATH中,并设置Python模块搜索路径为当前目录
ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

# 安装系统依赖：OpenGL和GLib
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 根据后端的requirements.txt安装Python依赖
COPY requirements.txt .
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 复制数据库迁移文件，项目配置和源代码
COPY migrations .
COPY pyproject.toml .

COPY src/ ./src/