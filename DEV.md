# 开发环境配置指南

本项目支持两种开发模式：Docker 开发环境和本地开发环境。推荐使用 Docker 开发环境，以保持与生产环境的一致性。

## 1. 首次环境设置

```bash
# 创建 Docker 网络（如果还没有）
docker network create blog-network

# 创建必要的目录
mkdir -p logs uploads

# 配置环境变量
cp backend/.env.example backend/.env.production
# 根据需要编辑 backend/.env.production 文件
```

## 2. 前端开发
前端开发直接在本地运行，支持热更新：
```bash
cd frontend
npm install
npm run dev
```
- 开发服务器运行在 http://localhost:3000
- 自动代理 `/api` 请求到后端服务
- 代码修改后自动热更新

## 3. 后端开发

### 方式一：Docker 开发环境（推荐）
使用专门的开发环境 Docker 配置：
```bash
# 在项目根目录下运行
docker compose -f docker-compose.dev.yml up backend
```

优势：
- 与生产环境保持一致
- 自动处理依赖
- 支持代码热更新
- 避免环境配置问题

### 方式二：本地开发环境
直接在本地运行后端服务：
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 3001
```

优势：
- 更快的启动速度
- 直接使用 IDE 调试
- 更少的系统资源占用

## 4. 开发过程

### API 文档
- Swagger UI: http://localhost:3001/docs
- ReDoc: http://localhost:3001/redoc

### 健康检查
- 访问 http://localhost:3001/health 确认后端状态

### 日志查看
Docker 环境：
```bash
# 实时查看后端日志
docker compose -f docker-compose.dev.yml logs -f backend
```

本地环境：
- 日志直接输出到终端
- 日志文件保存在 `logs` 目录

## 5. 测试部署

在提交代码前，建议使用生产环境配置进行完整测试：
```bash
# 使用生产环境配置启动所有服务
docker compose up -d --build
```

## 6. 文件结构说明

### 开发配置文件
- `docker-compose.dev.yml`: 开发环境 Docker 配置
- `docker-compose.yml`: 生产环境 Docker 配置
- `docker-compose.aliyun.yml`: 阿里云环境 Docker 配置

### 环境变量文件
- `backend/.env.example`: 环境变量模板
- `backend/.env.production`: 生产环境变量配置

### 目录说明
- `frontend/`: 前端代码目录
- `backend/`: 后端代码目录
- `logs/`: 日志文件目录
- `uploads/`: 上传文件目录
- `docker/`: Docker 相关配置文件

## 7. 注意事项

1. **代码导入路径**
- Docker 环境使用 `from backend.xxx import yyy`
- 本地环境使用 `from xxx import yyy`
- `main.py` 中已配置自动处理两种环境

2. **环境变量**
- 开发时注意检查 `.env.production` 中的配置
- 确保 `ALLOWED_ORIGINS` 包含前端开发服务器地址

3. **端口使用**
- 前端开发服务器：3000
- 后端服务：3001
- 确保这些端口未被其他服务占用

4. **Docker 网络**
- 确保 `blog-network` 网络已创建
- 使用 `docker network ls` 检查网络状态

## 8. 常见问题解决

1. **后端无法启动**
- 检查端口占用
- 确认环境变量配置
- 检查 Python 依赖是否完整

2. **前端API请求失败**
- 确认后端服务运行状态
- 检查代理配置
- 验证 CORS 设置

3. **Docker 相关问题**
- 确保 Docker 服务正常运行
- 检查网络配置
- 查看容器日志排查问题

## 9. 开发建议

1. **代码提交前**
- 确保代码能在 Docker 环境中正常运行
- 测试所有主要功能
- 检查日志输出

2. **环境切换**
- 记录环境相关的配置变更
- 更新文档中的相关说明
- 通知团队成员重要变更

3. **性能优化**
- 注意日志级别设置
- 合理使用缓存
- 监控资源��用情况 