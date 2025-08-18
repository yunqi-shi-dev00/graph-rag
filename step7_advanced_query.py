#!/usr/bin/env python3
"""
步骤 7: 高级查询功能
这个脚本演示 GraphRAG 的高级查询功能和参数调整
"""

import subprocess
import sys
from pathlib import Path
import json

def advanced_query_features():
    """演示高级查询功能"""
    
    print("=" * 60)
    print("GraphRAG 高级查询功能")
    print("=" * 60)
    
    project_root = Path("./my_graphrag_project")
    
    if not project_root.exists():
        print("✗ 错误: 项目目录不存在，请先运行 step1_initialize.py")
        return False
    
    # 检查索引
    output_dir = project_root / "output"
    if not output_dir.exists() or not list(output_dir.glob("*.parquet")):
        print("✗ 错误: 没有找到索引输出文件")
        print("  请先运行 step3_index.py 构建索引")
        return False
    
    # 加载环境变量
    env_file = project_root / ".env"
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv(env_file)
    
    while True:
        print("\n" + "=" * 60)
        print("选择要演示的高级功能:")
        print("=" * 60)
        print("1. 基础搜索 (Baseline Search)")
        print("2. 漂移搜索 (Drift Search) - 跟踪主题演变")
        print("3. 不同社区级别的查询")
        print("4. 流式输出")
        print("5. 自定义响应格式")
        print("6. 组合查询策略")
        print("7. 性能优化技巧")
        print("0. 退出")
        
        choice = input("\n请选择 (0-7): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            demo_baseline_search(project_root)
        elif choice == "2":
            demo_drift_search(project_root)
        elif choice == "3":
            demo_community_levels(project_root)
        elif choice == "4":
            demo_streaming_output(project_root)
        elif choice == "5":
            demo_custom_response_format(project_root)
        elif choice == "6":
            demo_combined_strategies(project_root)
        elif choice == "7":
            show_performance_tips()
        else:
            print("无效选择，请重试")
    
    print("\n" + "=" * 60)
    print("✓ 高级查询功能演示完成!")
    print("=" * 60)
    
    return True

def demo_baseline_search(project_root):
    """演示基础搜索"""
    print("\n--- 基础搜索演示 ---")
    print("基础搜索是最简单的搜索方法，直接在文本单元中搜索")
    
    query = input("\n输入查询 (或按回车使用默认): ").strip()
    if not query:
        query = "人工智能的定义是什么？"
    
    print(f"\n执行基础搜索: '{query}'")
    
    try:
        result = subprocess.run(
            ["python", "-m", "graphrag", "query",
             "--method", "baseline",
             "--query", query,
             "--root", str(project_root)],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("\n结果:")
        print("-" * 40)
        print(result.stdout)
        print("-" * 40)
        
    except subprocess.CalledProcessError as e:
        print(f"查询失败: {e.stderr}")

def demo_drift_search(project_root):
    """演示漂移搜索"""
    print("\n--- 漂移搜索演示 ---")
    print("漂移搜索可以跟踪主题如何随时间或上下文演变")
    
    # 准备多轮对话
    queries = [
        "什么是人工智能？",
        "它与机器学习有什么关系？",
        "深度学习又是什么？",
    ]
    
    print("\n模拟多轮对话:")
    for i, q in enumerate(queries, 1):
        print(f"{i}. {q}")
    
    print("\n开始漂移搜索...")
    
    for i, query in enumerate(queries):
        print(f"\n第 {i+1} 轮查询: '{query}'")
        
        try:
            result = subprocess.run(
                ["python", "-m", "graphrag", "query",
                 "--method", "drift",
                 "--query", query,
                 "--root", str(project_root)],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.stdout:
                print("响应摘要:")
                # 只显示前200个字符
                response = result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout
                print(response)
            
        except Exception as e:
            print(f"查询失败: {e}")

def demo_community_levels(project_root):
    """演示不同社区级别的影响"""
    print("\n--- 社区级别演示 ---")
    print("社区级别影响查询的粒度：")
    print("- 较低级别 (0-1): 大社区，宏观视角")
    print("- 中等级别 (2-3): 平衡的视角")
    print("- 较高级别 (4+): 小社区，详细视角")
    
    query = input("\n输入查询 (或按回车使用默认): ").strip()
    if not query:
        query = "AI技术的应用领域"
    
    levels = [1, 2, 4]
    
    for level in levels:
        print(f"\n使用社区级别 {level} 查询...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "graphrag", "query",
                 "--method", "global",
                 "--query", query,
                 "--root", str(project_root),
                 "--community-level", str(level)],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.stdout:
                print(f"级别 {level} 结果摘要:")
                # 显示前150个字符
                response = result.stdout[:150] + "..." if len(result.stdout) > 150 else result.stdout
                print(response)
                print("-" * 40)
            
        except Exception as e:
            print(f"级别 {level} 查询失败: {e}")

def demo_streaming_output(project_root):
    """演示流式输出"""
    print("\n--- 流式输出演示 ---")
    print("流式输出可以逐步显示响应，提供更好的用户体验")
    
    query = input("\n输入查询 (或按回车使用默认): ").strip()
    if not query:
        query = "详细解释机器学习的工作原理"
    
    print(f"\n执行流式查询: '{query}'")
    print("(注意: 响应将逐步显示)")
    
    try:
        # 使用 Popen 实现真正的流式输出
        process = subprocess.Popen(
            ["python", "-m", "graphrag", "query",
             "--method", "local",
             "--query", query,
             "--root", str(project_root),
             "--streaming"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("\n流式响应:")
        print("-" * 40)
        
        # 逐行读取输出
        for line in process.stdout:
            print(line, end='', flush=True)
        
        process.wait()
        print("-" * 40)
        
    except Exception as e:
        print(f"流式查询失败: {e}")

def demo_custom_response_format(project_root):
    """演示自定义响应格式"""
    print("\n--- 自定义响应格式演示 ---")
    print("可以指定响应的格式要求")
    
    formats = [
        ("单句话总结", "Single Sentence"),
        ("要点列表", "List of 3-5 bullet points"),
        ("详细段落", "Detailed paragraph with examples"),
        ("对比表格", "Comparison table format"),
        ("FAQ格式", "Q&A format with 3 questions"),
    ]
    
    print("\n可用格式:")
    for i, (name, _) in enumerate(formats, 1):
        print(f"{i}. {name}")
    
    format_choice = input("\n选择格式 (1-5): ").strip()
    
    try:
        idx = int(format_choice) - 1
        if 0 <= idx < len(formats):
            format_name, format_type = formats[idx]
        else:
            format_name, format_type = formats[0]
    except:
        format_name, format_type = formats[0]
    
    query = input("\n输入查询 (或按回车使用默认): ").strip()
    if not query:
        query = "比较不同的AI技术"
    
    print(f"\n使用格式 '{format_name}' 查询: '{query}'")
    
    try:
        result = subprocess.run(
            ["python", "-m", "graphrag", "query",
             "--method", "global",
             "--query", query,
             "--root", str(project_root),
             "--response-type", format_type],
            capture_output=True,
            text=True,
            check=True
        )
        
        print(f"\n{format_name} 格式的响应:")
        print("-" * 40)
        print(result.stdout)
        print("-" * 40)
        
    except subprocess.CalledProcessError as e:
        print(f"查询失败: {e.stderr}")

def demo_combined_strategies(project_root):
    """演示组合查询策略"""
    print("\n--- 组合查询策略演示 ---")
    print("对同一问题使用不同方法，然后比较结果")
    
    query = input("\n输入查询 (或按回车使用默认): ").strip()
    if not query:
        query = "自然语言处理的最新进展"
    
    methods = ["baseline", "local", "global"]
    results = {}
    
    print(f"\n对查询 '{query}' 使用多种方法...")
    
    for method in methods:
        print(f"\n执行 {method} 搜索...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "graphrag", "query",
                 "--method", method,
                 "--query", query,
                 "--root", str(project_root)],
                capture_output=True,
                text=True,
                check=False,
                timeout=30  # 30秒超时
            )
            
            if result.returncode == 0:
                results[method] = result.stdout
                print(f"✓ {method} 完成")
            else:
                results[method] = f"错误: {result.stderr}"
                print(f"✗ {method} 失败")
                
        except subprocess.TimeoutExpired:
            results[method] = "超时"
            print(f"⚠️  {method} 超时")
        except Exception as e:
            results[method] = str(e)
            print(f"✗ {method} 错误: {e}")
    
    # 显示比较结果
    print("\n" + "=" * 60)
    print("结果比较:")
    print("=" * 60)
    
    for method, result in results.items():
        print(f"\n【{method.upper()} 方法】")
        print("-" * 40)
        # 显示前200个字符
        if len(result) > 200:
            print(result[:200] + "...")
        else:
            print(result)
    
    print("\n分析:")
    print("- Baseline: 最快但最简单，直接文本匹配")
    print("- Local: 基于实体和关系，适合具体问题")
    print("- Global: 基于社区摘要，适合宏观问题")

def show_performance_tips():
    """显示性能优化技巧"""
    print("\n" + "=" * 60)
    print("GraphRAG 性能优化技巧")
    print("=" * 60)
    
    tips = [
        ("索引优化", [
            "- 使用适当的分块大小 (1000-1500 tokens)",
            "- 调整重叠大小 (50-200 tokens)",
            "- 启用缓存以避免重复 API 调用",
            "- 使用批处理进行嵌入计算",
        ]),
        ("查询优化", [
            "- 选择合适的搜索方法",
            "- 调整社区级别以平衡速度和质量",
            "- 使用流式输出改善用户体验",
            "- 限制返回的实体和关系数量",
        ]),
        ("成本优化", [
            "- 使用更便宜的模型进行初步处理",
            "- 调整 max_tokens 参数",
            "- 启用请求速率限制",
            "- 使用本地嵌入模型",
        ]),
        ("质量优化", [
            "- 进行提示词调优 (prompt tuning)",
            "- 提供领域特定的实体类型",
            "- 调整温度参数 (0 for 确定性, 0.7 for 创造性)",
            "- 使用多轮提取 (gleanings)",
        ]),
    ]
    
    for category, items in tips:
        print(f"\n{category}:")
        for item in items:
            print(f"  {item}")
    
    print("\n配置示例:")
    print("-" * 40)
    print("""
# 高性能配置
llm:
  concurrent_requests: 50  # 增加并发
  tokens_per_minute: 150000  # 提高限制
  
chunks:
  size: 1200  # 优化的分块大小
  overlap: 100  # 适度的重叠
  
cache:
  type: file  # 启用缓存
  
# 成本优化配置  
llm:
  model: gpt-3.5-turbo  # 更便宜的模型
  max_tokens: 2000  # 限制输出
  
embeddings:
  model: text-embedding-3-small  # 更小的嵌入模型
  batch_size: 32  # 批处理
    """)
    
    input("\n按回车继续...")

def install_dotenv():
    """安装 python-dotenv 包"""
    try:
        import dotenv
    except ImportError:
        print("安装 python-dotenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])

if __name__ == "__main__":
    install_dotenv()
    
    success = advanced_query_features()
    sys.exit(0 if success else 1)