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

## 快速开始
参考 项目架构文档[frame.md](frame.md)

## 快速开始
参考 项目架构文档[frame.md](frame.md)

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

