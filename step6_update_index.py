#!/usr/bin/env python3
"""
步骤 6: 更新知识图谱索引
这个脚本演示如何在添加新数据后更新现有的知识图谱
"""

import subprocess
import sys
from pathlib import Path
import time
import os

def update_knowledge_graph():
    """更新知识图谱索引"""
    
    print("=" * 60)
    print("GraphRAG 索引更新脚本")
    print("=" * 60)
    
    project_root = Path("./my_graphrag_project")
    
    if not project_root.exists():
        print("✗ 错误: 项目目录不存在，请先运行 step1_initialize.py")
        return False
    
    # 检查现有索引
    output_dir = project_root / "output"
    if not output_dir.exists() or not list(output_dir.glob("*.parquet")):
        print("✗ 错误: 没有找到现有索引")
        print("  请先运行 step3_index.py 构建初始索引")
        return False
    
    # 加载环境变量
    env_file = project_root / ".env"
    if env_file.exists():
        print("\n1. 加载环境变量...")
        from dotenv import load_dotenv
        load_dotenv(env_file)
        print("   ✓ 环境变量加载成功!")
    
    print("\n2. 添加新数据到输入目录...")
    
    # 创建新的示例数据
    input_dir = project_root / "input"
    new_data = """
    量子计算是一种利用量子力学原理进行信息处理的计算方式。
    与传统计算机使用比特（0或1）不同，量子计算机使用量子比特（qubit），可以同时处于多个状态。
    
    量子计算的主要应用包括：
    - 密码学和安全：破解现有加密算法，开发量子安全加密
    - 药物发现：模拟分子相互作用，加速新药开发
    - 金融建模：优化投资组合，风险分析
    - 人工智能：加速机器学习算法，优化神经网络
    
    主要的量子计算技术包括：
    - 超导量子计算：使用超导电路实现量子比特
    - 离子阱量子计算：使用被困离子作为量子比特
    - 拓扑量子计算：利用拓扑态实现容错量子计算
    
    量子计算与人工智能的结合被称为量子机器学习，有望解决传统计算机难以处理的复杂问题。
    """
    
    new_file = input_dir / "quantum_computing.txt"
    
    if not new_file.exists():
        print(f"   创建新文件: {new_file.name}")
        new_file.write_text(new_data, encoding='utf-8')
        print("   ✓ 新数据文件创建成功!")
    else:
        print(f"   文件已存在: {new_file.name}")
    
    # 显示所有输入文件
    input_files = list(input_dir.glob("*.txt"))
    print(f"\n3. 当前输入文件 ({len(input_files)}):")
    for file in input_files:
        file_size = file.stat().st_size
        print(f"   - {file.name} ({file_size} 字节)")
    
    # 备份现有输出（可选）
    print("\n4. 备份现有索引...")
    backup_dir = project_root / "output_backup"
    
    if output_dir.exists() and not backup_dir.exists():
        import shutil
        try:
            shutil.copytree(output_dir, backup_dir)
            print(f"   ✓ 索引已备份到: {backup_dir}")
        except Exception as e:
            print(f"   ⚠️  备份失败: {e}")
    else:
        print("   跳过备份（备份已存在或输出目录不存在）")
    
    # 运行更新命令
    print("\n5. 开始更新知识图谱索引...")
    print("   更新将保留现有索引并添加新数据")
    print("   运行命令: graphrag update --root ./my_graphrag_project")
    
    start_time = time.time()
    
    try:
        # 使用 subprocess 运行更新命令
        process = subprocess.Popen(
            ["python", "-m", "graphrag", "update",
             "--root", str(project_root),
             "--verbose"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("\n" + "-" * 40)
        print("更新过程输出:")
        print("-" * 40)
        
        # 实时显示输出
        for line in process.stdout:
            print(f"   {line.rstrip()}")
        
        # 等待进程完成
        return_code = process.wait()
        
        if return_code == 0:
            elapsed_time = time.time() - start_time
            print("-" * 40)
            print(f"\n   ✓ 索引更新成功!")
            print(f"   耗时: {elapsed_time:.2f} 秒")
        else:
            print(f"\n   ✗ 索引更新失败，返回码: {return_code}")
            
            # 尝试使用标准索引作为替代
            print("\n6. 尝试使用标准索引重建...")
            print("   注意: 这将重建整个索引，而不是增量更新")
            
            use_standard = input("   是否继续？(y/n): ").strip().lower()
            
            if use_standard == 'y':
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
                
                for line in process.stdout:
                    print(f"   {line.rstrip()}")
                
                return_code = process.wait()
                
                if return_code == 0:
                    print("\n   ✓ 索引重建成功!")
                else:
                    return False
            else:
                return False
            
    except subprocess.CalledProcessError as e:
        print(f"\n   ✗ 更新失败: {e}")
        print(f"   错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"\n   ✗ 发生错误: {e}")
        return False
    
    # 验证更新
    print("\n7. 验证更新结果...")
    
    # 检查更新后的输出文件
    update_output_dir = project_root / "update_output"
    
    if update_output_dir.exists():
        print(f"   ✓ 找到更新输出目录: {update_output_dir}")
        
        # 统计文件
        parquet_files = list(update_output_dir.glob("**/*.parquet"))
        print(f"   - Parquet 文件数: {len(parquet_files)}")
    else:
        print("   使用标准输出目录")
        parquet_files = list(output_dir.glob("**/*.parquet"))
        print(f"   - Parquet 文件数: {len(parquet_files)}")
    
    # 测试查询新数据
    print("\n8. 测试查询新数据...")
    test_query = "量子计算有哪些应用？"
    
    print(f"   测试查询: '{test_query}'")
    
    try:
        result = subprocess.run(
            ["python", "-m", "graphrag", "query",
             "--method", "local",
             "--query", test_query,
             "--root", str(project_root)],
            capture_output=True,
            text=True,
            check=False  # 不检查返回码
        )
        
        if "量子" in result.stdout or "quantum" in result.stdout.lower():
            print("   ✓ 新数据已成功索引（在查询结果中找到相关内容）")
        else:
            print("   ⚠️  查询结果中未找到新数据相关内容")
            print("   可能需要调整查询或等待索引完全更新")
        
    except Exception as e:
        print(f"   测试查询失败: {e}")
    
    print("\n" + "=" * 60)
    print("✓ 索引更新演示完成!")
    print("\n重要说明:")
    print("1. 更新索引会保留现有数据并添加新内容")
    print("2. 如果更新失败，可以使用标准索引重建")
    print("3. 定期更新索引以包含最新数据")
    print("\n下一步:")
    print("- 运行 step7_advanced_query.py 探索高级查询功能")
    print("- 运行 step8_complete_workflow.py 查看完整工作流程")
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
    
    success = update_knowledge_graph()
    sys.exit(0 if success else 1)