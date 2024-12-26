# 使用官方 Nginx 镜像
FROM nginx:1.25

# 复制 Nginx 配置文件
COPY docker/nginx.conf /etc/nginx/nginx.conf

# 创建静态文件目录
RUN mkdir -p /usr/share/nginx/html && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"] 