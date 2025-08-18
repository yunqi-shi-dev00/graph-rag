#!/usr/bin/env python3
"""
步骤 3: 构建知识图谱索引
这个脚本演示如何运行索引过程来构建知识图谱
"""

import subprocess
import sys
from pathlib import Path
import time
import os

def build_knowledge_graph():
    """构建知识图谱索引"""
    
    print("=" * 60)
    print("GraphRAG 索引构建脚本")
    print("=" * 60)
    
    project_root = Path("./my_graphrag_project")
    
    if not project_root.exists():
        print("✗ 错误: 项目目录不存在，请先运行 step1_initialize.py")
        return False
    
    # 检查环境变量
    env_file = project_root / ".env"
    if env_file.exists():
        print("\n1. 加载环境变量...")
        from dotenv import load_dotenv
        load_dotenv(env_file)
        
        if os.getenv("GRAPHRAG_API_KEY") == "YOUR_API_KEY":
            print("   ⚠️  警告: 请先在 .env 文件中设置您的 API 密钥!")
            print("   编辑 my_graphrag_project/.env 文件")
            return False
        print("   ✓ 环境变量加载成功!")
    
    # 检查输入文件
    input_dir = project_root / "input"
    input_files = list(input_dir.glob("*.txt"))
    
    print(f"\n2. 检查输入文件...")
    if not input_files:
        print("   ✗ 错误: 没有找到输入文件")
        print(f"   请在 {input_dir} 目录下添加 .txt 文件")
        return False
    
    print(f"   找到 {len(input_files)} 个输入文件:")
    for file in input_files:
        file_size = file.stat().st_size
        print(f"   - {file.name} ({file_size} 字节)")
    
    # 运行索引命令
    print("\n3. 开始构建知识图谱索引...")
    print("   这可能需要几分钟时间，取决于数据量和 API 速度")
    print("   运行命令: graphrag index --root ./my_graphrag_project")
    
    start_time = time.time()
    
    try:
        # 使用 subprocess 运行索引命令
        process = subprocess.Popen(
            ["python", "-m", "graphrag", "index", 
             "--root", str(project_root),
             "--verbose"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("\n" + "-" * 40)
        print("索引过程输出:")
        print("-" * 40)
        
        # 实时显示输出
        for line in process.stdout:
            print(f"   {line.rstrip()}")
        
        # 等待进程完成
        return_code = process.wait()
        
        if return_code == 0:
            elapsed_time = time.time() - start_time
            print("-" * 40)
            print(f"\n   ✓ 索引构建成功!")
            print(f"   耗时: {elapsed_time:.2f} 秒")
        else:
            print(f"\n   ✗ 索引构建失败，返回码: {return_code}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n   ✗ 索引构建失败: {e}")
        print(f"   错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n   ✗ 发生错误: {e}")
        return False
    
    # 检查输出文件
    output_dir = project_root / "output"
    
    print("\n4. 检查输出文件...")
    
    if output_dir.exists():
        # 列出所有生成的文件
        output_files = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = Path(root) / file
                output_files.append(file_path)
        
        if output_files:
            print(f"   生成了 {len(output_files)} 个输出文件:")
            
            # 按类型分组显示
            parquet_files = [f for f in output_files if f.suffix == '.parquet']
            json_files = [f for f in output_files if f.suffix == '.json']
            other_files = [f for f in output_files if f.suffix not in ['.parquet', '.json']]
            
            if parquet_files:
                print(f"\n   Parquet 文件 ({len(parquet_files)}):")
                for f in parquet_files[:5]:  # 只显示前5个
                    print(f"     - {f.name}")
                if len(parquet_files) > 5:
                    print(f"     ... 还有 {len(parquet_files) - 5} 个文件")
            
            if json_files:
                print(f"\n   JSON 文件 ({len(json_files)}):")
                for f in json_files[:5]:
                    print(f"     - {f.name}")
                if len(json_files) > 5:
                    print(f"     ... 还有 {len(json_files) - 5} 个文件")
            
            if other_files:
                print(f"\n   其他文件 ({len(other_files)}):")
                for f in other_files[:5]:
                    print(f"     - {f.name}")
                if len(other_files) > 5:
                    print(f"     ... 还有 {len(other_files) - 5} 个文件")
        else:
            print("   ⚠️  警告: 没有找到输出文件")
    else:
        print("   ⚠️  警告: 输出目录不存在")
    
    # 显示重要的输出文件
    print("\n5. 关键输出文件:")
    
    key_files = [
        ("实体", "create_final_entities.parquet"),
        ("关系", "create_final_relationships.parquet"),
        ("文档", "create_final_documents.parquet"),
        ("社区", "create_final_communities.parquet"),
        ("社区报告", "create_final_community_reports.parquet"),
        ("文本单元", "create_final_text_units.parquet"),
        ("节点", "create_final_nodes.parquet"),
    ]
    
    for name, filename in key_files:
        file_path = None
        for f in output_files if 'output_files' in locals() else []:
            if f.name == filename:
                file_path = f
                break
        
        if file_path and file_path.exists():
            size = file_path.stat().st_size / 1024  # KB
            print(f"   ✓ {name}: {filename} ({size:.2f} KB)")
        else:
            print(f"   - {name}: {filename} (未生成)")
    
    print("\n" + "=" * 60)
    print("✓ 知识图谱索引构建完成!")
    print("\n下一步:")
    print("1. 运行 step4_query_local.py 进行本地搜索")
    print("2. 运行 step5_query_global.py 进行全局搜索")
    print("3. 运行 step6_update_index.py 更新索引（添加新数据时）")
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
    
    success = build_knowledge_graph()
    sys.exit(0 if success else 1)