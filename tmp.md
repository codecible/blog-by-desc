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


# 1. 完全清理旧的 Docker 相关配置
sudo apt remove docker docker-engine docker.io containerd runc docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/sources.list.d/docker*.list
sudo rm -f /etc/apt/keyrings/docker.gpg

# 2. 更新系统
sudo apt update
sudo apt upgrade -y

# 3. 安装必要的依赖
sudo apt install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release


# 1. 首先清理旧的 Docker 相关配置
sudo apt remove docker docker-engine docker.io containerd runc docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd
sudo rm -f /etc/apt/sources.list.d/docker.list
sudo rm -f /etc/apt/sources.list.d/docker*.list
sudo rm -f /etc/apt/keyrings/docker.gpg

# 2. 安装必要的软件包
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# 3. 添加 Docker 的 GPG 密钥（使用阿里云镜像）
curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# 4. 添加 Docker 软件源（使用阿里云镜像）
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://mirrors.aliyun.com/docker-ce/linux/debian \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. 更新软件包索引
sudo apt update

# 6. 安装 Docker
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 7. 启动 Docker
sudo systemctl start docker
sudo systemctl enable docker

# 8. 将当前用户添加到 docker 

