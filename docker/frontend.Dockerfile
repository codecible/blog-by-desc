# 构建阶段
FROM node:18.19.0 AS builder

WORKDIR /app

# 设置构建时环境变量
ENV VITE_API_URL=http://backend:3001

# 设置npm配置
RUN npm config set registry https://registry.npmmirror.com && \
    npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-timeout 120000 && \
    npm config set strict-ssl false

# 设置apt源为阿里云源
RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY frontend/package*.json ./

# 安装依赖（添加重试和网络超时配置）
RUN npm ci --prefer-offline --no-audit --no-fund || \
    npm ci --prefer-offline --no-audit --no-fund --registry https://registry.npm.taobao.org || \
    npm ci --prefer-offline --no-audit --no-fund --registry https://registry.npmjs.org

# 复制源代码
COPY frontend/ .

# 构建应用
RUN npm run build

# 运行阶段
FROM node:18.19.0

WORKDIR /app

# 设置npm配置
RUN npm config set registry https://registry.npmmirror.com && \
    npm config set fetch-retries 5 && \
    npm config set fetch-retry-mintimeout 20000 && \
    npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-timeout 120000 && \
    npm config set strict-ssl false

# 设置apt源为阿里云源
RUN echo "deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 设置目录权限
RUN chown -R node:node /app

# 复制构建产物和必要文件
COPY --from=builder --chown=node:node /app/dist ./dist
COPY --from=builder --chown=node:node /app/package*.json ./
COPY --from=builder --chown=node:node /app/node_modules ./node_modules

# 切换到非root用户，镜像中会默认存在node用户
USER node

# 暴露端口
EXPOSE 3000

# 启动命令
# 启动命令说明:
# npm run preview: 运行Vite的预览模式,用于预览生产构建后的应用
# --: 分隔npm命令和后续参数
# --host "0.0.0.0": 允许从任何IP地址访问应用(不仅限于localhost)
# --port "3000": 在容器内使用3000端口提供服务
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "3000"]