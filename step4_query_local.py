#!/usr/bin/env python3
"""
步骤 4: 本地搜索查询
这个脚本演示如何使用本地搜索方法查询知识图谱
"""

import subprocess
import sys
from pathlib import Path
import os
import json

def local_search_query():
    """执行本地搜索查询"""
    
    print("=" * 60)
    print("GraphRAG 本地搜索查询")
    print("=" * 60)
    
    project_root = Path("./my_graphrag_project")
    
    if not project_root.exists():
        print("✗ 错误: 项目目录不存在，请先运行 step1_initialize.py")
        return False
    
    # 检查索引输出
    output_dir = project_root / "output"
    if not output_dir.exists() or not list(output_dir.glob("*.parquet")):
        print("✗ 错误: 没有找到索引输出文件")
        print("  请先运行 step3_index.py 构建索引")
        return False
    
    # 加载环境变量
    env_file = project_root / ".env"
    if env_file.exists():
        print("\n1. 加载环境变量...")
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("   ✓ 环境变量加载成功!")
    
    print("\n2. 本地搜索说明:")
    print("   本地搜索适用于需要了解特定实体的详细信息的查询")
    print("   它会搜索与查询最相关的实体及其周围的关系")
    
    # 预定义的示例查询
    example_queries = [
        "什么是人工智能？",
        "机器学习和深度学习有什么关系？",
        "自然语言处理的应用有哪些？",
        "AI 在医疗保健中的应用",
        "计算机视觉是什么？",
    ]
    
    print("\n3. 示例查询:")
    for i, query in enumerate(example_queries, 1):
        print(f"   {i}. {query}")
    
    # 获取用户输入
    print("\n4. 请输入您的查询（或输入数字选择示例）:")
    user_input = input("   > ").strip()
    
    if user_input.isdigit() and 1 <= int(user_input) <= len(example_queries):
        query = example_queries[int(user_input) - 1]
        print(f"   使用示例查询: {query}")
    else:
        query = user_input if user_input else example_queries[0]
    
    print(f"\n5. 执行本地搜索查询: '{query}'")
    print("   运行命令: graphrag query --method local")
    
    try:
        # 构建命令
        cmd = [
            "python", "-m", "graphrag", "query",
            "--method", "local",
            "--query", query,
            "--root", str(project_root),
            "--community-level", "2",  # 使用级别 2 的社区
        ]
        
        # 执行查询
        print("\n" + "-" * 40)
        print("查询结果:")
        print("-" * 40)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        # 显示结果
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("警告/信息:", result.stderr)
        
        print("-" * 40)
        print("\n   ✓ 本地搜索查询成功!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n   ✗ 查询失败: {e}")
        print(f"   错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n   ✗ 发生错误: {e}")
        return False
    
    # 提供更多查询选项
    print("\n6. 高级选项:")
    print("   您还可以尝试以下高级查询选项：")
    print("   - 调整社区级别 (--community-level): 更高的值表示更小的社区")
    print("   - 使用流式输出 (--streaming): 逐步显示响应")
    print("   - 自定义响应格式 (--response-type): 如 '单句话', '3-5个要点' 等")
    
    print("\n7. 尝试另一个查询？(y/n)")
    another = input("   > ").strip().lower()
    
    if another == 'y':
        return local_search_query()  # 递归调用
    
    print("\n" + "=" * 60)
    print("✓ 本地搜索演示完成!")
    print("\n下一步:")
    print("- 运行 step5_query_global.py 尝试全局搜索")
    print("- 运行 step7_advanced_query.py 了解更多高级查询选项")
    print("=" * 60)
    
    return True

def install_dotenv():
    """安装 python-dotenv 包"""
    try:
        import dotenv
    except ImportError:
        print("安装 python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])

if __name__ == "__main__":
    # 确保安装了必要的包
    install_dotenv()
    
    success = local_search_query()
    sys.exit(0 if success else 1)