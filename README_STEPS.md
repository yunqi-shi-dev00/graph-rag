# GraphRAG 分步执行指南

本项目提供了一系列 Python 脚本，让您能够通过运行文件的方式逐步了解和使用 GraphRAG 的每个功能。

## 📋 目录

- [概述](#概述)
- [环境准备](#环境准备)
- [分步执行脚本](#分步执行脚本)
- [脚本详细说明](#脚本详细说明)
- [常见问题](#常见问题)
- [高级用法](#高级用法)

## 概述

GraphRAG 是一个基于图的检索增强生成系统，能够从非结构化文本中提取结构化知识图谱，并提供强大的查询能力。

本项目将 GraphRAG 的使用流程分解为 8 个独立的步骤，每个步骤都有对应的 Python 脚本，您可以按顺序执行来学习整个系统。

## 环境准备

### 1. 安装 GraphRAG

```bash
# 使用 pip 安装
pip install graphrag

# 或使用 uv (更快)
uv pip install graphrag
```

### 2. 安装额外依赖

```bash
pip install python-dotenv
```

### 3. 准备 API 密钥

GraphRAG 需要 LLM API 来处理文本。支持：
- OpenAI API
- Azure OpenAI
- 其他兼容的 API

## 分步执行脚本

### 快速开始

按照以下顺序执行脚本：

```bash
# 步骤 1: 初始化项目
python step1_initialize.py

# 步骤 2: 配置参数
python step2_configure.py

# 步骤 3: 构建索引（需要配置 API 密钥）
python step3_index.py

# 步骤 4: 本地搜索查询
python step4_query_local.py

# 步骤 5: 全局搜索查询
python step5_query_global.py

# 步骤 6: 更新索引
python step6_update_index.py

# 步骤 7: 高级功能
python step7_advanced_query.py

# 步骤 8: 完整工作流程（一键演示所有功能）
python step8_complete_workflow.py
```

## 脚本详细说明

### 📁 step1_initialize.py - 项目初始化
**功能：**
- 创建项目目录结构
- 初始化 GraphRAG 配置
- 创建示例输入数据
- 生成基础配置文件

**输出：**
```
my_graphrag_project/
├── input/           # 输入数据目录
│   └── sample_data.txt
├── settings.yaml    # 配置文件
└── prompts/        # 提示词目录
```

**使用场景：** 开始新项目时的第一步

---

### ⚙️ step2_configure.py - 配置管理
**功能：**
- 配置 LLM 参数（模型、温度、令牌限制等）
- 设置嵌入模型
- 调整文本分块参数
- 配置缓存和存储选项
- 创建 .env 文件模板

**重要配置项：**
- `llm.model`: 使用的语言模型
- `chunks.size`: 文本分块大小
- `embeddings.model`: 嵌入模型
- `community_reports.max_length`: 社区报告长度

**使用场景：** 根据需求调整系统参数

---

### 🔨 step3_index.py - 构建知识图谱
**功能：**
- 读取输入文本数据
- 提取实体和关系
- 构建知识图谱
- 生成社区报告
- 创建向量嵌入

**执行时间：** 取决于数据量，通常需要几分钟

**输出文件：**
- `create_final_entities.parquet` - 实体数据
- `create_final_relationships.parquet` - 关系数据
- `create_final_communities.parquet` - 社区数据
- `create_final_community_reports.parquet` - 社区报告

**使用场景：** 处理新数据集时

---

### 🔍 step4_query_local.py - 本地搜索
**功能：**
- 基于实体和关系的精确搜索
- 适合具体、详细的问题
- 返回相关实体的上下文信息

**示例查询：**
- "什么是机器学习？"
- "深度学习的具体应用"
- "自然语言处理包含哪些技术"

**使用场景：** 需要详细信息时

---

### 🌍 step5_query_global.py - 全局搜索
**功能：**
- 基于社区摘要的宏观搜索
- 适合综合性、概括性问题
- 提供高层次的见解

**示例查询：**
- "总结所有主要技术"
- "各技术之间的关系"
- "整体趋势分析"

**使用场景：** 需要全局视角时

---

### 🔄 step6_update_index.py - 增量更新
**功能：**
- 添加新数据到现有索引
- 保留原有知识图谱
- 增量处理新内容

**流程：**
1. 添加新文件到 input/ 目录
2. 运行更新脚本
3. 验证新数据已被索引

**使用场景：** 持续更新知识库

---

### 🚀 step7_advanced_query.py - 高级功能
**功能：**
- **基础搜索：** 简单文本匹配
- **漂移搜索：** 跟踪主题演变
- **社区级别调整：** 控制查询粒度
- **流式输出：** 实时显示响应
- **自定义格式：** 指定输出格式
- **性能优化：** 提供优化建议

**高级选项：**
```python
# 动态社区选择
--dynamic-community-selection

# 自定义响应格式
--response-type "List of 5 points"

# 流式输出
--streaming
```

**使用场景：** 需要特定功能或优化性能时

---

### 🎯 step8_complete_workflow.py - 完整演示
**功能：**
- 一键运行完整流程
- 交互式配置向导
- 自动化所有步骤
- 提供详细说明

**包含步骤：**
1. 项目初始化
2. 数据准备
3. 系统配置
4. 索引构建
5. 查询演示
6. 数据更新
7. 高级功能展示
8. 总结报告

**使用场景：** 快速了解完整系统或演示给他人

## 常见问题

### Q1: 如何配置 API 密钥？

编辑 `my_graphrag_project/.env` 文件：

```bash
# OpenAI
GRAPHRAG_API_KEY=sk-your-api-key

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment
```

### Q2: 索引构建失败怎么办？

1. 检查 API 密钥是否正确
2. 确认网络连接正常
3. 查看错误日志
4. 尝试减小批处理大小
5. 使用 `--dry-run` 测试配置

### Q3: 如何优化性能？

```yaml
# settings.yaml 优化配置

# 增加并发
llm:
  concurrent_requests: 50

# 优化分块
chunks:
  size: 1200
  overlap: 100

# 启用缓存
cache:
  type: file

# 批处理嵌入
embeddings:
  batch_size: 32
```

### Q4: 本地搜索 vs 全局搜索？

- **本地搜索：** 详细、具体、基于实体
- **全局搜索：** 概括、宏观、基于社区

### Q5: 如何处理大量数据？

1. 分批处理输入文件
2. 使用更便宜的模型（如 gpt-3.5-turbo）
3. 调整 `tokens_per_minute` 限制
4. 启用缓存避免重复调用

## 高级用法

### 自定义提示词

```bash
# 运行提示词调优
python -m graphrag prompt-tune \
    --root ./my_graphrag_project \
    --domain "您的领域" \
    --language "Chinese"
```

### 编程集成

```python
import subprocess
import json

def query_graphrag(query, method="local"):
    """编程方式调用 GraphRAG"""
    result = subprocess.run(
        ["python", "-m", "graphrag", "query",
         "--method", method,
         "--query", query,
         "--root", "./my_graphrag_project"],
        capture_output=True,
        text=True
    )
    return result.stdout

# 使用示例
response = query_graphrag("什么是深度学习？")
print(response)
```

### 批量查询

```python
def batch_query(queries, method="local"):
    """批量执行查询"""
    results = {}
    for query in queries:
        results[query] = query_graphrag(query, method)
    return results

# 使用示例
questions = [
    "AI的定义",
    "机器学习的类型",
    "深度学习的应用"
]
answers = batch_query(questions)
```

### 监控和日志

```python
import logging
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='graphrag.log'
)

def monitored_index():
    """带监控的索引构建"""
    start_time = time.time()
    logging.info("开始索引构建")
    
    # 执行索引
    # ...
    
    elapsed = time.time() - start_time
    logging.info(f"索引完成，耗时: {elapsed:.2f}秒")
```

## 项目结构

```
workspace/
├── step1_initialize.py      # 初始化脚本
├── step2_configure.py        # 配置脚本
├── step3_index.py           # 索引构建
├── step4_query_local.py     # 本地搜索
├── step5_query_global.py    # 全局搜索
├── step6_update_index.py    # 更新索引
├── step7_advanced_query.py  # 高级功能
├── step8_complete_workflow.py # 完整流程
├── README_STEPS.md          # 本文档
└── my_graphrag_project/     # 生成的项目目录
    ├── input/               # 输入数据
    ├── output/              # 索引输出
    ├── cache/               # 缓存文件
    ├── settings.yaml        # 配置文件
    └── .env                # 环境变量
```

## 下一步

1. **深入学习：** 阅读[官方文档](https://microsoft.github.io/graphrag)
2. **实际应用：** 使用自己的数据集
3. **性能优化：** 调整参数以适应具体需求
4. **系统集成：** 将 GraphRAG 集成到应用中
5. **社区交流：** 参与 [GitHub Discussions](https://github.com/microsoft/graphrag/discussions)

## 许可证

本示例代码遵循 MIT 许可证。GraphRAG 本身的许可证请参考其官方仓库。

---

**提示：** 如有问题，请先查看脚本中的详细注释和错误提示，它们包含了丰富的调试信息。