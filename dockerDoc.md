### 目录结构
```
blog-by-desc/
├── backend/
│   ├── .dockerignore    # 后端构建忽略规则
│   ├── .env.development # 开发环境配置
│   ├── .env.production  # 生产环境配置
│   └── ...
├── frontend/
│   ├── .dockerignore    # 前端构建忽略规则
│   ├── .env.development # 开发环境配置
│   ├── .env.production  # 生产环境配置
│   └── ...
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── logs/                # 日志目录
├── uploads/             # 上传文件目录
└── docker-compose.yml
```

### Docker Compose 配置
```yaml
services:
  frontend:
    build: 
      context: ./frontend
      dockerfile: ../docker/frontend.Dockerfile
    ports:
      - "8001:8001"
    env_file:
      - ./frontend/.env.production
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 500M

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/backend.Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env.production
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    networks:
      - app-network
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G

networks:
  app-network:
    driver: bridge

volumes:
  logs:
  uploads:
```

### 部署最佳实践

#### 1. 环境变量管理
- 使用`.env`文件管理不同环境的配置
- 区分开发环境(.env.development)和生产环境(.env.production)
- 通过docker-compose的env_file指定环境变量文件
- 敏感信息（如密钥、密码）应通过环境变量注入

#### 2. 网络配置
- 使用自定义bridge网络实现容器间安全通信
- 只暴露必要的端口到宿主机
- 使用depends_on确保服务启动顺序
- 配置健康检查确保服务可用性

#### 3. 持久化存储
- 使用命名卷(volumes)持久化重要数据
- 日志文件持久化到host主机
- 上传文件持久化存储
- 定期备份重要数据

#### 4. 资源管理
- 设置容器CPU和内存限制
- 配置合理的重启策略
- 监控容器资源使用情况
- 设置资源告警阈值

#### 5. 安全性建议
- 使用非root用户运行容器
- 设置只读文件系统（适用场景下）
- 定期扫描镜像安全漏洞
- 及时更新依赖和基础镜像

#### 6. 日志管理
- 使用Docker日志驱动收集日志
- 配置日志轮转防止文件过大
- 集中化日志管理
- 记录关键操作日志

#### 7. 构建优化
- 使用多阶段构建减小镜像体积
- 合理使用.dockerignore排除不需要的文件
- 优化构建缓存
- 选择合适的基础镜像
