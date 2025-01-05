# 构建阶段
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1 AS builder

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
RUN yum install -y gcc gcc-c++ make curl \
    && yum clean all \
    && rm -rf /var/cache/yum

# 复制依赖文件
COPY backend/requirements.txt .

# 创建虚拟环境并安装依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 设置pip镜像源
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ \
    && pip config set global.trusted-host mirrors.aliyun.com

RUN pip install --no-cache-dir -r requirements.txt

# 运行阶段
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/python:3.11.1

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
RUN yum install -y curl ca-certificates \
    && yum clean all \
    && rm -rf /var/cache/yum

# 创建非root用户
RUN groupadd -r -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup -s /bin/bash appuser

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
WORKDIR /app

# 启动命令
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "3001", "--workers", "4"]

# 容器内目录结构
# /app/
# ├── backend/          # 后端应用代码目录
# │   ├── __init__.py  # Python包标识文件
# │   ├── main.py
# │   ├── routers/
# │   └── services/
# ├── logs/            # 日志目录
# └── uploads/         # 上传文件目录
