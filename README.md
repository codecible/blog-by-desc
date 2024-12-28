# AI 文章生成器 v0.2.0

这是一个基于Monica AI的智能文章生成工具，可以根据用户提供的描述和核心主题自动生成高质量的文章。现在支持多种AI提供商，包括Monica AI和智谱AI。

## 最新更新

- ✨ 全新的用户界面，采用简洁友好的设计风格
- 📝 支持一键复制和下载文章
- 🎨 优化的文章展示效果
- 📱 完善的移动端适配
- 🚀 更流畅的用户体验
- 🔒 支持Docker Compose快速部署
- 🌩️ 支持预发布和阿里云环境部署
- 🔄 支持多AI提供商切换（Monica AI / 智谱AI）
- ⚡️ 优化的配置管理，使用单例模式提高性能

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
- 🔀 支持多AI提供商灵活切换
- ⚡️ 高效的配置管理机制

## 技术栈
- 前端：Vue.js + Vite + Element Plus
  * Vue.js 3.0 - 渐进式JavaScript框架
  * Vite - 下一代前端构建工具
    - 基于原生 ES 模块的开发服务器
    - 快速的冷启动和热更新
    - 内置对 TypeScript、JSX、CSS 等的支持
    - 优化的构建输出，支持代码分割
    - 插件化架构，高度可扩展
  * Element Plus - 基于Vue 3的组件库
- 后端：Python + FastAPI
  * Python 3.11 - 高性能的解释型语言
  * FastAPI - 现代、快速的Web框架
    - 基于Python 3.6+类型提示的API接口开发
    - 极快的性能，与 NodeJS 和 Go 相当
    - 自动生成交互式API文档
    - 内置数据验证和序列化
    - 支持异步编程和WebSocket
    - 完整的IDE支持和类型检查
- 代理：Nginx
- 容器化：Docker + Docker Compose

## 配置说明

### 环境变量配置
- `AI_PROVIDER`: AI提供商选择（"monica"或"zhipu"）
- `MONICA_API_KEY`: Monica AI的API密钥
- `ZHIPU_API_KEY`: 智谱AI的API密钥
- `MONICA_MODEL`: Monica AI的模型名称
- `ZHIPU_MODEL`: 智谱AI的模型名称

### 配置管理特性
- 使用单例模式管理配置，确保全局配置一致性
- 支持运行时动态切换AI提供商
- 自动验证配置有效性
- 详细的配置加载日志

## 部署说明
参见[DEPLOYMENT.md](DEPLOYMENT.md)

## 项目结构

```
blog-by-desc/
├── backend/                 # 后端代码目录
│   ├── __init__.py         # Python包初始化文件
│   ├── main.py             # Web服务入口
│   ├── config.py           # 配置管理
│   ├── requirements.txt    # Python依赖包
│   ├── .env.example        # 环境变量示例文件
│   ├── .env                # 环境变量配置文件
│   ├── routers/            # 路由处理目录
│   │   └── article.py      # 文章相关路由
│   ├── services/           # 服务层目录
│   │   └── article_generator.py  # 文章生成服务
│   ├── models/             # 数据模型目录
│   │   └── article.py      # 文章数据模型
│   └── utils/              # 工具函数目录
│       ├── logger.py       # 日志工具
│       └── api_client/     # API客户端目录
│           ├── monica.py   # Monica AI客户端
│           └── zhipu.py    # 智谱AI客户端
├── frontend/               # 前端代码目录
│   ├── src/               # 源代码目录
│   │   ├── components/    # Vue组件目录
│   │   │   ├── ArticleForm.vue    # 文章生成表单组件
│   │   │   └── ArticlePreview.vue # 文章预览组件
│   │   ├── router/        # 路由配置目录
│   │   │   └── index.js   # 路由配置文件
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 应用入口文件
│   ├── public/            # 静态资源目录
│   ├── package.json       # 项目依赖配置
│   └── vite.config.js     # Vite配置文件
├── docker/                # Docker相关配置
│   ├── backend_aliyun.Dockerfile    # 阿里云专用后端Dockerfile
│   ├── frontend_aliyun.Dockerfile   # 阿里云专用前端Dockerfile
│   ├── nginx_aliyun.Dockerfile      # 阿里云专用Nginx Dockerfile
│   ├── nginx.conf                   # Nginx配置文件
│   └── init-nginx-logs.sh           # Nginx日志初始化脚本
├── logs/                            # 日志目录
│   ├── app/                         # 应用日志
│   └── nginx/                       # Nginx日志
├── docker-compose.pre.yml           # 预发布环境配置
├── docker-compose.aliyun.yml        # 阿里云环境配置
├── DEPLOYMENT.md                    # 部署说明文档
├── CHANGELOG.md                     # 更新日志
└── .gitignore                       # Git忽略文件
```

### 目录功能说明

#### backend/ - 后端服务
- `main.py`: Web服务入口，配置FastAPI应用
- `config.py`: 配置管理，使用单例模式实现
- `routers/`: API路由处理，包含所有HTTP端点
  * 1. 处理HTTP请求路由
  * 2. 参数验证和错误处理
  * 3. 调用相应的服务层处理业务逻辑
  * 4. 返回处理结果
- `services/`: 核心业务逻辑实现
  * 1. 实现核心业务逻辑
  * 2. 调用外部API服务
  * 3. 处理数据转换和数据验证
  * 4. 实现缓存机制
  * 5. 错误处理和重试机制
- `models/`: 数据模型定义
  * 1. 定义数据模型和数据结构
  * 2. 提供数据验证规则
    - 字段类型检查
    - 长度限制
    - 格式验证
    - 自定义验证规则
  * 3. 实现数据转换和序列化
  * 4. 提供模型间的关系映射
- `utils/`: 工具函数和API客户端实现

#### frontend/ - 前端应用
- `src/components/`: Vue组件，实现UI交互
- `src/router/`: 前端路由配置
- `public/`: 静态资源文件
- `vite.config.js`: Vite构建工具配置

#### docker/ - 容器化配置
- 包含所有环境的Dockerfile
- Nginx配置和日志管理
- 支持本地开发、预发布和阿里云环境

#### logs/ - 日志管理
- `app/`: 应用程序日志
- `nginx/`: Nginx访问和错误日志

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
