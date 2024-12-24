# AI 文章生成器 v0.2.0

这是一个基于Monica AI的智能文章生成工具，可以根据用户提供的描述和核心主题自动生成高质量的文章。

## 最新更新

- ✨ 全新的用户界面，采用简洁友好的设计风格
- 📝 支持一键复制和下载文章
- 🎨 优化的文章展示效果
- 📱 完善的移动端适配
- 🚀 更流畅的用户体验
- 🔒 Docker-compose部署

## 功能特点

- 🚀 自动生成3-5个写作方向
- 📝 智能生成文章标题
- 📚 生成500-1000字的文章内容
- 💾 自动保存为Markdown格式
- 🔄 支持异步处理提高性能
- 📦 内置缓存机制减少API调用
- 🛡️ 完善的错误处理和重试机制
- 📊 详细的日志记录
- 📱 响应式设计，支持移动端
- 📋 一键复制文章内容
- 💾 下载为Markdown文件
- 🔄 支持返回编辑功能

## 技术栈
- 前端：Vue 3 + Vite + Element Plus + Pinia
- 后端：Python FastAPI
- 开发工具：VSCode
- 包管理：npm(前端)、pip(后端)
- 容器化：Docker Compose

## 环境要求
- Docker Compose >= 2.0.0
- VSCode + Remote Container 插件(推荐 Dev Container)

## 项目结构

```
blog-by-desc/
├── backend/                 # 后端代码目录
│   ├── __init__.py         # Python包初始化文件
│   ├── main.py             # Web服务入口
│   ├── cli.py              # 命令行工具入口
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python依赖包
│   ├── .env.example        # 环境变量示例文件
│   ├── .env                # 环境变量配置文件
│   ├── routers/            # 路由处理目录
│   │   └── article.py      # 文章相关路由
│   ├── services/           # 服务层目录
│   │   └── article_generator.py  # 文章生成服务
│   ├── schemas/            # 数据验证模型目录
│   │   ├── __init__.py     # 包初始化文件
│   │   ├── article.py      # 文章相关的数据模型
│   │   ├── base.py         # 基础数据模型
│   │   └── errors.py       # 错误响应模型
│   ├── models/             # 数据模型目录
│   │   └── article.py      # 文章数据模型
│   ├── utils/              # 工具函数目录
│   │   └── logger.py       # 日志工具
│   └── tests/              # 测试目录
├── frontend/               # 前端代码目录
│   ├── src/               # 源代码目录
│   │   ├── components/    # Vue组件目录
│   │   │   ├── ArticleForm.vue    # 文章生成表单组件
│   │   │   └── ArticlePreview.vue # 文章预览组件
│   │   ├── router/        # 路由配置目录
│   │   │   └── index.js   # 路由配置文件
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 应用入口文件
│   ├── css/               # 样式文件目录
│   ├── js/                # JavaScript文件目录
│   ├── index.html         # HTML入口文件
│   ├── package.json       # 项目依赖配置
│   ├── vite.config.js     # Vite配置文件
│   └── .npmrc             # NPM配置文件
├── output/                 # 生成的文章输出目录
├── logs/                   # 日志输出目录
├── docker/                 # Docker相关配置
└── .gitignore             # Git忽略文件
```

### 目录功能详细描述

#### backend/routers
1. 处理HTTP请求路由
2. 参数验证和错误处理
3. 调用相应的服务层处理业务逻辑
4. 返回处理结果

#### backend/schemas
1. 定义请求和响应的数据模型
2. 提供数据验证规则
   - 字段类型检查
   - 长度限制
   - 格式验证
   - 自定义验证规则
3. 自动生成API文档
   - 请求/响应模型说明
   - 字段说明
   - 示例数据
4. 错误处理模型
   - 统一的错误响应格式
   - 错误码定义
   - 详细的错误信息

#### backend/services
1. 实现核心业务逻辑
2. 调用外部API服务
3. 处理数据转换
4. 实现缓存机制

## 安装步骤

1. 克隆项目到本地：
   ```bash
   git clone [项目地址]
   cd blog-by-desc
   ```
2. 配置环境变量：
   - 复制 `backend/.env.example` 文件为 `backend/.env`
   - 在 `backend/.env` 文件中设置你的 Monica AI API密钥：
     ```
     MONICA_API_KEY=your_api_key_here
     ```

2. 创建并激活虚拟环境（推荐）：
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖包：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```



## 使用方法

```cmd
# 后端服务启动
uvicorn backend.main:app --reload

# 前端服务启动
cd frontend && npm run dev
```

### 后端服务启动
提供两种使用方式：命令行工具和Web API服务。

#### 1. Web API服务使用方法

启动Web服务：
```bash
# 开发模式启动（支持自动重载）
uvicorn backend.main:app --reload

# 生产模式启动
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

#### 2. 命令行工具使用方法

通过命令行直接生成文章：

```bash
# 基本用法
python -m backend.cli <文章描述> [核心主题]

# 示例
python -m backend.cli "探讨人工智能对未来教育的影响" "AI教育革命"
```

参数说明：
- `文章描述`：（必需）描述你想要生成的文章内容
- `核心主题`：（可选）文章的核心主题或关键词



## API接口：

1. 访问API文档：
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc



## 配置说明

在 `backend/config.py` 中可以修改以下配置：

### API配置
```python
API_ENDPOINT = "https://openapi.monica.im/v1"  # Monica API的基础URL
AI_MODEL = "gpt-4o-mini"                       # 使用的AI模型
API_TEMPERATURE = 0.7                          # 控制输出的随机性 (0.0-1.0)
API_MAX_TOKENS = 2000                          # 限制输出的最大长度
MAX_RETRIES = 1                                # 最大重试次数
RETRY_DELAY = 2                                # 重试延迟时间（秒）
```

### 日志配置
```python
LOG_LEVEL = "INFO"         # 日志级别
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"  # 日志格式
```

## 输出说明

1. 生成的文章将保存在项目根目录的 `output` 目录下
2. 文件名格式：`YYYYMMDDHHMM.md`
3. 文件内容包括：
   - 文章标题
   - 写作方向列表
   - 正文内容

## 日志说明

- 日志文件位置：项目根目录下的 `logs` 目录
- 日志文件名格式：`YYYYMMDD.log`
- 记录内容：
  * API调用情况
  * 生成进度
  * 错误信息

## 技术支持

如遇到问题，请：
1. 查看日志文件了解详细错误信息
2. 在项目 Issues 中提交问题
3. 联系技术支持

## 许可证

MIT License

## API文档

### 1. 文档访问
- Swagger UI: http://localhost:8000/docs
  * 交互式API文档
  * 支持在线测试API
  * 查看请求/响应模型
  * 查看验证规则
- ReDoc: http://localhost:8000/redoc
  * 更清晰的文档阅读体验
  * 适合分享给团队成员

### 2. 请求/响应格式

#### 2.1 文章生成请求
```json
{
    "description": "探讨人工智能对未来教育的影响",
    "core_idea": "AI教育革命"
}
```
- `description`: 文章描述（必填，5-1000字）
- `core_idea`: 核心主题（选填，最多100字）

#### 2.2 成功响应
```json
{
    "success": true,
    "message": "文章生成成功",
    "data": {
        "title": "揭秘AI如何定制个性化学习，提升学生成绩的3大关键",
        "content": "# 揭秘AI如何定制个性化学习...",
        "directions": [
            "个性化学习：AI如何根据学生需求定制教育内容",
            "教师角色转变：AI在课堂中的辅助与替代",
            "未来技能培养：AI时代需要的核心素养"
        ],
        "file_path": "output/202312211234.md"
    }
}
```

#### 2.3 错误响应
```json
{
    "code": 400,
    "message": "请求参数错误",
    "details": "文章描述不能为空"
}
```

### 3. 错误码说明
- 400: 请求参数错误
- 404: 资源未找到
- 500: 服务器内部错误

### 4. 数据验证规则
- 文章描述：
  * 必填字段
  * 最小长度：5个字符
  * 最大长度：1000个字符
- 核心主题：
  * 选填字段
  * 最大长度：100个字符

### 5. 响应字段说明
- `success`: 请求是否成功
- `message`: 响应消息
- `data`: 文章数据
  * `title`: 生成的文章标题
  * `content`: 生成的文章内容（Markdown格式）
  * `directions`: 文章的写作方向列表
  * `file_path`: 文章保存的文件路径

## 使用Docker Compose部署

1. 确保已安装Docker和Docker Compose
   ```bash
   docker --version
   docker-compose --version
   ```

2. 配置环境变量
   ```bash
   cp ./backend/.env.example ./backend/.env
   # 编辑.env文件，设置MONICA_API_KEY
   ```

3. 构建和启动服务
   ```bash
   # 构建镜像并启动容器
   docker-compose up --build

   # 后台运行
   docker-compose up -d --build
   ```

4. 访问服务
   - 前端页面：http://localhost:5173
   - 后端API文档：http://localhost:8000/docs

5. 停止服务
   ```bash
   # 停止并移除容器
   docker-compose down

   # 停止并移除容器及镜像
   docker-compose down --rmi all
   ```

### Docker开发提示

1. 查看容器日志
   ```bash
   # 查看所有容器日志
   docker-compose logs

   # 查看特定服务日志
   docker-compose logs backend
   docker-compose logs frontend
   ```

2. 进入容器
   ```bash
   # 进入后端容器
   docker-compose exec backend bash

   # 进入前端容器
   docker-compose exec frontend sh
   ```

3. 重启服务
   ```bash
   # 重启所有服务
   docker-compose restart

   # 重启特定服务
   docker-compose restart backend
   docker-compose restart frontend
   ```

4. 开发模式
   - 已配置热重载，修改代码后会自动更新
   - 前端代码修改会自动编译
   - 后端代码修改会自动重启服务

5. 常见问题
   - 如果遇到权限问题，可能需要调整目录权限：
     ```bash
     sudo chown -R $USER:$USER .
     ```
   - 如果端口被占用，可以在docker-compose.yml中修改端口映射

## 快速开始

### 1. Docker部署（推荐）

这是最简单的启动方式，确保你已安装：
- Docker >= 20.10.0
- Docker Compose >= 2.0.0

```bash
# 1. 克隆项目
git clone [项目地址]
cd blog-by-desc

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 MONICA_API_KEY

# 3. 启动服务
docker-compose up -d --build

# 4. 访问服务
# 前端界面：http://localhost:5173
# API文档：http://localhost:8000/docs
```

### 2. 本地开发环境（可选）

如果你想在本地开发，请参考[开发环境设置](#开发环境设置)部分。

## Docker部署详解

### 目录结构
```
blog-by-desc/
├── backend/
│   ├── .dockerignore    # 后端构建忽略规则
│   └── ...
├── frontend/
│   ├── .dockerignore    # 前端构建忽略规则
│   └── ...
├── docker/
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
└── docker-compose.yml
```

### 部署说明

1. 服务组件
   - 后端服务（Python FastAPI）
     * 运行在 8000 端口
     * 使用非root用户运行
     * 支持热重载开发
   - 前端服务（Vue.js）
     * 运行在 5173 端口
     * 支持热更新
     * 自动编译

2. 数据持久化
   ```yaml
   volumes:
     - ./backend:/app/backend:ro  # 源代码（只读）
     - ./output:/app/output       # 生成的文章
     - ./logs:/app/logs          # 日志文件
   ```

3. 环境变量
   - 在 `.env` 文件中配置
   - 支持的变量：
     * `MONICA_API_KEY`：API密钥
     * 其他配置参见 `.env.example`

4. 安全特性
   - 使用非root用户运行容器
   - 源代码目录只读挂载
   - 合理的文件权限设置
   - 独立的构建上下文

### 常用操作

1. 服务管理
   ```bash
   # 启动服务
   docker-compose up -d

   # 停止服务
   docker-compose down

   # 重启服务
   docker-compose restart

   # 查看日志
   docker-compose logs -f
   ```

2. 开发模式
   ```bash
   # 启动开发模式（带实时日志）
   docker-compose up

   # 重新构建（代码更新后）
   docker-compose up --build
   ```

3. 容器管理
   ```bash
   # 进入容器
   docker-compose exec backend bash
   docker-compose exec frontend sh

   # 查看容器状态
   docker-compose ps
   ```

4. 文件权限（如果遇到权限问题）
   ```bash
   # 设置目录权限
   sudo chown -R $USER:$USER .
   sudo chmod -R 755 .
   ```

### 故障排除

1. 容器无法启动
   - 检查端口占用：`lsof -i :8000` 和 `lsof -i :5173`
   - 检查日志：`docker-compose logs`
   - 确认环境变量已正确设置

2. 文件权限问题
   - 运行权限修复命令（见上文）
   - 确认 output 和 logs 目录存在且有正确权限

3. 热重载不工作
   - 检查 volume 挂载是否正确
   - 确认代码保存时没有语法错误

4. API调用失败
   - 验证 MONICA_API_KEY 是否正确设置
   - 检查网络连接
   - 查看后端日志

## 最佳实践

1. 开发流程
   - 使用 Docker 开发环境保持一致性
   - 遵循代码规范和提交规范
   - 定期更新依赖版本

2. 部署建议
   - 生产环境使用固定版本标签
   - 定期备份 output 目录
   - 监控容器日志和状态

3. 安全建议
   - 定期更新基础镜像
   - 不在容器中存储敏感信息
   - 使用非root用户运行服务
   - 限制容器资源使用