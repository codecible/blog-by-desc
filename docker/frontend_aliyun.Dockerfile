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

# 创建目录并设置权限
RUN mkdir -p /app/dist && \
    chown -R node:node /app

# 复制前端项目文件
COPY --chown=node:node frontend/package*.json ./
RUN npm ci --prefer-offline --no-audit --no-fund

# 复制源代码
COPY --chown=node:node frontend/ ./

# 切换到非root用户构建
USER node

# 构建应用
RUN npm run build

# 设置构建文件的权限
USER root
RUN chown -R node:node /app/dist && \
    chmod -R 755 /app/dist

# 切换回非root用户
USER node