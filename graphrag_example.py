#!/usr/bin/env python3
"""
GraphRAG Python API 使用示例
这个脚本演示如何通过 Python 代码使用 GraphRAG
"""

import asyncio
import os
from pathlib import Path
import pandas as pd

# 设置环境变量
os.environ["GRAPHRAG_API_KEY"] = "your-openai-api-key-here"

def setup_project():
    """设置项目目录和配置"""
    project_dir = Path("graphrag_python_example")
    project_dir.mkdir(exist_ok=True)
    
    # 创建输入目录
    input_dir = project_dir / "input"
    input_dir.mkdir(exist_ok=True)
    
    # 创建示例文档
    sample_text = """
    GraphRAG 技术介绍
    
    GraphRAG 是微软研究院开发的一种新型检索增强生成技术。与传统的 RAG 系统不同，
    GraphRAG 通过构建知识图谱来组织和理解文档内容。
    
    核心组件：
    1. 实体提取器：识别文档中的重要实体（人物、组织、概念等）
    2. 关系提取器：发现实体之间的关系
    3. 社区检测：使用图算法识别相关实体群组
    4. 摘要生成器：为每个社区生成综合摘要
    
    主要优势：
    - 更好的全局理解：通过图结构捕获文档的整体语义
    - 多尺度检索：支持从细节到全局的不同粒度查询
    - 可解释性：图结构提供了清晰的推理路径
    
    应用场景：
    GraphRAG 特别适合处理长文档、多文档总结、复杂问答等任务。
    在金融分析、法律文档理解、科研文献综述等领域有广泛应用。
    """
    
    (input_dir / "sample.txt").write_text(sample_text, encoding="utf-8")
    
    # 创建配置文件
    config = """
llm:
  api_key: ${GRAPHRAG_API_KEY}
  type: openai_chat
  model: gpt-3.5-turbo
  max_tokens: 2000
  temperature: 0.0

embeddings:
  api_key: ${GRAPHRAG_API_KEY}
  type: openai_embedding
  model: text-embedding-3-small

chunks:
  size: 500
  overlap: 50

input:
  type: file
  file_type: text
  base_dir: "input"

storage:
  type: file
  base_dir: "output"

cache:
  type: file
  base_dir: "cache"

reporting:
  type: console
"""
    
    (project_dir / "settings.yaml").write_text(config)
    (project_dir / ".env").write_text("GRAPHRAG_API_KEY=your-key-here\n")
    
    return project_dir


async def run_indexing_example():
    """运行索引示例"""
    from graphrag.index import run_pipeline_with_config
    from graphrag.config import create_graphrag_config
    
    print("开始构建索引...")
    
    # 加载配置
    config = create_graphrag_config(root_dir="graphrag_python_example")
    
    # 运行索引管道
    # 注意：实际使用时需要正确的 API 密钥
    # await run_pipeline_with_config(config)
    
    print("索引构建完成！")


def query_example():
    """查询示例"""
    print("\n查询示例：")
    print("-" * 50)
    
    # 局部搜索示例
    local_query = """
    from graphrag.query.structured_search.local_search.search import LocalSearch
    from graphrag.query.indexer_adapters import read_indexer_entities, read_indexer_relationships
    
    # 加载索引数据
    entity_df = pd.read_parquet("output/entities.parquet")
    relationship_df = pd.read_parquet("output/relationships.parquet")
    
    # 创建搜索实例
    search = LocalSearch(
        entities=entities,
        relationships=relationships,
        # ... 其他参数
    )
    
    # 执行查询
    result = await search.asearch("GraphRAG 的核心组件有哪些？")
    print(result.response)
    """
    
    print("局部搜索代码示例：")
    print(local_query)
    
    # 全局搜索示例
    global_query = """
    from graphrag.query.structured_search.global_search.search import GlobalSearch
    from graphrag.query.indexer_adapters import read_indexer_reports
    
    # 加载社区报告
    reports_df = pd.read_parquet("output/community_reports.parquet")
    reports = read_indexer_reports(reports_df)
    
    # 创建全局搜索实例
    search = GlobalSearch(
        community_reports=reports,
        # ... 其他参数
    )
    
    # 执行查询
    result = await search.asearch("总结文档的主要内容")
    print(result.response)
    """
    
    print("\n全局搜索代码示例：")
    print(global_query)


def advanced_usage():
    """高级用法示例"""
    print("\n高级用法：")
    print("-" * 50)
    
    # 自定义实体提取
    custom_entity = """
    # 自定义实体类型
    entity_types = ["技术", "公司", "产品", "人物", "概念"]
    
    # 自定义提示词
    custom_prompt = '''
    请从以下文本中提取 {entity_types} 类型的实体。
    对每个实体，提供：
    1. 名称
    2. 类型
    3. 描述
    4. 重要性评分（1-10）
    
    文本：{text}
    '''
    """
    
    print("自定义实体提取：")
    print(custom_entity)
    
    # 自定义向量存储
    vector_store = """
    # 使用 LanceDB 作为向量存储
    from graphrag.vector_stores.lancedb import LanceDBVectorStore
    
    vector_store = LanceDBVectorStore(
        collection_name="graphrag_embeddings",
        uri="./lancedb"
    )
    
    # 或使用 Azure Cognitive Search
    from graphrag.vector_stores.azure_ai_search import AzureAISearchVectorStore
    
    vector_store = AzureAISearchVectorStore(
        endpoint="https://your-search-service.search.windows.net",
        api_key="your-api-key",
        index_name="graphrag-index"
    )
    """
    
    print("\n自定义向量存储：")
    print(vector_store)


def performance_tips():
    """性能优化建议"""
    print("\n性能优化建议：")
    print("-" * 50)
    
    tips = """
    1. 批处理优化：
       - 增加 batch_size 以提高吞吐量
       - 调整 batch_max_tokens 避免超过限制
    
    2. 并发控制：
       - 设置 GRAPHRAG_LLM_THREAD_COUNT 控制并发请求
       - 设置 GRAPHRAG_EMBEDDING_THREAD_COUNT 控制嵌入并发
    
    3. 成本控制：
       - 使用更便宜的模型（如 gpt-3.5-turbo）进行初步处理
       - 减少 max_gleanings 参数降低重试次数
       - 禁用不必要的功能（如 claim_extraction）
    
    4. 缓存策略：
       - 使用文件缓存避免重复计算
       - 对于生产环境，考虑使用 Redis 或其他缓存系统
    
    5. 分块策略：
       - 根据文档类型调整 chunk_size
       - 适当的 overlap 确保上下文连续性
    """
    
    print(tips)


if __name__ == "__main__":
    print("=" * 60)
    print("GraphRAG Python API 使用示例")
    print("=" * 60)
    
    # 设置项目
    project_dir = setup_project()
    print(f"\n项目已创建在: {project_dir}")
    
    # 运行索引（需要有效的 API 密钥）
    # asyncio.run(run_indexing_example())
    
    # 查询示例
    query_example()
    
    # 高级用法
    advanced_usage()
    
    # 性能优化
    performance_tips()
    
    print("\n" + "=" * 60)
    print("完整文档请访问: https://microsoft.github.io/graphrag")
    print("=" * 60)