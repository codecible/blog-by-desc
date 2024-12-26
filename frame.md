# 项目框架设计文档

## 架构概述
本项目采用前后端分离架构，使用 Docker 进行容器化部署，包含三个主要服务：Nginx 服务、前端构建服务和后端服务。

## 技术栈
- 前端：Vue.js + Vite
- 后端：Python + FastAPI
- 代理：Nginx
- 容器化：Docker + Docker Compose

## 服务架构

### 1. 服务组成
```yaml
services:
  # 1. Nginx 服务：处理反向代理和静态文件服务
  nginx:
    build:
      context: .
      dockerfile: docker/nginx.Dockerfile
    ports:
      - "80:80"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html  # 前端静态文件
      - ./docker/nginx.conf:/etc/nginx/nginx.conf  # Nginx配置
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - app-network

  # 2. 前端构建服务：只负责构建
  frontend:
    build:
      context: .
      dockerfile: docker/frontend.Dockerfile
    volumes:
      - ./frontend:/app/src  # 源代码
      - ./frontend/dist:/app/dist  # 构建输出
    command: ["npm", "run", "build"]

  # 3. 后端服务：纯业务逻辑
  backend:
    build:
      context: .
      dockerfile: docker/backend.Dockerfile
    expose:
      - "3001"
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    networks:
      - app-network
```

### 2. 目录结构
```
project/
├── docker/
│   ├── nginx.Dockerfile    # Nginx镜像构建
│   ├── frontend.Dockerfile # 前端构建镜像
│   ├── backend.Dockerfile  # 后端服务镜像
│   └── nginx.conf         # Nginx配置文件
├── frontend/
│   ├── src/               # 前端源代码
│   └── dist/              # 前端构建输出
├── backend/
│   └── ...                # 后端代码
└── docker-compose.yml     # 服务编排配置
```

## 服务职责

### 1. Nginx 服务
- 反向代理 `/api` 请求到后端服务
- 提供静态文件服务
- 处理 SSL 终止（如果需要）
- 负责基础的安全防护

### 2. 前端服务
- 负责前端代码构建
- 构建完成后自动退出
- 输出静态文件到共享卷

### 3. 后端服务
- 提供 API 服务
- 处理业务逻辑
- 管理数据存储和计算

## 工作流程

### 1. 开发环境
```bash
# 前端开发
cd frontend
npm run dev

# 后端开发
cd backend
uvicorn main:app --reload
```

### 2. 生产环境
```bash
# 首次部署
docker-compose up -d --build

# 前端代码更新
cd frontend && npm run build  # 只重新构建前端代码
# 无需重启任何容器

# 后端代码更新
docker-compose up -d --build backend

# Nginx配置更新
docker-compose up -d --build nginx
```

## 优势特点

### 1. 解耦合
- 服务职责单一，各司其职
- 可以独立更新和扩展
- 便于维护和调试

### 2. 灵活性
- 前端代码可以随时更新而不影响其他服务
- 配置更改只需要重载相关服务
- 开发更便捷

### 3. 可维护性
- 日志分离
- 配置集中管理
- 故障隔离

### 4. 性能
- Nginx 高效处理静态资源
- 后端服务专注于业务逻辑
- 可以独立扩展各个服务

## 注意事项

### 1. 安全性
- 确保卷权限正确设置
- 注意敏感信息的管理
- 定期更新依赖包

### 2. 运维管理
- 做好日志收集和监控
- 实现健康检查机制
- 建立数据备份策略

### 3. 配置管理
- 使用环境变量管理配置
- 区分开发和生产环境
- 保持配置文件的版本控制

## 后续优化方向
1. 添加容器监控
2. 实现自动化部署
3. 优化构建流程
4. 添加测试覆盖
5. 完善文档系统 