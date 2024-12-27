# 使用官方 Nginx 镜像
FROM alibaba-cloud-linux-3-registry.cn-hangzhou.cr.aliyuncs.com/alinux3/nginx_optimized:20240221-1.20.1-2.3.0

# 复制 Nginx 配置文件
COPY docker/nginx.conf /etc/nginx/nginx.conf

# 创建必要的目录并设置权限
RUN mkdir -p /usr/share/nginx/html \
    /var/cache/nginx \
    /var/log/nginx \
    /tmp/nginx \
    && chown -R nginx:nginx /usr/share/nginx/html \
    /var/cache/nginx \
    /var/log/nginx \
    /tmp/nginx \
    && chmod -R 755 /usr/share/nginx/html \
    /var/cache/nginx \
    /tmp/nginx \
    && chmod -R 766 /var/log/nginx

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

EXPOSE 80

# 使用nginx用户运行
USER nginx

CMD ["nginx", "-g", "daemon off;"] 