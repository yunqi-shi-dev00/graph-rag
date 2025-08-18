# GraphRAG - 基于图的检索增强生成系统

<div align="center">
  
[![PyPI - Version](https://img.shields.io/pypi/v/graphrag)](https://pypi.org/project/graphrag/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/graphrag)](https://pypi.org/project/graphrag/)
[![GitHub Issues](https://img.shields.io/github/issues/microsoft/graphrag)](https://github.com/microsoft/graphrag/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/microsoft/graphrag)](https://github.com/microsoft/graphrag/discussions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 📚 项目简介

GraphRAG 是由微软研究院开发的一个创新性的数据处理和转换套件，旨在利用大型语言模型（LLM）的强大能力，从非结构化文本中提取有意义的结构化数据。与传统的基于语义搜索的 RAG（检索增强生成）方法不同，GraphRAG 采用了基于知识图谱的结构化、层次化方法。

### 🌟 核心特性

- **知识图谱构建**：自动从文本数据中提取实体、关系和关键声明，构建知识图谱
- **层次化社区检测**：使用 Leiden 算法对图进行层次聚类，生成社区结构
- **智能摘要生成**：自底向上生成每个社区及其组成部分的摘要
- **多模式查询**：支持全局搜索、本地搜索和 DRIFT 搜索三种查询模式
- **提示词调优**：提供强大的提示词微调功能，优化特定领域的性能

### 🎯 GraphRAG vs 传统 RAG

**传统 RAG 的局限性：**
- 难以连接分散的信息点
- 在理解大规模数据集的整体语义概念时表现不佳
- 无法有效处理需要跨文档推理的复杂查询

**GraphRAG 的优势：**
- 通过知识图谱结构更好地理解实体间的关系
- 社区摘要提供了数据的整体视角
- 在回答复杂问题时表现出显著的性能提升
- 特别适合处理私有数据集和企业文档

## 🚀 快速开始

### 系统要求

- Python 3.10 - 3.12
- 8GB+ RAM（建议16GB以上）
- OpenAI API 密钥或 Azure OpenAI 服务

### 安装

```bash
# 使用 pip 安装
pip install graphrag

# 或从源码安装（开发模式）
git clone https://github.com/microsoft/graphrag.git
cd graphrag
pip install -e .
```

### 基础使用示例

#### 1. 初始化项目

```bash
# 创建项目目录
mkdir my_graphrag_project
cd my_graphrag_project

# 初始化 GraphRAG 配置
graphrag init --root .
```

这将创建两个重要文件：
- `.env`：包含 API 密钥等环境变量
- `settings.yaml`：包含所有配置选项

#### 2. 准备数据

```bash
# 创建输入目录
mkdir input

# 将文本文件放入 input 目录
# 支持 .txt, .json, .csv 等格式
cp /path/to/your/documents/*.txt ./input/
```

#### 3. 配置 API

编辑 `.env` 文件：

```bash
# OpenAI 配置
GRAPHRAG_API_KEY=your_openai_api_key_here

# 或 Azure OpenAI 配置
GRAPHRAG_API_KEY=your_azure_api_key_here
```

对于 Azure OpenAI，还需要在 `settings.yaml` 中配置：

```yaml
models:
  chat:
    type: azure_openai_chat
    api_base: https://your-instance.openai.azure.com
    api_version: 2024-02-15-preview
    deployment_name: your-deployment-name

  embeddings:
    type: azure_openai_embedding
    api_base: https://your-instance.openai.azure.com
    api_version: 2024-02-15-preview
    deployment_name: your-embedding-deployment
```

#### 4. 运行索引构建

```bash
graphrag index --root .
```

索引过程包括：
- 文本分块和预处理
- 实体和关系提取
- 知识图谱构建
- 社区检测和层次聚类
- 摘要生成

#### 5. 查询数据

```bash
# 全局搜索 - 适合宏观问题
graphrag query \
  --root . \
  --method global \
  --query "这个数据集的主要主题是什么？"

# 本地搜索 - 适合具体问题
graphrag query \
  --root . \
  --method local \
  --query "张三的主要职责是什么？"

# DRIFT 搜索 - 结合本地和全局上下文
graphrag query \
  --root . \
  --method drift \
  --query "项目中的技术架构是如何演进的？"
```

## 📖 详细功能说明

### 索引构建流程

1. **文本单元化（Text Units）**
   - 将输入文档分割成可分析的文本单元
   - 提供细粒度的引用和追踪

2. **实体和关系提取**
   - 使用 LLM 识别文本中的实体（人物、地点、组织等）
   - 提取实体间的关系和关键声明

3. **图构建和社区检测**
   - 构建知识图谱
   - 应用 Leiden 算法进行层次聚类
   - 识别紧密相关的实体社区

4. **摘要生成**
   - 为每个社区生成综合摘要
   - 自底向上构建层次化的理解

### 查询模式详解

#### 🌍 全局搜索（Global Search）
- **用途**：回答关于整个数据集的宏观问题
- **原理**：利用社区摘要进行推理
- **适用场景**：
  - "数据集的主要主题是什么？"
  - "文档中讨论的关键趋势有哪些？"
  - "整体叙事结构是怎样的？"

#### 📍 本地搜索（Local Search）
- **用途**：回答关于特定实体的详细问题
- **原理**：从特定实体扩展到其邻居和相关概念
- **适用场景**：
  - "张三的背景和经历是什么？"
  - "产品 X 的具体功能有哪些？"
  - "事件 Y 的详细过程是怎样的？"

#### 🔄 DRIFT 搜索（Dynamic Reasoning and Information Flow Tracking）
- **用途**：结合局部和全局信息进行复杂推理
- **原理**：动态追踪信息流，结合社区上下文
- **适用场景**：
  - "不同部门之间是如何协作的？"
  - "技术决策的演变过程是怎样的？"
  - "多个事件之间的因果关系是什么？"

### 提示词调优

GraphRAG 提供了强大的提示词调优功能，可以针对特定领域优化性能：

```bash
# 自动调优提示词
graphrag prompt-tune \
  --root . \
  --domain "医疗研究" \
  --method random \
  --limit 10
```

调优参数说明：
- `--domain`：指定领域（如"金融分析"、"法律文档"等）
- `--method`：选择方法（random、top、all）
- `--limit`：限制处理的文档数量
- `--language`：指定语言（支持中文）

## 🛠️ 高级配置

### settings.yaml 关键配置项

```yaml
# LLM 配置
models:
  chat:
    model: gpt-4-turbo
    temperature: 0.7
    max_tokens: 4000
    
  embeddings:
    model: text-embedding-3-small
    batch_size: 16

# 文本处理配置
chunks:
  size: 1200          # 文本块大小
  overlap: 100        # 重叠大小
  
# 实体提取配置
entity_extraction:
  prompt: "prompts/entity_extraction.txt"
  max_gleanings: 1   # 提取轮数
  
# 图嵌入配置
embed_graph:
  enabled: true       # 启用图嵌入
  
# UMAP 降维配置
umap:
  enabled: true       # 启用 UMAP
  
# 社区报告配置
community_reports:
  max_length: 2000
  max_input_length: 8000
```

### 成本优化建议

⚠️ **注意**：GraphRAG 索引构建可能产生较高的 API 调用成本

优化策略：
1. **从小数据集开始**：先用小样本测试配置
2. **调整块大小**：增大 chunk size 可减少 API 调用
3. **使用更便宜的模型**：在质量可接受的前提下使用 gpt-3.5-turbo
4. **限制提取轮数**：设置 `max_gleanings: 0` 减少重复提取
5. **使用本地缓存**：启用缓存避免重复处理

## 🎨 可视化和调试

### 知识图谱可视化

GraphRAG 生成的知识图谱可以通过多种工具可视化：

```python
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 加载图数据
nodes = pd.read_parquet("output/create_final_nodes.parquet")
edges = pd.read_parquet("output/create_final_edges.parquet")

# 创建 NetworkX 图
G = nx.Graph()
for _, node in nodes.iterrows():
    G.add_node(node['title'], **node.to_dict())
    
for _, edge in edges.iterrows():
    G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

# 可视化
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', 
        node_size=500, font_size=8)
plt.show()
```

### Unified Search 应用

项目包含了一个交互式的 Streamlit 应用，用于比较不同搜索模式：

```bash
# 进入应用目录
cd unified-search-app

# 安装依赖
uv sync --extra dev

# 运行应用
uv run poe start
```

功能特性：
- 多数据集支持
- 搜索结果对比
- 知识图谱探索
- 社区报告查看
- 问题建议生成

## 📊 API 使用

### Python API 示例

```python
from graphrag import api
import asyncio

# 索引构建
async def build_index():
    await api.build_index(
        root="./my_project",
        verbose=True,
        resume=False,
        memprofile=False
    )

# 查询
async def query_data():
    result = await api.query(
        root="./my_project",
        method="local",
        query="你的查询问题",
        community_level=2,
        response_type="Multiple Paragraphs"
    )
    print(result.response)
    
# 运行
asyncio.run(build_index())
asyncio.run(query_data())
```

### 提示词调优 API

```python
from graphrag import api

# 运行提示词调优
api.prompt_tune(
    root="./my_project",
    domain="技术文档",
    method="random",
    limit=10,
    language="Chinese",
    max_tokens=2000,
    chunk_size=1200
)
```

## 🧪 测试

项目包含完整的测试套件：

```bash
# 运行所有测试
pytest tests/

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行特定测试
pytest tests/unit/test_entity_extraction.py -v

# 测试覆盖率
coverage run -m pytest tests/
coverage report --show-missing
```

## 🤝 贡献指南

我们欢迎社区贡献！请查看以下资源：

- [贡献指南](CONTRIBUTING.md) - 了解如何贡献代码
- [开发指南](DEVELOPING.md) - 设置开发环境
- [行为准则](CODE_OF_CONDUCT.md) - 社区行为规范
- [GitHub Discussions](https://github.com/microsoft/graphrag/discussions) - 参与讨论

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/microsoft/graphrag.git
cd graphrag

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev]"

# 运行代码检查
poe check

# 格式化代码
poe format
```

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🔗 相关资源

- 📝 [官方文档](https://microsoft.github.io/graphrag)
- 📊 [研究论文](https://arxiv.org/pdf/2404.16130)
- 📖 [微软研究院博客](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
- 💬 [GitHub Discussions](https://github.com/microsoft/graphrag/discussions)
- 🐛 [问题追踪](https://github.com/microsoft/graphrag/issues)

## ⚠️ 重要说明

1. **成本警告**：GraphRAG 索引构建可能产生大量 API 调用，请仔细阅读文档了解成本影响
2. **版本兼容**：在次版本升级时运行 `graphrag init --force` 更新配置
3. **数据隐私**：处理敏感数据时请确保符合相关法规要求
4. **性能考虑**：大型数据集可能需要较长处理时间和大量计算资源

## 🙏 致谢

GraphRAG 是微软研究院的研究成果，感谢所有贡献者的努力。特别感谢：
- 微软研究院团队
- 开源社区贡献者
- 所有提供反馈和建议的用户

---

<div align="center">
  
**[⬆ 返回顶部](#graphrag---基于图的检索增强生成系统)**

Made with ❤️ by Microsoft Research

</div>