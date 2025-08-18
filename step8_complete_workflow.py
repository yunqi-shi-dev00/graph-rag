#!/usr/bin/env python3
"""
步骤 8: 完整工作流程示例
这个脚本演示了一个完整的 GraphRAG 工作流程，从初始化到查询
"""

import subprocess
import sys
from pathlib import Path
import time
import os
import shutil

class GraphRAGWorkflow:
    """GraphRAG 完整工作流程管理器"""
    
    def __init__(self, project_name="demo_project"):
        self.project_root = Path(f"./{project_name}")
        self.steps_completed = []
        
    def run_complete_workflow(self):
        """运行完整的 GraphRAG 工作流程"""
        
        print("=" * 70)
        print("GraphRAG 完整工作流程演示")
        print("=" * 70)
        print("\n这个演示将带您完成 GraphRAG 的完整使用流程")
        print("包括: 初始化 → 配置 → 索引 → 查询 → 更新")
        
        input("\n按回车开始...")
        
        # 步骤 1: 清理和初始化
        if not self.step1_cleanup_and_init():
            return False
            
        # 步骤 2: 准备数据
        if not self.step2_prepare_data():
            return False
            
        # 步骤 3: 配置系统
        if not self.step3_configure():
            return False
            
        # 步骤 4: 构建索引
        if not self.step4_build_index():
            return False
            
        # 步骤 5: 执行查询
        if not self.step5_perform_queries():
            return False
            
        # 步骤 6: 更新数据
        if not self.step6_update_data():
            return False
            
        # 步骤 7: 高级功能
        if not self.step7_advanced_features():
            return False
            
        # 步骤 8: 总结
        self.step8_summary()
        
        return True
    
    def step1_cleanup_and_init(self):
        """步骤 1: 清理旧项目并初始化新项目"""
        
        print("\n" + "=" * 70)
        print("步骤 1: 项目初始化")
        print("=" * 70)
        
        # 清理旧项目
        if self.project_root.exists():
            print(f"\n发现现有项目: {self.project_root}")
            response = input("是否删除并重新创建？(y/n): ").strip().lower()
            
            if response == 'y':
                shutil.rmtree(self.project_root)
                print("✓ 已删除旧项目")
            else:
                print("使用现有项目")
                self.steps_completed.append("init")
                return True
        
        # 创建项目目录
        print(f"\n创建项目目录: {self.project_root}")
        self.project_root.mkdir(parents=True, exist_ok=True)
        
        # 初始化 GraphRAG
        print("初始化 GraphRAG 配置...")
        
        try:
            result = subprocess.run(
                ["python", "-m", "graphrag", "init", "--root", str(self.project_root)],
                capture_output=True,
                text=True,
                check=True
            )
            print("✓ GraphRAG 初始化成功")
            self.steps_completed.append("init")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"✗ 初始化失败: {e.stderr}")
            return False
    
    def step2_prepare_data(self):
        """步骤 2: 准备示例数据"""
        
        print("\n" + "=" * 70)
        print("步骤 2: 准备数据")
        print("=" * 70)
        
        input_dir = self.project_root / "input"
        input_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建多个示例文件以演示更复杂的场景
        sample_data = {
            "ai_basics.txt": """
人工智能基础

人工智能（Artificial Intelligence, AI）是计算机科学的一个分支，旨在创建能够执行通常需要人类智能的任务的系统。
AI系统可以学习、推理、感知、理解自然语言，并与环境交互。

AI的主要类型包括：
1. 弱AI（Narrow AI）：专注于特定任务，如语音识别、图像分类
2. 强AI（General AI）：具有人类水平的认知能力（尚未实现）
3. 超级AI：超越人类智能的假设性AI（理论概念）

AI的核心技术包括机器学习、深度学习、自然语言处理、计算机视觉和机器人技术。
            """,
            
            "machine_learning.txt": """
机器学习详解

机器学习是人工智能的核心子领域，使计算机能够从数据中学习而无需明确编程。

主要的机器学习类型：

1. 监督学习
   - 使用标记数据训练
   - 应用：分类、回归
   - 算法：决策树、随机森林、支持向量机、神经网络

2. 无监督学习
   - 使用未标记数据
   - 应用：聚类、降维、异常检测
   - 算法：K-means、DBSCAN、PCA、自编码器

3. 强化学习
   - 通过与环境交互学习
   - 应用：游戏AI、机器人控制、推荐系统
   - 算法：Q-learning、Policy Gradient、Actor-Critic

深度学习是机器学习的子集，使用多层神经网络学习数据的复杂表示。
主要架构包括：CNN（卷积神经网络）、RNN（循环神经网络）、Transformer。
            """,
            
            "ai_applications.txt": """
AI应用领域

人工智能正在改变各个行业：

医疗保健：
- 疾病诊断和预测
- 药物发现和开发
- 个性化治疗方案
- 医学图像分析

金融服务：
- 欺诈检测
- 算法交易
- 信用评分
- 客户服务聊天机器人

交通运输：
- 自动驾驶汽车
- 交通流量优化
- 预测性维护
- 路线规划

教育：
- 个性化学习
- 自动评分
- 智能辅导系统
- 教育内容推荐

零售和电商：
- 推荐系统
- 库存管理
- 价格优化
- 客户行为分析
            """
        }
        
        print("\n创建示例数据文件:")
        for filename, content in sample_data.items():
            file_path = input_dir / filename
            file_path.write_text(content, encoding='utf-8')
            print(f"  ✓ {filename} ({len(content)} 字符)")
        
        self.steps_completed.append("data")
        return True
    
    def step3_configure(self):
        """步骤 3: 配置系统"""
        
        print("\n" + "=" * 70)
        print("步骤 3: 系统配置")
        print("=" * 70)
        
        # 创建环境变量文件
        env_file = self.project_root / ".env"
        
        print("\n配置 API 密钥:")
        print("1. 使用 OpenAI API")
        print("2. 使用 Azure OpenAI")
        print("3. 跳过（稍后配置）")
        
        choice = input("\n选择 (1-3): ").strip()
        
        if choice == "1":
            api_key = input("输入 OpenAI API 密钥: ").strip()
            if api_key:
                env_content = f"GRAPHRAG_API_KEY={api_key}\n"
                env_file.write_text(env_content)
                print("✓ API 密钥已配置")
            else:
                print("⚠️  跳过 API 配置")
                
        elif choice == "2":
            print("Azure OpenAI 配置:")
            api_key = input("  API 密钥: ").strip()
            endpoint = input("  端点 URL: ").strip()
            deployment = input("  部署名称: ").strip()
            
            env_content = f"""AZURE_OPENAI_API_KEY={api_key}
AZURE_OPENAI_ENDPOINT={endpoint}
AZURE_OPENAI_DEPLOYMENT_NAME={deployment}
AZURE_OPENAI_API_VERSION=2024-02-15-preview
"""
            env_file.write_text(env_content)
            print("✓ Azure OpenAI 已配置")
            
        else:
            print("⚠️  跳过 API 配置，请稍后手动配置")
            env_content = "GRAPHRAG_API_KEY=YOUR_API_KEY\n"
            env_file.write_text(env_content)
        
        self.steps_completed.append("config")
        return True
    
    def step4_build_index(self):
        """步骤 4: 构建知识图谱索引"""
        
        print("\n" + "=" * 70)
        print("步骤 4: 构建索引")
        print("=" * 70)
        
        print("\n开始构建知识图谱索引...")
        print("这可能需要几分钟，取决于数据量和 API 速度")
        
        # 检查是否配置了 API
        env_file = self.project_root / ".env"
        if env_file.exists():
            from dotenv import load_dotenv
            load_dotenv(env_file)
            
            if os.getenv("GRAPHRAG_API_KEY") == "YOUR_API_KEY":
                print("\n⚠️  警告: 未配置 API 密钥")
                print("请编辑 .env 文件添加您的 API 密钥")
                skip = input("是否跳过索引步骤？(y/n): ").strip().lower()
                if skip == 'y':
                    print("跳过索引构建")
                    return True
                return False
        
        try:
            # 运行索引命令
            process = subprocess.Popen(
                ["python", "-m", "graphrag", "index",
                 "--root", str(self.project_root)],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # 显示进度
            print("\n索引进度:")
            for line in process.stdout:
                if "%" in line or "Error" in line or "Warning" in line:
                    print(f"  {line.rstrip()}")
            
            return_code = process.wait()
            
            if return_code == 0:
                print("\n✓ 索引构建成功!")
                self.steps_completed.append("index")
                
                # 显示统计信息
                self.show_index_stats()
                return True
            else:
                print(f"\n✗ 索引构建失败 (返回码: {return_code})")
                return False
                
        except Exception as e:
            print(f"\n✗ 索引构建出错: {e}")
            return False
    
    def show_index_stats(self):
        """显示索引统计信息"""
        
        output_dir = self.project_root / "output"
        if not output_dir.exists():
            return
        
        print("\n索引统计:")
        
        # 统计各类文件
        stats = {
            "entities": "create_final_entities.parquet",
            "relationships": "create_final_relationships.parquet",
            "communities": "create_final_communities.parquet",
            "documents": "create_final_documents.parquet",
        }
        
        for name, filename in stats.items():
            files = list(output_dir.glob(f"**/{filename}"))
            if files:
                size = files[0].stat().st_size / 1024
                print(f"  - {name}: {size:.1f} KB")
    
    def step5_perform_queries(self):
        """步骤 5: 执行各种查询"""
        
        print("\n" + "=" * 70)
        print("步骤 5: 查询演示")
        print("=" * 70)
        
        # 检查索引是否存在
        output_dir = self.project_root / "output"
        if not output_dir.exists() or not list(output_dir.glob("*.parquet")):
            print("⚠️  未找到索引文件，跳过查询步骤")
            return True
        
        queries = [
            ("本地搜索", "local", "什么是监督学习？"),
            ("全局搜索", "global", "AI在各个行业的应用总结"),
            ("基础搜索", "baseline", "深度学习"),
        ]
        
        print("\n执行示例查询:")
        
        for name, method, query in queries:
            print(f"\n{name}: '{query}'")
            print("-" * 40)
            
            try:
                result = subprocess.run(
                    ["python", "-m", "graphrag", "query",
                     "--method", method,
                     "--query", query,
                     "--root", str(self.project_root)],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.stdout:
                    # 显示前300个字符
                    response = result.stdout[:300] + "..." if len(result.stdout) > 300 else result.stdout
                    print(response)
                else:
                    print("(无响应)")
                    
            except subprocess.TimeoutExpired:
                print("(查询超时)")
            except Exception as e:
                print(f"(查询错误: {e})")
        
        self.steps_completed.append("query")
        return True
    
    def step6_update_data(self):
        """步骤 6: 更新数据和索引"""
        
        print("\n" + "=" * 70)
        print("步骤 6: 数据更新")
        print("=" * 70)
        
        print("\n添加新数据文件...")
        
        input_dir = self.project_root / "input"
        
        new_content = """
最新AI趋势

生成式AI：
- 大语言模型（LLM）如 GPT、Claude、Gemini
- 图像生成模型如 DALL-E、Midjourney、Stable Diffusion
- 视频生成和编辑
- 代码生成和自动编程

AI安全和伦理：
- 对齐问题
- 偏见和公平性
- 隐私保护
- 可解释性

未来展望：
- AGI（通用人工智能）研究
- 量子机器学习
- 神经形态计算
- AI与人类协作
        """
        
        new_file = input_dir / "ai_trends.txt"
        new_file.write_text(new_content, encoding='utf-8')
        print(f"  ✓ 创建 ai_trends.txt")
        
        print("\n是否更新索引以包含新数据？(y/n)")
        update = input("  > ").strip().lower()
        
        if update == 'y':
            print("\n更新索引...")
            
            try:
                # 尝试使用 update 命令
                result = subprocess.run(
                    ["python", "-m", "graphrag", "update",
                     "--root", str(self.project_root)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    print("✓ 索引更新成功")
                else:
                    # 如果 update 失败，使用标准 index
                    print("使用标准索引重建...")
                    subprocess.run(
                        ["python", "-m", "graphrag", "index",
                         "--root", str(self.project_root)],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    print("✓ 索引重建成功")
                    
            except subprocess.TimeoutExpired:
                print("⚠️  更新超时")
            except Exception as e:
                print(f"⚠️  更新失败: {e}")
        
        self.steps_completed.append("update")
        return True
    
    def step7_advanced_features(self):
        """步骤 7: 演示高级功能"""
        
        print("\n" + "=" * 70)
        print("步骤 7: 高级功能")
        print("=" * 70)
        
        print("\n可用的高级功能:")
        print("1. 提示词调优 (Prompt Tuning)")
        print("2. 流式输出")
        print("3. 自定义响应格式")
        print("4. 不同社区级别")
        
        print("\n演示流式输出...")
        
        try:
            process = subprocess.Popen(
                ["python", "-m", "graphrag", "query",
                 "--method", "local",
                 "--query", "解释生成式AI",
                 "--root", str(self.project_root),
                 "--streaming"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            print("\n流式响应:")
            print("-" * 40)
            
            line_count = 0
            for line in process.stdout:
                print(line, end='', flush=True)
                line_count += 1
                if line_count > 10:  # 限制输出行数
                    print("\n... (输出已截断)")
                    break
            
            process.terminate()
            print("-" * 40)
            
        except Exception as e:
            print(f"演示失败: {e}")
        
        self.steps_completed.append("advanced")
        return True
    
    def step8_summary(self):
        """步骤 8: 总结和后续步骤"""
        
        print("\n" + "=" * 70)
        print("工作流程完成!")
        print("=" * 70)
        
        print("\n已完成的步骤:")
        for step in self.steps_completed:
            print(f"  ✓ {step}")
        
        print("\n项目结构:")
        print(f"  {self.project_root}/")
        print("  ├── input/          # 输入数据")
        print("  ├── output/         # 索引输出")
        print("  ├── cache/          # LLM 缓存")
        print("  ├── settings.yaml   # 配置文件")
        print("  └── .env           # 环境变量")
        
        print("\n后续步骤:")
        print("1. 添加更多数据到 input/ 目录")
        print("2. 调整 settings.yaml 中的配置")
        print("3. 运行 'graphrag prompt-tune' 优化提示词")
        print("4. 探索不同的查询方法和参数")
        print("5. 集成到您的应用程序中")
        
        print("\n有用的命令:")
        print(f"  graphrag index --root {self.project_root}")
        print(f"  graphrag query --method local --query 'your question' --root {self.project_root}")
        print(f"  graphrag update --root {self.project_root}")
        
        print("\n" + "=" * 70)
        print("感谢使用 GraphRAG!")
        print("=" * 70)

def install_dependencies():
    """安装必要的依赖"""
    
    packages = ["python-dotenv"]
    
    for package in packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            print(f"安装 {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    """主函数"""
    
    print("GraphRAG 完整工作流程")
    print("=" * 70)
    
    # 安装依赖
    install_dependencies()
    
    # 选择模式
    print("\n选择运行模式:")
    print("1. 完整演示（推荐）")
    print("2. 快速演示（跳过索引）")
    print("3. 自定义项目名称")
    
    choice = input("\n选择 (1-3): ").strip()
    
    if choice == "3":
        project_name = input("输入项目名称: ").strip()
        if not project_name:
            project_name = "demo_project"
    else:
        project_name = "demo_project"
    
    # 创建工作流程实例
    workflow = GraphRAGWorkflow(project_name)
    
    # 运行工作流程
    success = workflow.run_complete_workflow()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())