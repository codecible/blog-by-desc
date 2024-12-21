# AI 文章生成器

这是一个基于Monica AI的智能文章生成工具，可以根据用户提供的描述和核心主题自动生成高质量的文章。

## 功能特点

- 🚀 自动生成3-5个写作方向
- 📝 智能生成文章标题
- 📚 生成500-1000字的文章内容
- 💾 自动保存为Markdown格式
- 🔄 支持异步处理提高性能
- 📦 内置缓存机制减少API调用
- 🛡️ 完善的错误处理和重试机制
- 📊 详细的日志记录
- 🎯 支持自定义角色设定
- 🔍 多样化的写作风格

## 项目结构

```
blog-by-desc/
├── backend/                 # 后端代码目录
│   ├── __init__.py         # Python包初始化文件
│   ├── main.py             # 主程序入口
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python依赖包
│   ├── services/           # 服务层目录
│   │   ├── __init__.py
│   │   └── blog_generator.py  # 文章生成服务
│   ├── utils/              # 工具函数目录
│   │   ├── __init__.py
│   │   └── logger.py       # 日志工具
│   ├── models/             # 数据模型目录
│   ├── routers/            # 路由目录
│   └── tests/              # 测试目录
├── frontend/               # 前端代码目录
├── output/                 # 生成的文章输出目录
├── docker/                 # Docker相关配置
├── .env.example           # 环境变量示例文件
└── .gitignore             # Git忽略文件
```

## 系统要求

- Python 3.8+
- Monica AI API密钥（支持 GPT-4o-mini 模型）
- OpenAI Python SDK (>=1.3.0)

## 安装步骤

1. 克隆项目到本地：
   ```bash
   git clone [项目地址]
   cd blog-by-desc
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

4. 配置环境变量：
   - 复制项目根目录下的 `.env.example` 文件为 `.env`
   - 在 `.env` 文件中设置你的 Monica AI API密钥：
     ```
     MONICA_API_KEY=your_api_key_here
     ```

## 使用方法

基本用法：
```bash
# 在项目根目录下运行
python -m backend.main "文章描述" ["核心主题"]
```

参数说明：
- `文章描述`：（必需）描述你想要生成的文章内容
- `核心主题`：（可选）文章的核心主题或关键词

示例：
```bash
python -m backend.main "探讨人工智能对未来教育的影响" "AI教育革命"
```

## 生成流程说明

### 1. 生成写作方向
- 由资深内容策划专家角色生成
- 紧密结合描述内容和核心主题
- 考虑当前社会热点与读者兴趣
- 输出3-5个清晰的写作方向

### 2. 生成文章标题
- 由自媒体内容策划专家角色生成
- 标题长度控制在10-25字之间
- 优先使用数字/具体数据
- 包含吸引眼球的关键词
- 生成3个备选标题供选择

### 3. 生成文章内容
- 由经验丰富的自媒体创作者角色生成
- 确保内容结构清晰，层层递进
- 使用通俗易懂的语言
- 通过故事化叙述增加趣味性
- 适当加入数据支持论点

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

## 常见问题

Q: API调用失败怎么办？
A: 程序会自动重试，如果仍然失败，请检查：
1. API密钥是否正确
2. 网络连接是否正常
3. API额度是否充足

Q: 如何修改生成的文章风格？
A: 可以修改 `backend/services/blog_generator.py` 中各个生成方法的 system 角色设定。

Q: 为什么运行时提示模块找不到？
A: 请确保：
1. 在项目根目录下运行命令
2. 使用 `python -m backend.main` 的方式运行
3. 已正确安装所有依赖

## 注意事项

1. 请确保 Monica AI API 密钥有效且有足够的调用额度
2. 生成的内容质量与输入的描述质量密切相关
3. 建议在虚拟环境中运行项目，避免依赖冲突
4. 确保系统安装了 Python 3.8 或更高版本

## 技术支持

如遇到问题，请：
1. 查看日志文件了解详细错误信息
2. 在项目 Issues 中提交问题
3. 联系技术支持

## 许可证

MIT License