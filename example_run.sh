#!/bin/bash

# GraphRAG 完整运行示例脚本
# 作者：GraphRAG 示例
# 描述：演示如何从零开始设置和运行 GraphRAG

echo "==================================="
echo "GraphRAG 完整运行示例"
echo "==================================="

# 1. 设置项目目录
PROJECT_DIR="graphrag_example"
echo "步骤 1: 创建项目目录 $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# 2. 初始化项目
echo "步骤 2: 初始化 GraphRAG 项目"
graphrag init --root .

# 3. 配置 API 密钥
echo "步骤 3: 配置 API 密钥"
cat > .env << EOF
# OpenAI API 配置
GRAPHRAG_API_KEY=your-openai-api-key-here

# 或者使用 Azure OpenAI
# AZURE_OPENAI_API_KEY=your-azure-key
# AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
# AZURE_OPENAI_API_VERSION=2024-02-15-preview
EOF

echo "请编辑 .env 文件，添加您的 API 密钥"

# 4. 创建示例输入数据
echo "步骤 4: 创建示例输入数据"
mkdir -p input
cat > input/sample_document.txt << 'EOF'
人工智能的发展历程

人工智能（AI）的概念最早可以追溯到1950年代，当时艾伦·图灵提出了著名的"图灵测试"，
用于判断机器是否具有智能。1956年，在达特茅斯会议上，"人工智能"这个术语正式诞生。

早期发展（1950-1970年代）
这一时期的研究主要集中在符号推理和专家系统。研究人员如约翰·麦卡锡、马文·明斯基等
开创了AI研究的基础。然而，由于计算能力的限制和过高的期望，AI在1970年代末期进入了
第一个"寒冬"。

机器学习的兴起（1980-2000年代）
1980年代，专家系统的商业应用带来了AI的复兴。随后，机器学习方法，特别是神经网络的
研究开始受到重视。1997年，IBM的深蓝击败国际象棋世界冠军卡斯帕罗夫，标志着AI在
特定领域达到了人类水平。

深度学习革命（2010年代至今）
2012年，AlexNet在ImageNet竞赛中的胜利开启了深度学习时代。随后，谷歌的AlphaGo
在2016年击败围棋世界冠军李世石，展示了深度强化学习的威力。

大语言模型时代（2020年代）
OpenAI的GPT系列模型，特别是ChatGPT的发布，将AI带入了新的时代。这些模型展示了
前所未有的语言理解和生成能力，正在改变人们工作和生活的方式。

主要研究机构和公司
- OpenAI：开发了GPT系列和DALL-E
- Google DeepMind：开发了AlphaGo和Gemini
- Microsoft Research：在AI各个领域都有重要贡献
- Meta AI：开发了LLaMA等开源模型
- 百度研究院：在中文AI领域处于领先地位

未来展望
人工智能正朝着通用人工智能（AGI）的方向发展。研究重点包括：
1. 多模态理解和生成
2. 更强的推理能力
3. 更好的可解释性
4. 更低的计算成本
5. 更强的安全性和对齐性
EOF

# 5. 创建配置文件
echo "步骤 5: 创建优化的配置文件"
cat > settings.yaml << 'EOF'
# GraphRAG 配置文件

llm:
  api_key: ${GRAPHRAG_API_KEY}
  type: openai_chat
  model: gpt-3.5-turbo  # 使用更经济的模型
  max_tokens: 2000
  temperature: 0.0
  request_timeout: 180.0

embeddings:
  api_key: ${GRAPHRAG_API_KEY}
  type: openai_embedding
  model: text-embedding-3-small
  batch_size: 16
  batch_max_tokens: 8000

chunks:
  size: 1000
  overlap: 100
  group_by_columns: [id]

input:
  type: file
  file_type: text
  base_dir: "input"
  file_pattern: ".*\\.txt"
  encoding: utf-8

cache:
  type: file
  base_dir: "cache"

storage:
  type: file
  base_dir: "output"

reporting:
  type: console

entity_extraction:
  prompt: "prompts/entity_extraction.txt"
  max_gleanings: 1
  entity_types: ["person", "organization", "location", "event", "concept"]

summarize_descriptions:
  prompt: "prompts/summarize_descriptions.txt"

claim_extraction:
  enabled: false  # 可选：禁用声明提取以节省成本

community_reports:
  prompt: "prompts/community_report.txt"
  max_length: 2000
  max_input_length: 8000

cluster_graph:
  max_cluster_size: 10

embed_graph:
  enabled: true
  num_walks: 10
  walk_length: 10
  window_size: 2
  iterations: 3
  random_seed: 42

umap:
  enabled: true

snapshots:
  graphml: false
  raw_entities: false
  top_level_nodes: false

encoding_model: cl100k_base
skip_workflows: []
EOF

echo "==================================="
echo "设置完成！"
echo "==================================="
echo ""
echo "接下来的步骤："
echo "1. 编辑 .env 文件，添加您的 OpenAI API 密钥"
echo "2. 运行索引: graphrag index --root ."
echo "3. 运行查询:"
echo "   - 局部搜索: graphrag query --root . --method local \"图灵测试是什么？\""
echo "   - 全局搜索: graphrag query --root . --method global \"总结一下AI的发展历程\""
echo ""
echo "注意事项："
echo "- 首次运行索引可能需要几分钟时间"
echo "- 请确保有足够的 API 调用额度"
echo "- 建议先用小数据集测试"