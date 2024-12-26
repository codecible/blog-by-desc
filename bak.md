
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

