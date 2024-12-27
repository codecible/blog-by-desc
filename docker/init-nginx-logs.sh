#!/bin/bash

# 创建nginx日志目录
mkdir -p logs/nginx

# 创建日志文件（如果不存在）
touch logs/nginx/access.log logs/nginx/error.log

# 设置目录权限
# 744权限确保nginx用户可以读写执行，其他用户只能读
chmod 744 logs/nginx
chmod 644 logs/nginx/access.log logs/nginx/error.log

# 设置所有者为nginx用户（UID 1000）
chown -R 1000:1000 logs/nginx

echo "Nginx logs directory initialized with correct permissions"
ls -la logs/nginx 