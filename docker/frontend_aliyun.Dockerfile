# 使用 Node.js 镜像
# FROM node:18.19.0
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/node:20.16

WORKDIR /app

# 设置npm配置
RUN npm config set registry https://registry.npmmirror.com && \
    npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-timeout 120000 && \
    npm config set strict-ssl false

# 复制前端项目文件
COPY frontend/package*.json ./
RUN npm ci --prefer-offline --no-audit --no-fund

# 复制源代码
COPY frontend/ ./

# 设置构建目录权限
RUN mkdir -p /app/dist && chown -R node:node /app

# 切换到非root用户
USER node

# 默认命令
CMD ["npm", "run", "build"]