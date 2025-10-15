# 🎯 FastAPI YOLO Detection System

基于FastAPI + Vue.js + YOLO11的智能目标检测Web应用系统。支持图片和视频的实时目标检测，提供用户管理、模型切换等完整功能。

## ✨ 功能特性

### 🔐 用户系统
- **用户注册/登录** - JWT Token认证，安全可靠
- **个人资料管理** - 用户信息展示和管理
- **权限控制** - 基于Cookie的身份验证

### 🔍 AI检测功能
- **图片检测** - 支持JPG、PNG、JPEG格式，可批量上传
- **视频检测** - 支持MP4、AVI格式视频文件
- **实时预览** - 检测前后对比展示
- **模型切换** - 支持多种YOLO模型切换

### 📊 技术栈
- **后端**: FastAPI + Tortoise ORM + PostgreSQL
- **前端**: Vue 3 + Composition API + Vuex + Bootstrap 5
- **AI引擎**: YOLO11 (Ultralytics)
- **部署**: Docker + Docker Compose

## 🚀 快速开始

### 📋 系统要求

- **Docker** >= 20.10
- **Docker Compose** >= 2.0
- **系统内存** >= 4GB (推荐8GB)
- **硬盘空间** >= 5GB

### 🛠️ 安装步骤

#### 1. 克隆项目
```bash
git clone <repository-url>
cd fastapi_yolo_fxy
```

#### 2. 启动服务
```bash
# 构建并启动所有服务
docker compose up --build
# 如果拉不下来，可以先运行：
docker pull cnstark/pytorch:2.3.1-py3.10.15-ubuntu22.04
# 或者后台运行
docker compose up --build -d
```

#### 3. 访问应用
- **前端界面**: http://localhost:8080
- **后端API文档**: http://localhost:5000/docs
- **数据库**: localhost:5432

### 🔧 开发模式

如果需要开发调试，可以单独启动服务：

```bash
# 启动数据库
docker compose up db -d

# 启动后端 (开发模式)
cd services/backend
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 5000

# 启动前端 (开发模式)
cd services/frontend
npm install
npm run serve
```

## 📁 项目结构

```
fastapi_yolo_fxy/
├── docker-compose.yml          # Docker编排配置
├── README.md                   # 项目文档
├── services/
│   ├── backend/                # FastAPI后端服务
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── src/
│   │   │   ├── main.py        # 应用入口
│   │   │   ├── auth/          # 认证模块
│   │   │   ├── crud/          # 数据库操作
│   │   │   ├── database/      # 数据库配置
│   │   │   ├── models/        # AI模型文件
│   │   │   ├── routes/        # API路由
│   │   │   ├── schemas/       # 数据模型
│   │   │   └── yolo/          # YOLO检测核心
│   │   └── tests/             # 测试文件
│   └── frontend/              # Vue.js前端应用
│       ├── Dockerfile
│       ├── package.json
│       ├── src/
│       │   ├── components/    # Vue组件
│       │   ├── router/        # 路由配置
│       │   ├── store/         # Vuex状态管理
│       │   └── views/         # 页面视图
│       └── public/            # 静态资源
```

## 🎮 使用指南

### 1. 用户注册/登录
1. 访问 http://localhost:8080
2. 点击"注册"创建新账户
3. 使用用户名和密码登录系统

### 2. 目标检测
1. 登录后点击"目标检测"菜单
2. 选择YOLO模型 (可选择不同的预训练模型)
3. 上传图片或视频文件
4. 查看检测结果和对比效果

### 3. 模型管理
- **可用模型**:
  - `yolo11n.pt` - 通用目标检测 (默认)
  - `valorant.pt` - 游戏场景检测
  - `gtav_50k.pt` - GTA游戏场景
  - `gtav_50kplus.pt` - GTA增强版

## 🔧 API文档

访问 http://localhost:5000/docs 查看完整的API文档

### 主要API端点

#### 用户管理
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `GET /users/whoami` - 获取当前用户信息

#### YOLO检测
- `POST /yolo/detect_picture` - 图片检测
- `POST /yolo/detect_video` - 视频检测
- `POST /yolo/change_model` - 切换模型
- `GET /yolo/available_models` - 获取可用模型

## 🧪 测试

### 后端测试
```bash
cd services/backend
pytest tests/
```

### API测试示例
```bash
# 用户注册
curl -X POST "http://localhost:5000/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'

# 用户登录
curl -X POST "http://localhost:5000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test123"

# 图片检测
curl -X POST "http://localhost:5000/yolo/detect_picture" \
  -F "files=@/path/to/image.jpg" \
  -F "conf_threshold=0.25"
```

## 🐛 故障排除

### 常见问题

#### 1. 容器启动失败
```bash
# 检查容器状态
docker compose ps

# 查看日志
docker compose logs backend
docker compose logs frontend
```

#### 2. 数据库连接失败
```bash
# 重启数据库服务
docker compose restart db

# 检查数据库连接
docker compose exec db psql -U hello_fastapi -d hello_fastapi_dev
```

#### 3. YOLO模型加载失败
- 确保模型文件存在于 `services/backend/src/yolo/models/`
- 检查模型文件权限和大小
- 查看后端日志获取详细错误信息

#### 4. 前端无法访问后端
- 检查CORS配置
- 确认后端服务在5000端口正常运行
- 检查网络连接和防火墙设置

### 性能优化

#### 内存使用
```bash
# 监控容器资源使用
docker stats

# 限制容器内存使用
docker compose up --memory=2g
```

#### 清理空间
```bash
# 清理未使用的镜像和容器
docker system prune -f

# 清理项目相关容器
docker compose down --rmi all --volumes
```

## 📝 开发说明

### 环境变量配置

在生产环境中，建议修改以下环境变量：

```bash
# .env 文件
DATABASE_URL=postgres://user:password@db:5432/database
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 数据库迁移

```bash
# 进入后端容器
docker compose exec backend bash

# 初始化数据库
aerich init -t src.database.config.TORTOISE_ORM

# 生成迁移文件
aerich init-db

# 应用迁移
aerich upgrade
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

