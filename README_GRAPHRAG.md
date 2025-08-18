# GraphRAG 项目部署与使用指南

## 📋 项目概述

这是一个基于Microsoft GraphRAG的知识图谱增强检索生成系统，已配置完成并可以运行。系统包含了完整的环境设置、示例数据、查询接口（Gradio UI和FastAPI）。

## ✅ 已完成的配置

### 1. 环境准备 ✓
- Python虚拟环境已创建 (`.venv`)
- 所有依赖已安装（包括GraphRAG、PyTorch、Transformers等）
- 项目已配置为可编辑模式安装

### 2. API配置 ✓
- `.env`文件模板已创建（需要添加实际的API密钥）
- 支持OpenAI和Azure OpenAI配置

### 3. GraphRAG初始化 ✓
- 项目结构已初始化 (`graphrag_project/`)
- 配置文件已优化 (`settings.yaml`)

### 4. 示例数据 ✓
已准备多个领域的中文文档：
- 量子计算 (`quantum_computing.txt`)
- 人工智能 (`artificial_intelligence.txt`)
- 区块链技术 (`blockchain_technology.txt`)
- 5G网络 (`5g_network.txt`)
- 云计算 (`cloud_computing.txt`)
- 技术趋势JSON数据 (`technology_trends.json`)

### 5. 查询服务 ✓
- **Gradio Web UI** (`gradio_app.py`) - 可视化问答界面
- **FastAPI REST API** (`api_server.py`) - RESTful API服务
- **测试脚本** (`test_query.py`) - 功能测试工具

## 🚀 快速开始

### 1. 激活虚拟环境
```bash
source .venv/bin/activate
```

### 2. 配置API密钥
编辑 `.env` 文件，添加您的OpenAI API密钥：
```bash
nano graphrag_project/.env
# 将 OPENAI_API_KEY="sk-xxxx" 替换为实际密钥
```

### 3. 构建知识图谱（需要API密钥）
```bash
python build_graph.py
```
或使用GraphRAG CLI：
```bash
graphrag index --root ./graphrag_project
```

### 4. 启动查询服务

#### 方式1: Gradio Web UI
```bash
python gradio_app.py
```
访问: http://localhost:7860

#### 方式2: FastAPI REST API
```bash
uvicorn api_server:app --reload --port 8000
```
访问: 
- API文档: http://localhost:8000/docs
- 健康检查: http://localhost:8000/health

### 5. 测试功能
```bash
# 测试本地模块
python test_query.py --mode local

# 测试API服务器（需要先启动api_server）
python test_query.py --mode api

# 测试两者
python test_query.py --mode both
```

## 📁 项目结构

```
/workspace/
├── .venv/                      # Python虚拟环境
├── graphrag_project/           # GraphRAG项目目录
│   ├── data/                   # 输入数据文档
│   │   ├── quantum_computing.txt
│   │   ├── artificial_intelligence.txt
│   │   ├── blockchain_technology.txt
│   │   ├── 5g_network.txt
│   │   ├── cloud_computing.txt
│   │   └── technology_trends.json
│   ├── storage/                # 知识图谱存储（构建后生成）
│   ├── cache/                  # 缓存目录
│   ├── output/                 # 输出报告
│   ├── prompts/                # 提示词模板
│   ├── settings.yaml           # GraphRAG配置
│   └── .env                    # API密钥配置
├── scripts/
│   └── generate_sample_data.py # 数据生成脚本
├── build_graph.py              # 图谱构建脚本
├── gradio_app.py               # Gradio Web界面
├── api_server.py               # FastAPI服务器
├── test_query.py               # 测试脚本
├── requirements-essential.txt  # 依赖列表
└── README_GRAPHRAG.md          # 本文档
```

## 🔧 配置说明

### settings.yaml 关键配置
- **模型**: 默认使用 `gpt-3.5-turbo`（可改为 `gpt-4`）
- **块大小**: 1024 tokens
- **并发请求**: 5（避免速率限制）
- **嵌入模型**: `text-embedding-3-small`

### API速率限制
- 请求/分钟: 20
- Tokens/分钟: 10000

## 📊 功能特性

### Gradio界面功能
- 交互式问答界面
- Local/Global搜索模式切换
- 对话历史记录
- 置信度显示
- 数据源追踪

### FastAPI功能
- RESTful API端点
- Swagger文档
- 健康检查
- 批量查询支持
- CORS支持

## 🛠️ 故障排除

### 常见问题

1. **依赖冲突**
```bash
pip uninstall -y $(pip freeze) && pip install -r requirements-essential.txt
```

2. **API连接失败**
- 检查 `.env` 中的API密钥
- 确认网络连接
- 使用代理（如需要）：
```python
os.environ["HTTP_PROXY"] = "http://proxy:port"
```

3. **内存不足（OOM）**
- 减小 `chunk_size`
- 使用更小的模型
- 减少并发请求数

4. **图谱未加载**
- 确保已运行 `graphrag index` 构建图谱
- 检查 `storage/` 目录是否有输出文件

## 📚 示例查询

系统已配置以下领域的知识：

1. **量子计算**
   - "什么是量子计算？"
   - "量子计算的应用有哪些？"

2. **人工智能**
   - "AI的发展历程是怎样的？"
   - "深度学习的核心技术有哪些？"

3. **区块链**
   - "区块链的核心特性是什么？"
   - "智能合约如何工作？"

4. **5G网络**
   - "5G与4G的区别是什么？"
   - "5G的关键技术有哪些？"

5. **云计算**
   - "云计算的服务模型有哪些？"
   - "公有云和私有云的区别？"

## 🔐 安全注意事项

1. **API密钥管理**
   - 不要将API密钥提交到版本控制
   - 使用环境变量管理敏感信息
   - 定期轮换密钥

2. **生产环境部署**
   - 限制CORS来源域名
   - 启用HTTPS
   - 实施速率限制
   - 添加身份验证

## 📈 性能优化建议

1. **减少API调用**
   - 使用缓存机制
   - 批量处理请求
   - 考虑使用本地嵌入模型

2. **提高处理速度**
   - 调整并发请求数
   - 优化块大小
   - 使用更快的模型

3. **降低成本**
   - 使用 `gpt-3.5-turbo` 而非 `gpt-4`
   - 减少 `max_tokens`
   - 启用智能缓存

## 🤝 贡献与支持

- GraphRAG官方文档: https://microsoft.github.io/graphrag
- GitHub仓库: https://github.com/microsoft/graphrag
- 问题反馈: 通过GitHub Issues

## 📝 许可证

本项目基于Microsoft GraphRAG构建，遵循MIT许可证。

---

**注意**: 运行完整的GraphRAG索引构建需要有效的OpenAI API密钥。当前提供的是模拟查询功能，用于演示系统架构和接口。