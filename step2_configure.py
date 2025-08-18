#!/usr/bin/env python3
"""
步骤 2: 配置 GraphRAG 项目
这个脚本演示如何配置 GraphRAG 的各种参数
"""

import yaml
from pathlib import Path
import os

def configure_graphrag_project():
    """配置 GraphRAG 项目参数"""
    
    print("=" * 60)
    print("GraphRAG 配置脚本")
    print("=" * 60)
    
    project_root = Path("./my_graphrag_project")
    config_file = project_root / "settings.yaml"
    
    if not project_root.exists():
        print("✗ 错误: 项目目录不存在，请先运行 step1_initialize.py")
        return False
    
    print(f"\n1. 读取现有配置文件: {config_file}")
    
    # 读取现有配置
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        print("   ✓ 配置文件读取成功!")
    else:
        print("   ✗ 配置文件不存在，创建默认配置...")
        config = {}
    
    # 2. 配置 LLM 设置
    print("\n2. 配置语言模型 (LLM) 设置:")
    
    # 注意：这里需要根据实际情况配置
    # 可以使用 OpenAI API、Azure OpenAI 或其他兼容的 API
    
    if 'llm' not in config:
        config['llm'] = {}
    
    # 示例配置（需要根据实际情况修改）
    config['llm'] = {
        'api_key': '${GRAPHRAG_API_KEY}',  # 从环境变量读取
        'type': 'openai',  # 或 'azure_openai', 'openai_compatible'
        'model': 'gpt-4o-mini',
        'api_base': None,  # 如果使用自定义端点
        'api_version': None,  # Azure OpenAI 需要
        'deployment_name': None,  # Azure OpenAI 需要
        'max_tokens': 4000,
        'temperature': 0,
        'top_p': 1,
        'n': 1,
        'request_timeout': 180.0,
        'max_retries': 10,
        'retry_delay': 1.0,
        'max_retry_delay': 10.0,
        'concurrent_requests': 25,
        'tokens_per_minute': 0,  # 0 表示无限制
        'requests_per_minute': 0,  # 0 表示无限制
    }
    
    print("   - API 类型: openai")
    print("   - 模型: gpt-4o-mini")
    print("   - 最大令牌数: 4000")
    print("   - 温度: 0")
    
    # 3. 配置嵌入模型设置
    print("\n3. 配置嵌入模型设置:")
    
    if 'embeddings' not in config:
        config['embeddings'] = {}
    
    config['embeddings']['llm'] = {
        'api_key': '${GRAPHRAG_API_KEY}',
        'type': 'openai',
        'model': 'text-embedding-3-small',
        'api_base': None,
        'api_version': None,
        'deployment_name': None,
        'max_tokens': 8191,
        'request_timeout': 180.0,
        'max_retries': 10,
        'retry_delay': 1.0,
        'max_retry_delay': 10.0,
        'concurrent_requests': 25,
        'tokens_per_minute': 0,
        'requests_per_minute': 0,
        'batch_size': 16,
        'batch_max_tokens': 8191,
        'target': 'required',
    }
    
    print("   - 模型: text-embedding-3-small")
    print("   - 批处理大小: 16")
    print("   - 最大令牌数: 8191")
    
    # 4. 配置分块设置
    print("\n4. 配置文本分块设置:")
    
    if 'chunks' not in config:
        config['chunks'] = {}
    
    config['chunks'] = {
        'size': 1200,  # 分块大小
        'overlap': 100,  # 重叠大小
        'group_by_columns': ['id'],  # 按列分组
        'encoding_model': 'cl100k_base',  # 编码模型
    }
    
    print(f"   - 分块大小: {config['chunks']['size']}")
    print(f"   - 重叠大小: {config['chunks']['overlap']}")
    
    # 5. 配置输入设置
    print("\n5. 配置输入设置:")
    
    if 'input' not in config:
        config['input'] = {}
    
    config['input'] = {
        'type': 'file',
        'file_type': 'text',
        'base_dir': 'input',
        'file_encoding': 'utf-8',
        'file_pattern': '.*\\.txt$',  # 匹配所有 .txt 文件
    }
    
    print(f"   - 输入类型: {config['input']['type']}")
    print(f"   - 文件类型: {config['input']['file_type']}")
    print(f"   - 输入目录: {config['input']['base_dir']}")
    print(f"   - 文件模式: {config['input']['file_pattern']}")
    
    # 6. 配置缓存设置
    print("\n6. 配置缓存设置:")
    
    if 'cache' not in config:
        config['cache'] = {}
    
    config['cache'] = {
        'type': 'file',
        'base_dir': 'cache',
    }
    
    print(f"   - 缓存类型: {config['cache']['type']}")
    print(f"   - 缓存目录: {config['cache']['base_dir']}")
    
    # 7. 配置存储设置
    print("\n7. 配置存储设置:")
    
    if 'storage' not in config:
        config['storage'] = {}
    
    config['storage'] = {
        'type': 'file',
        'base_dir': 'output',
    }
    
    print(f"   - 存储类型: {config['storage']['type']}")
    print(f"   - 输出目录: {config['storage']['base_dir']}")
    
    # 8. 配置报告设置
    print("\n8. 配置报告设置:")
    
    if 'reporting' not in config:
        config['reporting'] = {}
    
    config['reporting'] = {
        'type': 'file',
        'base_dir': 'output',
    }
    
    print(f"   - 报告类型: {config['reporting']['type']}")
    print(f"   - 报告目录: {config['reporting']['base_dir']}")
    
    # 9. 配置实体提取设置
    print("\n9. 配置实体提取设置:")
    
    if 'entity_extraction' not in config:
        config['entity_extraction'] = {}
    
    config['entity_extraction'] = {
        'prompt': None,  # 使用默认提示
        'entity_types': [],  # 自动检测实体类型
        'max_gleanings': 1,
    }
    
    print(f"   - 最大提取轮数: {config['entity_extraction']['max_gleanings']}")
    
    # 10. 配置摘要设置
    print("\n10. 配置摘要设置:")
    
    if 'summarize_descriptions' not in config:
        config['summarize_descriptions'] = {}
    
    config['summarize_descriptions'] = {
        'prompt': None,  # 使用默认提示
        'max_length': 500,
    }
    
    print(f"   - 最大摘要长度: {config['summarize_descriptions']['max_length']}")
    
    # 11. 配置社区报告设置
    print("\n11. 配置社区报告设置:")
    
    if 'community_reports' not in config:
        config['community_reports'] = {}
    
    config['community_reports'] = {
        'prompt': None,  # 使用默认提示
        'max_length': 2000,
        'max_input_length': 8000,
    }
    
    print(f"   - 最大报告长度: {config['community_reports']['max_length']}")
    
    # 12. 配置声明提取设置
    print("\n12. 配置声明提取设置:")
    
    if 'claim_extraction' not in config:
        config['claim_extraction'] = {}
    
    config['claim_extraction'] = {
        'enabled': False,  # 默认禁用
        'prompt': None,
        'description': 'Any claims or facts that could be relevant to information discovery.',
        'max_gleanings': 1,
    }
    
    print(f"   - 启用状态: {config['claim_extraction']['enabled']}")
    
    # 13. 配置集群图设置
    print("\n13. 配置集群图设置:")
    
    if 'cluster_graph' not in config:
        config['cluster_graph'] = {}
    
    config['cluster_graph'] = {
        'max_cluster_size': 10,
    }
    
    print(f"   - 最大集群大小: {config['cluster_graph']['max_cluster_size']}")
    
    # 14. 配置 umap 设置
    print("\n14. 配置 UMAP 设置:")
    
    if 'umap' not in config:
        config['umap'] = {}
    
    config['umap'] = {
        'enabled': False,  # 默认禁用
    }
    
    print(f"   - 启用状态: {config['umap']['enabled']}")
    
    # 15. 配置快照设置
    print("\n15. 配置快照设置:")
    
    if 'snapshots' not in config:
        config['snapshots'] = {}
    
    config['snapshots'] = {
        'graphml': False,
        'raw_entities': False,
        'top_level_nodes': False,
    }
    
    print(f"   - GraphML: {config['snapshots']['graphml']}")
    print(f"   - 原始实体: {config['snapshots']['raw_entities']}")
    print(f"   - 顶级节点: {config['snapshots']['top_level_nodes']}")
    
    # 16. 配置本地搜索设置
    print("\n16. 配置本地搜索设置:")
    
    if 'local_search' not in config:
        config['local_search'] = {}
    
    config['local_search'] = {
        'text_unit_prop': 0.5,
        'community_prop': 0.1,
        'conversation_history_max_turns': 5,
        'top_k_entities': 10,
        'top_k_relationships': 10,
        'temperature': 0.0,
        'top_p': 1.0,
        'n': 1,
        'max_tokens': 12000,
        'llm_max_tokens': 2000,
    }
    
    print(f"   - 文本单元权重: {config['local_search']['text_unit_prop']}")
    print(f"   - 社区权重: {config['local_search']['community_prop']}")
    
    # 17. 配置全局搜索设置
    print("\n17. 配置全局搜索设置:")
    
    if 'global_search' not in config:
        config['global_search'] = {}
    
    config['global_search'] = {
        'temperature': 0.0,
        'top_p': 1.0,
        'n': 1,
        'max_tokens': 12000,
        'data_max_tokens': 12000,
        'map_max_tokens': 1000,
        'reduce_max_tokens': 2000,
        'concurrency': 32,
    }
    
    print(f"   - 温度: {config['global_search']['temperature']}")
    print(f"   - 并发数: {config['global_search']['concurrency']}")
    
    # 18. 配置编码模型
    print("\n18. 配置编码模型:")
    
    if 'encoding_model' not in config:
        config['encoding_model'] = 'cl100k_base'
    
    print(f"   - 编码模型: {config['encoding_model']}")
    
    # 19. 配置跳过工作流
    print("\n19. 配置跳过工作流:")
    
    if 'skip_workflows' not in config:
        config['skip_workflows'] = []
    
    print(f"   - 跳过的工作流: {config['skip_workflows'] if config['skip_workflows'] else '无'}")
    
    # 20. 保存配置文件
    print(f"\n20. 保存配置到: {config_file}")
    
    with open(config_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print("   ✓ 配置文件保存成功!")
    
    # 21. 创建 .env 文件示例
    env_file = project_root / ".env"
    print(f"\n21. 创建环境变量文件: {env_file}")
    
    env_content = """# GraphRAG 环境变量配置
# 请将 YOUR_API_KEY 替换为实际的 API 密钥

GRAPHRAG_API_KEY=YOUR_API_KEY

# 如果使用 Azure OpenAI，请配置以下变量：
# AZURE_OPENAI_API_KEY=YOUR_AZURE_API_KEY
# AZURE_OPENAI_ENDPOINT=YOUR_AZURE_ENDPOINT
# AZURE_OPENAI_API_VERSION=2024-02-15-preview
# AZURE_OPENAI_DEPLOYMENT_NAME=YOUR_DEPLOYMENT_NAME

# 其他可选配置：
# GRAPHRAG_LLM_TYPE=openai
# GRAPHRAG_LLM_MODEL=gpt-4o-mini
# GRAPHRAG_EMBEDDING_MODEL=text-embedding-3-small
"""
    
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("   ✓ 环境变量文件创建成功!")
    print("   ⚠️  请编辑 .env 文件，添加您的 API 密钥")
    
    print("\n" + "=" * 60)
    print("✓ GraphRAG 配置完成!")
    print("\n重要提示:")
    print("1. 请编辑 my_graphrag_project/.env 文件，添加您的 API 密钥")
    print("2. 如果使用 Azure OpenAI，请相应修改配置")
    print("3. 运行 step3_index.py 开始构建知识图谱")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    import sys
    success = configure_graphrag_project()
    sys.exit(0 if success else 1)