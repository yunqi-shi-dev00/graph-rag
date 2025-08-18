# GraphRAG

<div align="center">

[![PyPI - Version](https://img.shields.io/pypi/v/graphrag)](https://pypi.org/project/graphrag/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/graphrag)](https://pypi.org/project/graphrag/)
[![GitHub Issues](https://img.shields.io/github/issues/microsoft/graphrag)](https://github.com/microsoft/graphrag/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/microsoft/graphrag)](https://github.com/microsoft/graphrag/discussions)

</div>

## 项目简介

GraphRAG 是一个基于图结构的检索增强生成（Retrieval-Augmented Generation, RAG）系统，由微软研究院开发。与传统的基于语义搜索的 RAG 方法不同，GraphRAG 采用结构化、分层的方法来处理和理解私有数据。

### 核心特性

- **知识图谱构建**: 从非结构化文本中提取有意义的结构化数据
- **社区层次结构**: 构建社区层次结构并生成摘要
- **增强推理能力**: 显著提升大语言模型对私有数据的推理能力
- **多种搜索模式**: 支持全局搜索和本地搜索
- **可视化界面**: 包含统一搜索应用，提供直观的数据探索体验

## 与传统 RAG 的对比

传统的 RAG 系统（基线 RAG）主要使用向量相似性作为搜索技术，在以下场景中表现不佳：

1. **连接分散信息**: 当回答问题需要通过共享属性遍历不同信息片段时
2. **整体理解**: 对大型数据集合或单个大型文档的语义概念进行整体理解时

GraphRAG 通过创建基于输入语料库的知识图谱，结合社区摘要和图机器学习输出来增强查询时的提示，在这两类问题上表现出显著改进。

## 快速开始

### 环境要求

- Python 3.10-3.12
- 支持的操作系统：Windows、macOS、Linux

### 安装

```bash
# 使用 pip 安装
pip install graphrag

# 或使用 uv 安装（推荐）
uv add graphrag
```

### 基本使用流程

1. **初始化项目**
   ```bash
   graphrag init --root ./my-project
   ```

2. **配置设置**
   编辑生成的 `settings.yaml` 文件，配置 LLM 提供商（如 OpenAI、Azure OpenAI）

3. **准备数据**
   将文本文件放入 `input` 目录

4. **建立索引**
   ```bash
   graphrag index --root ./my-project
   ```

5. **执行查询**
   ```bash
   # 全局搜索
   graphrag query --root ./my-project --method global "你的问题"
   
   # 本地搜索
   graphrag query --root ./my-project --method local "你的问题"
   ```

## 主要组件

### 1. 索引系统 (`graphrag.index`)
负责处理和索引原始文本数据，构建知识图谱：
- 实体提取和关系识别
- 社区检测和层次结构构建
- 嵌入生成和向量存储

### 2. 查询系统 (`graphrag.query`)
提供两种主要的查询模式：
- **全局搜索**: 适合需要整体理解数据集的问题
- **本地搜索**: 适合针对特定实体或概念的详细问题

### 3. 提示调优 (`graphrag.prompt_tune`)
帮助优化 LLM 提示以获得更好的结果：
```bash
graphrag prompt-tune --root ./my-project
```

### 4. 配置管理 (`graphrag.config`)
灵活的配置系统，支持：
- 多种 LLM 提供商
- 自定义嵌入模型
- 向量存储配置
- 缓存和存储选项

## 统一搜索应用

项目还包含一个基于 Streamlit 的可视化界面 `unified-search-app`，提供：

- 多数据集管理
- 交互式搜索比较
- 图谱可视化
- 社区报告浏览

### 运行统一搜索应用

```bash
cd unified-search-app
uv sync --extra dev
uv run poe start
```

## 高级配置

### 支持的 LLM 提供商
- OpenAI GPT 系列
- Azure OpenAI
- 其他兼容 OpenAI API 的模型

### 向量存储选项
- LanceDB（默认）
- Azure Search
- 其他向量数据库

### 存储后端
- 本地文件系统
- Azure Blob Storage
- Azure Cosmos DB

## 开发指南

### 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/microsoft/graphrag.git
cd graphrag

# 安装开发依赖
uv sync --extra dev

# 运行测试
uv run poe test

# 代码格式化
uv run poe format

# 类型检查
uv run poe check
```

### 项目结构

```
graphrag/
├── api/              # API 接口
├── cache/            # 缓存系统
├── cli/              # 命令行界面
├── config/           # 配置管理
├── data_model/       # 数据模型
├── index/            # 索引系统
├── language_model/   # 语言模型接口
├── query/            # 查询系统
├── prompt_tune/      # 提示调优
├── storage/          # 存储抽象
├── utils/            # 工具函数
└── vector_stores/    # 向量存储
```

## 重要提示

⚠️ **成本警告**: GraphRAG 索引可能是一个昂贵的操作，特别是在处理大型数据集时。请仔细阅读文档以了解相关成本，并从小规模数据开始测试。

⚠️ **提示调优**: 为了获得最佳结果，强烈建议根据[提示调优指南](https://microsoft.github.io/graphrag/prompt_tuning/overview/)对提示进行微调。

## 版本管理

请查看 [breaking-changes.md](./breaking-changes.md) 了解版本控制方法。

**重要**: 在次要版本升级之间始终运行 `graphrag init --root [path] --force` 以确保获得最新的配置格式。

## 相关资源

- 📖 [官方文档](https://microsoft.github.io/graphrag)
- 📝 [微软研究博客](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
- 📄 [GraphRAG 论文](https://arxiv.org/pdf/2404.16130)
- 💬 [GitHub 讨论区](https://github.com/microsoft/graphrag/discussions)
- 🐛 [问题反馈](https://github.com/microsoft/graphrag/issues)

## 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献指南。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](./LICENSE) 文件。

## 负责任的 AI

请参阅 [RAI_TRANSPARENCY.md](./RAI_TRANSPARENCY.md) 了解负责任 AI 的相关信息。

## 商标声明

本项目可能包含项目、产品或服务的商标或徽标。Microsoft 商标或徽标的授权使用须遵循 [Microsoft 商标和品牌指南](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general)。

## 隐私声明

[Microsoft 隐私声明](https://privacy.microsoft.com/en-us/privacystatement)