# 构建阶段
FROM python:3.11.7-slim AS builder

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1

# 设置pip镜像源
ENV PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com

WORKDIR /app

# 安装构建依赖
RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 设置pip镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip config set global.trusted-host mirrors.aliyun.com

RUN pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM python:3.11.7-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DEBIAN_FRONTEND=noninteractive \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple/ \
    PIP_TRUSTED_HOST=mirrors.aliyun.com \
    PYTHONPATH=/app

WORKDIR /app

# 复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 安装运行时依赖
RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN addgroup --system --gid 1000 appgroup && \
    adduser --system --uid 1000 --ingroup appgroup --shell /bin/sh appuser

# 创建必要的目录
RUN mkdir -p logs uploads backend

# 复制后端代码
COPY backend/ backend/

# 设置目录权限
RUN chown -R appuser:appgroup /app && \
    chmod 755 logs uploads backend && \
    # 确保backend是一个Python包
    [ -f backend/__init__.py ] || touch backend/__init__.py

USER appuser

# 暴露端口
EXPOSE 3001

# 修改工作目录确保Python包导入正确
WORKDIR /app/backend

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001", "--workers", "4"]

# 容器内目录结构
# /app/
# ├── backend/          # 后端应用代码目录
# │   ├── __init__.py  # Python包标识文件
# │   ├── main.py
# │   ├── routers/
# │   └── services/
# ├── logs/            # 日志目录
# └── uploads/         # 上传文件目录

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3001/health || exit 1