# GraphRAG 使用指南

## 目录
- [项目简介](#项目简介)
- [环境要求](#环境要求)
- [安装步骤](#安装步骤)
- [快速开始](#快速开始)
- [核心功能](#核心功能)
- [详细流程](#详细流程)
- [配置说明](#配置说明)
- [常见问题](#常见问题)

## 项目简介

GraphRAG 是微软开发的基于图的检索增强生成（Graph-based Retrieval-Augmented Generation）系统。它通过构建知识图谱的方式，从非结构化文本中提取实体、关系和社区结构，实现更准确和全面的信息检索与问答。

### 主要特点
- 🔍 **多层次搜索**：支持全局搜索和局部搜索
- 📊 **知识图谱构建**：自动提取实体和关系
- 🎯 **社区检测**：识别文档中的主题社区
- 💡 **智能索引**：基于LLM的智能文本处理

## 环境要求

- **Python**: 3.10 - 3.12
- **操作系统**: Windows, macOS, Linux
- **内存**: 建议 8GB 以上
- **API密钥**: OpenAI API 或 Azure OpenAI API

## 安装步骤

### 1. 基础安装

#### 方法一：使用 pip 安装（推荐）
```bash
# 创建虚拟环境
python -m venv graphrag_env
source graphrag_env/bin/activate  # Linux/Mac
# 或
graphrag_env\Scripts\activate  # Windows

# 安装 GraphRAG
pip install graphrag
```

#### 方法二：从源码安装
```bash
# 克隆仓库
git clone https://github.com/microsoft/graphrag.git
cd graphrag

# 使用 uv 安装（推荐）
pip install uv
uv venv --python 3.11
source .venv/bin/activate  # Linux/Mac
uv pip install -e .

# 或使用 pip 安装
pip install -e .
```

### 2. 依赖包说明

核心依赖：
```bash
# LLM相关
pip install openai>=1.68.0
pip install tiktoken>=0.9.0

# 数据处理
pip install pandas>=2.2.3
pip install numpy>=1.25.2
pip install networkx>=3.4.2

# 向量存储
pip install lancedb>=0.17.0
pip install azure-search-documents>=11.5.2

# NLP工具
pip install nltk==3.9.1
pip install spacy>=3.8.4
pip install textblob>=0.18.0.post0

# 配置管理
pip install pyyaml>=6.0.2
pip install python-dotenv>=1.0.1
pip install pydantic>=2.10.3
```

### 3. 额外工具安装（可选）

如需处理PPT/图片等格式：
```bash
# PPT处理
pip install python-pptx

# PDF处理
pip install pypdf2 pdfplumber

# OCR功能
pip install pytesseract pillow
# 需要安装 Tesseract: https://github.com/tesseract-ocr/tesseract

# 或使用 EasyOCR
pip install easyocr
```

## 快速开始

### 1. 初始化项目
```bash
# 创建项目目录
mkdir my_graphrag_project
cd my_graphrag_project

# 初始化配置
graphrag init --root .
```

这将创建两个文件：
- `.env` - 环境变量配置（API密钥等）
- `settings.yaml` - 项目配置文件

### 2. 配置API密钥

编辑 `.env` 文件：

#### OpenAI配置
```bash
GRAPHRAG_API_KEY=your_openai_api_key_here
```

#### Azure OpenAI配置
```bash
GRAPHRAG_API_KEY=your_azure_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
```

### 3. 准备输入数据
```bash
# 创建输入目录
mkdir input

# 添加文本文件
echo "Your text content here" > input/document.txt

# 或下载示例数据
curl https://www.gutenberg.org/cache/epub/24022/pg24022.txt -o input/book.txt
```

### 4. 运行索引
```bash
# 基础索引命令
graphrag index --root .

# 带详细日志
graphrag index --root . --verbose
```

## 核心功能

### 一、索引构建 (Index)

#### 基础索引
```bash
# 标准索引
graphrag index --root /path/to/project

# 指定配置文件
graphrag index --root /path/to/project --config custom_settings.yaml

# 详细日志模式
graphrag index --root /path/to/project --verbose

# 内存分析模式
graphrag index --root /path/to/project --memprofile

# 干运行（验证配置）
graphrag index --root /path/to/project --dry-run

# 禁用缓存
graphrag index --root /path/to/project --no-cache

# 指定输出目录
graphrag index --root /path/to/project --output /path/to/output
```

#### 增量更新
```bash
# 更新已有索引
graphrag update --root /path/to/project

# 带配置文件的更新
graphrag update --root /path/to/project --config settings.yaml
```

### 二、提示词调优 (Prompt Tuning)

```bash
# 基础调优
graphrag prompt-tune --root /path/to/project

# 指定配置
graphrag prompt-tune --root /path/to/project --config settings.yaml

# 设置调优参数
graphrag prompt-tune --root /path/to/project \
    --limit 10 \
    --chunk-size 1000 \
    --min-examples-per-persona 3 \
    --max-examples-per-persona 5

# 指定选择策略
graphrag prompt-tune --root /path/to/project \
    --selection-method random  # 或 top, auto

# 禁用语言检测
graphrag prompt-tune --root /path/to/project --no-language-detection

# 输出到指定目录
graphrag prompt-tune --root /path/to/project --output /path/to/prompts
```

### 三、查询搜索 (Query)

#### 全局搜索 (Global Search)
```bash
# 基础全局搜索
graphrag query --root /path/to/project \
    --method global \
    --query "What are the main themes?"

# 带社区级别的全局搜索
graphrag query --root /path/to/project \
    --method global \
    --community-level 2 \
    --query "Summarize the key findings"
```

#### 局部搜索 (Local Search)
```bash
# 基础局部搜索
graphrag query --root /path/to/project \
    --method local \
    --query "Tell me about specific entity"

# 带社区级别的局部搜索
graphrag query --root /path/to/project \
    --method local \
    --community-level 1 \
    --query "What happened to character X?"
```

#### 漂移搜索 (Drift Search)
```bash
# 漂移搜索（跟踪主题演变）
graphrag query --root /path/to/project \
    --method drift \
    --query "How has the topic evolved?"

# 带跟踪参数的漂移搜索
graphrag query --root /path/to/project \
    --method drift \
    --community-level 2 \
    --query "Track changes in sentiment"
```

#### 高级查询选项
```bash
# 指定数据路径
graphrag query --root /path/to/project \
    --data /path/to/indexed/data \
    --method global \
    --query "Your question"

# 使用自定义配置
graphrag query --root /path/to/project \
    --config custom_settings.yaml \
    --method local \
    --query "Your question"

# 流式输出
graphrag query --root /path/to/project \
    --method global \
    --streaming \
    --query "Your question"

# 指定响应类型
graphrag query --root /path/to/project \
    --method local \
    --response-type "multiple-paragraphs" \
    --query "Your question"
```

## 详细流程

### 完整工作流程示例

```bash
# 1. 创建新项目
mkdir news_analysis
cd news_analysis

# 2. 初始化
graphrag init --root .

# 3. 配置API（编辑.env文件）
echo "GRAPHRAG_API_KEY=sk-..." > .env

# 4. 准备数据
mkdir input
cp /path/to/your/texts/*.txt input/

# 5. （可选）调优提示词
graphrag prompt-tune --root . --limit 10

# 6. 构建索引
graphrag index --root . --verbose

# 7. 执行查询
# 全局查询 - 适合总结性问题
graphrag query --root . \
    --method global \
    --query "What are the main topics discussed?"

# 局部查询 - 适合具体问题
graphrag query --root . \
    --method local \
    --query "What did person X say about topic Y?"

# 8. （可选）更新索引
# 添加新文件到input目录后
graphrag update --root .
```

## 配置说明

### settings.yaml 主要配置项

```yaml
# LLM配置
models:
  chat:
    model: gpt-4-turbo-preview
    temperature: 0.0
    max_tokens: 4000
  
  embeddings:
    model: text-embedding-3-small
    
# 输入配置
input:
  file_type: text  # 可选: text, csv, json
  file_pattern: ".*\\.txt$"
  encoding: utf-8
  
# 分块配置
chunks:
  size: 1200
  overlap: 100
  strategy: sentence  # 可选: sentence, tokens
  
# 输出配置
output:
  base_dir: output
  
# 缓存配置
cache:
  type: file  # 可选: file, memory, none
  
# 存储配置
storage:
  type: file  # 可选: file, blob, cosmosdb
  
# 社区检测配置
community:
  max_level: 2
  
# 嵌入配置
embed_graph:
  enabled: true
  
umap:
  enabled: true
```

### 输入格式配置

#### 文本文件输入
```yaml
input:
  file_type: text
  file_pattern: ".*\\.txt$"
  encoding: utf-8
```

#### CSV文件输入
```yaml
input:
  file_type: csv
  file_pattern: ".*\\.csv$"
  text_column: content  # 文本列名
  title_column: title   # 标题列名
  metadata:             # 元数据列
    - author
    - date
```

#### JSON文件输入
```yaml
input:
  file_type: json
  file_pattern: ".*\\.json$"
  text_column: text
  title_column: title
```

## 常见问题

### Q1: 如何处理大文件？
```bash
# 调整分块大小
# 编辑 settings.yaml
chunks:
  size: 800  # 减小分块大小
  overlap: 50
```

### Q2: 如何降低API调用成本？
```bash
# 1. 使用更便宜的模型
models:
  chat:
    model: gpt-3.5-turbo
    
# 2. 启用缓存
graphrag index --root . --cache

# 3. 先用小数据集测试
graphrag index --root . --dry-run
```

### Q3: 索引失败如何排查？
```bash
# 1. 启用详细日志
graphrag index --root . --verbose

# 2. 检查日志文件
cat output/logs.txt

# 3. 验证配置
graphrag index --root . --dry-run
```

### Q4: 如何处理非英文文本？
```yaml
# 在 settings.yaml 中配置
encoding: utf-8
language: chinese  # 或其他语言
```

### Q5: 如何使用本地模型？
```yaml
# 配置本地 Ollama 或其他兼容接口
models:
  chat:
    api_base: http://localhost:11434/v1
    model: llama2
```

## 性能优化建议

1. **批处理**：将多个小文件合并为几个大文件
2. **并行处理**：调整并发数设置
3. **增量更新**：使用 `graphrag update` 而非重建索引
4. **缓存利用**：始终启用缓存以避免重复API调用
5. **分块优化**：根据文档特点调整分块策略

## 故障排除

### 常见错误及解决方案

1. **API密钥错误**
```bash
# 检查环境变量
echo $GRAPHRAG_API_KEY

# 重新设置
export GRAPHRAG_API_KEY="your-key"
```

2. **内存不足**
```bash
# 减小批处理大小
# 在 settings.yaml 中
parallelization:
  num_threads: 2  # 减少并发
```

3. **编码错误**
```bash
# 指定正确的编码
input:
  encoding: utf-8  # 或 gbk, latin-1 等
```

## 进阶使用

### 自定义工作流
```python
import asyncio
from graphrag import api

async def custom_index():
    config = api.load_config("settings.yaml")
    results = await api.build_index(
        config=config,
        method="standard",
        memory_profile=False
    )
    return results

# 运行自定义索引
asyncio.run(custom_index())
```

### 编程方式查询
```python
import asyncio
from graphrag import api

async def search():
    result = await api.local_search(
        config_path="settings.yaml",
        data_path="output",
        query="Your question here",
        community_level=2
    )
    print(result.response)

asyncio.run(search())
```

## 更多资源

- 📚 [官方文档](https://microsoft.github.io/graphrag)
- 💻 [GitHub仓库](https://github.com/microsoft/graphrag)
- 📝 [研究论文](https://arxiv.org/pdf/2404.16130)
- 🎯 [示例项目](examples_notebooks/)
- 💬 [社区讨论](https://github.com/microsoft/graphrag/discussions)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件