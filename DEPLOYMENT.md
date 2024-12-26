# 部署和操作手册
本项目采用前后端分离架构，使用 Docker 进行容器化部署，包含三个主要服务：Nginx 服务、前端构建服务和后端服务。

> 部署配置说明
- 本地开发环境：使用 `docker compose.yml`
- 阿里云环境：使用 `docker compose.aliyun.yml`
  * 使用阿里云优化版镜像
  * 配置阿里云镜像加速
  * 阿里云内可访问的镜像资源限制

## 1. 首次部署流程
```bash
# 1. 确保 Docker 和 Docker Compose 已安装

# 2. 克隆项目代码
git clone [项目地址]
cd [项目目录]

# 3. 配置环境变量
cp backend/.env.example backend/.env.production
# 编辑 backend/.env.production 设置必要的环境变量

# 4. 创建必要的目录
mkdir -p frontend/dist logs uploads

# 5. Docker 网络配置（两种方案）

## 方案1：手动管理网络（推荐）
# 如果需要手动管理网络，执行：
docker network create blog-network
# 然后在 docker compose.yml 中使用：
networks:
  app-network:
    name: blog-network
    external: true

## 方案2：使用 docker compose 自动管理网络(不推荐)
> 不推荐使用，因为首次部署时会自动创建。但在该网络已存在情况下，会报错
# 使用 docker compose.yml 中的配置：
networks:
  app-network:
    name: blog-network
    driver: bridge

# 6. 启动所有服务
docker compose up -d --build
```

## 2. 日常开发流程

### 前端开发
```bash
# 本地开发
cd frontend
npm install
npm run dev

# 部署更新
# 方法1：使用 Docker（推荐）
docker compose up --build frontend

# 方法2：本地构建
cd frontend
npm run build
```

### 后端开发
```bash
# 本地开发
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# 部署更新
docker compose up -d --build backend
```

### Nginx 配置更新
```bash
# 修改 docker/nginx.conf 后
docker compose up -d --build nginx
```

## 3.阿里云上线
```bash
# 创建外部网络（如果尚未创建）
docker network create blog-network

# 使用阿里云专用配置启动服务
docker compose -f docker compose.aliyun.yml up -d
```

## 4. 常用运维操作

### 查看日志
```bash
# 查看所有服务日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f nginx
docker compose logs -f backend
docker compose logs -f frontend
```

### 服务管理
```bash
# 停止所有服务
docker compose down

# 重启特定服务
docker compose restart nginx
docker compose restart backend

# 查看服务状态
docker compose ps
```

### 清理和重置
```bash
# 完全清理（包括容器、网络、卷）
docker compose down -v

# 重新构建所有服务
docker compose build --no-cache
docker compose up -d
```

## 5. 故障排查指南

### 常见问题和解决方案

1. **前端构建失败**
   - 检查 frontend/package.json 是否正确
   - 检查 node_modules 是否完整
   - 查看构建日志：`docker compose logs frontend`

2. **后端服务无法启动**
   - 检查环境变量配置
   - 检查端口占用情况
   - 查看日志：`docker compose logs backend`

3. **Nginx 403 错误**
   - 检查目录权限
   - 确认前端文件是否正确构建
   - 检查 nginx.conf 配置

4. **网络连接问题**
   ```bash
   # 检查网络列表
   docker network ls
   
   # 重新创建网络（如果需要）
   docker network rm blog-network
   docker network create blog-network
   ```

## 6. 性能优化建议

1. **前端优化**
   - 启用 gzip 压缩
   - 配置适当的缓存策略
   - 优化构建输出

2. **后端优化**
   - 适当调整 worker 数量
   - 配置合理的超时时间
   - 实现请求限流

3. **Nginx 优化**
   - 配置合理的 worker 连接数
   - 启用 HTTP/2
   - 优化静态文件缓存

## 7. 安全建议

1. **配置管理**
   - 不要在代码中硬编码敏感信息
   - 使用 .env 文件管理环境变量
   - 定期更新依赖包

2. **访问控制**
   - 限制容器权限
   - 使用非 root 用户运行服务
   - 配置防火墙规则

3. **日志管理**
   - 实现日志轮转
   - 记录关键操作日志
   - 定期备份日志文件

## 后续优化方向
1. 添加容器监控
2. 实现自动化部署
3. 优化构建流程
4. 添加测试覆盖
5. 完善文档系统 