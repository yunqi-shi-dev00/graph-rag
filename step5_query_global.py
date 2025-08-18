#!/usr/bin/env python3
"""
步骤 5: 全局搜索查询
这个脚本演示如何使用全局搜索方法查询知识图谱
"""

import subprocess
import sys
from pathlib import Path
import os

def global_search_query():
    """执行全局搜索查询"""
    
    print("=" * 60)
    print("GraphRAG 全局搜索查询")
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
    
    print("\n2. 全局搜索说明:")
    print("   全局搜索适用于需要综合整个数据集信息的查询")
    print("   它使用社区摘要来提供高层次的见解和主题概览")
    
    # 预定义的示例查询
    example_queries = [
        "总结一下文档中提到的所有主要技术",
        "人工智能的主要应用领域有哪些？",
        "文档中讨论了哪些关键概念？",
        "不同AI技术之间有什么联系？",
        "这些技术对各行业有什么影响？",
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
    
    print(f"\n5. 执行全局搜索查询: '{query}'")
    print("   运行命令: graphrag query --method global")
    
    try:
        # 构建命令
        cmd = [
            "python", "-m", "graphrag", "query",
            "--method", "global",
            "--query", query,
            "--root", str(project_root),
            "--community-level", "2",
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
        print("\n   ✓ 全局搜索查询成功!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n   ✗ 查询失败: {e}")
        print(f"   错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n   ✗ 发生错误: {e}")
        return False
    
    # 比较本地搜索和全局搜索
    print("\n6. 本地搜索 vs 全局搜索:")
    print("   - 本地搜索: 适合具体实体相关的详细问题")
    print("   - 全局搜索: 适合需要综合理解的宏观问题")
    print("   - 动态选择: 可以使用 --dynamic-community-selection 自动选择")
    
    print("\n7. 尝试动态社区选择？(y/n)")
    dynamic = input("   > ").strip().lower()
    
    if dynamic == 'y':
        print("\n8. 使用动态社区选择重新查询...")
        
        cmd.append("--dynamic-community-selection")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True
            )
            
            print("\n动态选择结果:")
            print("-" * 40)
            if result.stdout:
                print(result.stdout)
            print("-" * 40)
            
        except Exception as e:
            print(f"动态查询失败: {e}")
    
    print("\n9. 尝试另一个查询？(y/n)")
    another = input("   > ").strip().lower()
    
    if another == 'y':
        return global_search_query()  # 递归调用
    
    print("\n" + "=" * 60)
    print("✓ 全局搜索演示完成!")
    print("\n下一步:")
    print("- 运行 step6_update_index.py 学习如何更新索引")
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
    
    success = global_search_query()
    sys.exit(0 if success else 1)