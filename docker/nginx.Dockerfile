# 第一阶段：构建前端
FROM node:18.19.0 AS builder

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

COPY frontend/ ./
RUN npm run build

# 第二阶段：配置nginx
FROM nginx:1.25

# 复制 Nginx 配置文件
COPY docker/nginx.conf /etc/nginx/nginx.conf

# 从构建阶段复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 设置权限
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 