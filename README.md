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

## 系统要求

- Python 3.8+
- Monica AI API密钥（支持 GPT-4o-mini 模型）

## 安装步骤

1. 克隆项目到本地：
   ```bash
   git clone [项目地址]
   cd [项目目录]
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
   # 使用默认源安装
   pip install -r requirements.txt

   # 或使用国内镜像源安装（推荐国内用户使用）
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. 配置环境变量：
   - 复制 `.env.example` 文件为 `.env`
   - 在 `.env` 文件中设置你的 Monica AI API密钥：
     ```
     MONICA_API_KEY=your_api_key_here
     ```

## 使用方法

基本用法：
```bash
python main.py "文章描述" ["核心主题"]
```

参数说明：
- `文章描述`：（必需）描述你想要生成的文章内容
- `核心主题`：（可选）文章的核心主题或关键词

示例：
```bash
python main.py "探讨人工智能对未来教育的影响" "AI教育革命"
```

## 配置说明

在 `src/config.py` 中可以修改以下配置：

### API配置
```python
MAX_RETRIES: int = 3        # API调用最大重试次数
RETRY_DELAY: int = 2        # 重试间隔时间（秒）
API_TEMPERATURE: float = 0.7 # API温度参数
API_MAX_TOKENS: int = 2000  # 最大生成令牌数
```

### 缓存配置
```python
CACHE_ENABLED: bool = True  # 是否启用缓存
CACHE_EXPIRE_TIME: int = 3600  # 缓存过期时间（秒）
```

### 文章配置
```python
MIN_WORD_COUNT: int = 500   # 最小字数
MAX_WORD_COUNT: int = 1000  # 最大字数
```

## 输出说明

1. 生成的文章将保存在 `output` 目录下
2. 文件名格式：`YYYYMMDDHHMM.md`
3. 文件内容包括：
   - 文章标题
   - 写作方向
   - 正文内容

## 日志说明

- 日志文件位置：`logs` 目录
- 日志文件名格式：`YYYYMMDD.log`
- 记录内容：
  * API调用情况
  * 生成进度
  * 错误信息

## 常见问题

Q: API调用失败怎么办？
A: 程序会自动重试3次，每次间隔2秒。如果仍然失败，请检查：
1. API密钥是否正确
2. 网络连接是否正常
3. API额度是否充足

Q: 如何修改生成的文章长度？
A: 在 `src/config.py` 中修改 `MIN_WORD_COUNT` 和 `MAX_WORD_COUNT` 的值。

## 注意事项

1. 请确保 Monica AI API 密钥有效且有足够的调用额度
2. 生成的内容质量与输入的描述质量密切相关
3. 建议在虚拟环境中运行项目，避免依赖冲突

## 技术支持

如遇到问题，请：
1. 查看日志文件了解详细错误信息
2. 在项目 Issues 中提交问题
3. 联系技术支持

## 许可证

MIT License