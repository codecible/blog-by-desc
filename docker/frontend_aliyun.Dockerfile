FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/node:20.16

# 确保使用 root 用户
USER root

WORKDIR /app

# 设置npm配置
RUN npm config set registry https://registry.npmmirror.com && \
    npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-timeout 120000 && \
    npm config set strict-ssl false

# 确保 node 用户和组存在
RUN getent group node || groupadd -r node && \
    getent passwd node || useradd -r -g node -m node

# 创建目录并设置权限（添加详细的错误处理）
RUN set -e; \
    mkdir -p /app/dist; \
    chown -R node:node /app || { echo "Failed to change ownership"; exit 1; }; \
    ls -la /app

# 复制前端项目文件
COPY --chown=node:node frontend/package*.json ./
RUN npm ci --prefer-offline --no-audit --no-fund

# 复制源代码
COPY --chown=node:node frontend/ ./

# 切换到非root用户
USER node

# 默认命令
CMD ["npm", "run", "build"]