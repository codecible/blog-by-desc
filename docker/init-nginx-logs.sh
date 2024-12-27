#!/bin/bash

# 创建nginx日志目录
mkdir -p logs/nginx

# 设置目录权限
# 766权限确保nginx用户可以读写，其他用户可以读
chmod -R 766 logs/nginx

# 如果使用非root用户运行nginx，需要修改目录所有者
# 1000是容器内nginx用户的uid
chown -R 1000:1000 logs/nginx

echo "Nginx logs directory initialized with correct permissions" 