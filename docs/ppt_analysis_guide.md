# PPT解析数据与GraphRAG集成指南

## 概述

本指南详细说明如何将PPT解析生成的JSON数据集成到GraphRAG项目中，实现对PPT内容的知识图谱构建和智能问答。

## 数据兼容性分析

### ✅ 您的数据**可以**用于GraphRAG项目

您提供的PPT解析数据（TCL智能终端相对竞争力分析）非常适合GraphRAG处理，原因如下：

1. **结构化程度高**：包含清晰的表格数据、指标对比和趋势分析
2. **实体关系丰富**：包含公司（TCL、海信）、产品（空调、冰箱、洗衣机）、指标（营收、市占率）等多维度实体
3. **时序数据完整**：涵盖多个时间段的对比分析（2024Q1、2023年、2023Q1）
4. **知识密度大**：每页PPT都包含有价值的业务洞察和数据

## 快速开始

### 1. 环境准备

```bash
# 安装GraphRAG
pip install graphrag

# 安装数据处理依赖
pip install pandas
```

### 2. 数据转换

使用我们提供的转换脚本将PPT解析JSON转换为GraphRAG格式：

```bash
# 转换为JSON格式（推荐）
python scripts/ppt_to_graphrag.py your_ppt_data.json -o ./input/ppt_analysis.json

# 或转换为CSV格式
python scripts/ppt_to_graphrag.py your_ppt_data.json -f csv -o ./input/ppt_analysis.csv
```

### 3. 初始化GraphRAG项目

```bash
# 创建项目目录
mkdir ppt_analysis_project
cd ppt_analysis_project

# 初始化GraphRAG
graphrag init --root .

# 复制我们的中文优化配置
cp ../examples_notebooks/ppt_analysis_config.yaml ./settings.yaml
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
# OpenAI API配置
GRAPHRAG_API_KEY=your-api-key-here
GRAPHRAG_API_BASE=https://api.openai.com/v1  # 或您的API端点

# 或使用Azure OpenAI
# GRAPHRAG_API_KEY=your-azure-key
# GRAPHRAG_API_BASE=https://your-resource.openai.azure.com/
```

### 5. 运行索引构建

```bash
# 构建知识图谱索引
graphrag index --root .
```

### 6. 执行查询

```bash
# 全局查询（适合宏观问题）
graphrag query --root . --method global "TCL在2024年Q1的整体竞争力如何？"

# 局部查询（适合具体问题）
graphrag query --root . --method local "TCL的空调市场份额变化趋势是什么？"
```

## 数据格式说明

### 原始PPT解析JSON格式

```json
{
  "query": "请详细用中文讲解并提取图片中的内容...",
  "images": ["/path/to/image.png"],
  "directory_name": "TCL智能终端相对竞争力季度结果.pptx",
  "image_name": "第2页_1.png",
  "page_number": 2,
  "ref_orpo": "实际的内容解析结果...",
  "metadata": {...}
}
```

### 转换后的GraphRAG格式

```json
{
  "text": "【页面 2】\n【文档】TCL智能终端相对竞争力季度结果.pptx\n【内容解析】...",
  "title": "TCL智能终端相对竞争力季度结果.pptx - 第2页",
  "metadata": {
    "source_type": "ppt_analysis",
    "directory_name": "...",
    "page_number": 2,
    ...
  }
}
```

## 优化建议

### 1. 中文处理优化

- **使用GPT-4**：推荐使用GPT-4或GPT-4-turbo以获得更好的中文理解能力
- **调整分块大小**：中文文本信息密度大，建议将chunk_size设置为1200-1500
- **自定义提示词**：在配置文件中使用中文提示词，提高实体和关系提取的准确性

### 2. 成本控制

- **分批处理**：如果PPT页数较多，建议分批处理以控制API调用成本
- **使用缓存**：启用缓存功能避免重复处理
- **选择性处理**：可以先处理关键页面，评估效果后再处理全部内容

### 3. 查询优化

针对您的数据特点，建议的查询示例：

```python
# 竞争分析查询
"TCL相对于海信的主要优势和劣势是什么？"
"2024年Q1相比2023年，TCL的竞争力有哪些变化？"

# 产品线分析
"TCL在各个产品线（空调、冰箱、洗衣机）的市场表现如何？"
"哪个产品线是TCL的强项？"

# 财务指标分析
"TCL的营收和净利率表现如何？"
"运营效率方面，TCL与竞争对手相比处于什么水平？"

# 趋势分析
"TCL的市场份额变化趋势是什么？"
"哪些指标在改善，哪些在恶化？"
```

## 高级功能

### 1. 自定义实体类型

根据您的业务需求，可以在配置文件中定义特定的实体类型：

```yaml
entity_types:
  - 公司
  - 产品线
  - 财务指标
  - 市场指标
  - 时间周期
  - 竞争关系
```

### 2. 关系权重设置

可以为不同类型的关系设置权重，突出重要的业务关系：

```yaml
relationship_weights:
  竞争关系: 1.0
  产品归属: 0.8
  时间关联: 0.6
  指标对比: 0.9
```

### 3. 批量处理脚本

创建批量处理脚本 `batch_process.sh`：

```bash
#!/bin/bash

# 批量转换所有PPT解析文件
for file in ./raw_data/*.json; do
    python scripts/ppt_to_graphrag.py "$file" -o "./input/$(basename $file)"
done

# 构建索引
graphrag index --root .

# 生成分析报告
graphrag query --root . --method global "生成整体竞争力分析报告" > report.txt
```

## 常见问题

### Q1: 如何处理图片中的表格数据？

您的PPT解析已经将表格转换为文本，GraphRAG可以直接处理。如需更结构化的处理，可以在转换脚本中添加表格解析逻辑。

### Q2: 如何提高中文实体识别准确率？

1. 使用更强大的模型（如GPT-4）
2. 在提示词中提供领域特定的实体示例
3. 使用prompt tuning功能优化提示词

### Q3: 处理大量PPT时如何控制成本？

1. 使用分层采样：先处理关键页面
2. 启用缓存避免重复处理
3. 使用更经济的模型进行初步处理
4. 调整并行度和批处理大小

### Q4: 如何集成到现有系统？

GraphRAG提供API接口，可以：
1. 使用Python SDK进行编程集成
2. 通过REST API提供查询服务
3. 导出知识图谱数据到其他系统

## 进阶应用

### 1. 构建竞争情报系统

利用GraphRAG构建的知识图谱，可以：
- 自动生成竞争分析报告
- 追踪市场份额变化趋势
- 识别竞争优势和劣势
- 预测市场发展方向

### 2. 多文档关联分析

如果有多个季度的PPT：
1. 将所有PPT转换后放入同一项目
2. GraphRAG会自动关联不同时期的数据
3. 可以进行跨时期的趋势分析

### 3. 与其他数据源集成

可以将PPT数据与其他数据源结合：
- 财报数据
- 新闻资讯
- 行业报告
- 内部业务数据

## 技术支持

如遇到问题，可以：
1. 查看GraphRAG官方文档：https://microsoft.github.io/graphrag
2. 查看项目GitHub Issues
3. 参考我们提供的示例配置和脚本

## 总结

您的PPT解析数据完全可以用于GraphRAG项目。通过适当的数据转换和配置优化，可以构建一个强大的知识图谱系统，实现：

- ✅ 智能问答
- ✅ 竞争分析
- ✅ 趋势洞察
- ✅ 自动报告生成
- ✅ 多维度数据关联

祝您使用愉快！