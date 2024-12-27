# 部署和操作手册

## 环境要求
- Python 3.11 或 3.12（不支持 Python 3.13）
- Node.js 18+ LTS 版本
- Rust 工具链（用于编译某些依赖，通过 https://rustup.rs/ 安装）
- Docker 和 Docker Compose（用于容器化部署）

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
mkdir -p logs/nginx && chmod -R 777 logs/nginx

# 5. Docker 网络配置（两种方案）

## 方案1：手动管理网络（推荐&默认）
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
docker compose -f docker-compose.pre.pre.yml up -d --build
```

## 2. 日常开发流程

### 前端开发
```bash
# 本地开发
cd frontend
npm install #首次执行/或者有新的插件安装
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
# 基于项目根目录
python3.11 -m venv venv              # 创建新的虚拟环境
source venv/bin/activate         # 激活虚拟环境
pip install --upgrade pip        # 升级pip
pip install -r requirements.txt  # 安装依赖

# 开启热重载
# 方式1：使用默认配置
# 默认配置说明：
# --host: 监听的网络接口
#   - 127.0.0.1: 只允许本机访问
#   - 0.0.0.0: 允许所有网络接口访问（包括局域网和远程访问）
# --port: 监听的端口号（默认为8000, Uvicorn的默认端口）
# --reload: 启用热重载，代码修改后自动重启
# --workers: 工作进程数（默认为1）
# --log-level: 日志级别（默认为info）
python3.11 -m uvicorn backend.main:app --reload

# 方式2：自定义配置
# 仅本地访问
python -m uvicorn backend.main:app --host 127.0.0.1 --port 3001 --reload
# 允许局域网访问
python -m uvicorn backend.main:app --host 0.0.0.0 --port 3001 --reload
```

## 3.预览环境
- 上线前在预览环境进行测试访问，和正式环境更新一样，均采用docker compose
```bash
# 创建外部网络（如果尚未创建）
docker network create blog-network

# 使用阿里云专用配置启动服务
docker compose -f docker-compose.pre.yml up -d
```

## 4.正式上线
```bash
# 创建外部网络（如果尚未创建）
docker network create blog-network

# 使用阿里云专用配置启动服务
docker compose -f docker-compose.aliyun.yml up -d
```

## 4. 常用运维操作

### 查看日志
```bash
# 查看所有服务日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f nginx
```t

### 服务管理
```bash
# 停止所有服务
docker compose down

# 重启特定服务
docker compose restart nginx

# 查看服务状态
docker compose ps
```

### 清理和重置
```bash
# 完全清理（包括容器、网络、卷）
docker compose down -v

# 重新构建所有服务
docker compose [-f docker-compose.aliyun.yml] up [-d] [--build [--no-cache] [nginx]]
```


## 各容器关联
1. frontend容器负责构建(build)，完成后自动退出
2. 构建产物通过volume(frontend_build)持久化
3. nginx容器挂载这个volume来提供静态文件服务