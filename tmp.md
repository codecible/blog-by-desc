# 1. 首先停止所有容器
docker-compose down

# 2. 删除网络
docker network rm blog-by-desc_app-network blog-by-desc_default blog-network

# 如果某个网络删除失败（提示有容器在使用），可以先检查：
docker network inspect blog-by-desc_app-network
docker network inspect blog-by-desc_default
docker network inspect blog-network

# 如果确实有容器还在使用，可以强制删除：
docker network disconnect -f blog-by-desc_app-network [容器ID]
docker network disconnect -f blog-by-desc_default [容器ID]
docker network disconnect -f blog-network [容器ID]