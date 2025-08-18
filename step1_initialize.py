#!/usr/bin/env python3
"""
步骤 1: 初始化 GraphRAG 项目
这个脚本演示如何初始化一个新的 GraphRAG 项目
"""

import os
import sys
from pathlib import Path
import subprocess

def initialize_graphrag_project():
    """初始化 GraphRAG 项目"""
    
    print("=" * 60)
    print("GraphRAG 项目初始化脚本")
    print("=" * 60)
    
    # 1. 设置项目根目录
    project_root = Path("./my_graphrag_project")
    
    print(f"\n1. 创建项目目录: {project_root}")
    project_root.mkdir(parents=True, exist_ok=True)
    
    # 2. 初始化 GraphRAG 配置
    print("\n2. 初始化 GraphRAG 配置...")
    print("   运行命令: graphrag init --root ./my_graphrag_project")
    
    try:
        result = subprocess.run(
            ["python", "-m", "graphrag", "init", "--root", str(project_root)],
            capture_output=True,
            text=True,
            check=True
        )
        print("   ✓ 配置初始化成功!")
        print(f"   输出: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"   ✗ 初始化失败: {e}")
        print(f"   错误信息: {e.stderr}")
        return False
    
    # 3. 创建输入数据目录
    input_dir = project_root / "input"
    print(f"\n3. 创建输入数据目录: {input_dir}")
    input_dir.mkdir(parents=True, exist_ok=True)
    
    # 4. 创建示例输入文件
    sample_text = """
    人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。
    
    机器学习是人工智能的一个子领域，它使计算机能够从数据中学习并改进性能，而无需明确编程。
    深度学习是机器学习的一个子集，使用多层神经网络来学习数据的复杂模式。
    
    自然语言处理（NLP）是AI的另一个重要领域，专注于使计算机能够理解、解释和生成人类语言。
    计算机视觉使机器能够解释和理解视觉世界，从数字图像和视频中获取信息。
    
    这些技术正在改变各个行业，包括医疗保健、金融、交通和教育。
    """
    
    sample_file = input_dir / "sample_data.txt"
    print(f"\n4. 创建示例输入文件: {sample_file}")
    sample_file.write_text(sample_text, encoding='utf-8')
    print("   ✓ 示例文件创建成功!")
    
    # 5. 显示项目结构
    print("\n5. 项目结构:")
    for root, dirs, files in os.walk(project_root):
        level = root.replace(str(project_root), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{sub_indent}{file}')
    
    print("\n" + "=" * 60)
    print("✓ GraphRAG 项目初始化完成!")
    print("下一步: 运行 step2_configure.py 配置项目参数")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = initialize_graphrag_project()
    sys.exit(0 if success else 1)