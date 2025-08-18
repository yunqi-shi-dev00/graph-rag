#!/usr/bin/env python3
"""
GraphRAG查询测试脚本
Test GraphRAG Query Functionality
"""

import os
import sys
import json
import requests
from pathlib import Path
import logging
from typing import Dict, Any

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GraphRAGTester:
    """GraphRAG测试类"""
    
    def __init__(self, api_url: str = "http://localhost:8000"):
        """
        初始化测试器
        
        Args:
            api_url: API服务器地址
        """
        self.api_url = api_url
    
    def test_health(self) -> bool:
        """测试健康检查端点"""
        try:
            response = requests.get(f"{self.api_url}/health")
            if response.status_code == 200:
                data = response.json()
                logger.info(f"健康检查成功: {data}")
                return data.get("graph_loaded", False)
            else:
                logger.error(f"健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"连接失败: {e}")
            return False
    
    def test_query(self, question: str, search_type: str = "local") -> Dict[str, Any]:
        """
        测试查询端点
        
        Args:
            question: 测试问题
            search_type: 搜索类型
            
        Returns:
            查询结果
        """
        try:
            payload = {
                "question": question,
                "search_type": search_type,
                "max_tokens": 1024,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.api_url}/query",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"查询失败: {response.status_code}")
                logger.error(f"错误详情: {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"查询异常: {e}")
            return None
    
    def run_tests(self):
        """运行所有测试"""
        
        print("="*60)
        print("GraphRAG 查询功能测试")
        print("="*60)
        
        # 1. 健康检查
        print("\n1. 健康检查测试")
        print("-"*40)
        health_ok = self.test_health()
        if not health_ok:
            print("❌ API服务器未运行或图谱未加载")
            print("请先运行: uvicorn api_server:app --reload")
            return
        print("✅ API服务器正常运行")
        
        # 2. 查询测试
        print("\n2. 查询功能测试")
        print("-"*40)
        
        test_cases = [
            ("什么是量子计算？", "local"),
            ("人工智能的发展历程是怎样的？", "global"),
            ("区块链技术有哪些应用？", "local"),
            ("5G网络与4G相比有什么优势？", "global"),
            ("云计算的主要服务模型有哪些？", "local")
        ]
        
        for i, (question, search_type) in enumerate(test_cases, 1):
            print(f"\n测试 {i}: {question}")
            print(f"搜索类型: {search_type}")
            
            result = self.test_query(question, search_type)
            
            if result:
                print(f"✅ 查询成功")
                print(f"答案预览: {result['answer'][:100]}...")
                print(f"置信度: {result.get('confidence', 0):.2%}")
                print(f"数据源: {', '.join(result.get('sources', []))}")
            else:
                print(f"❌ 查询失败")
        
        # 3. 获取示例
        print("\n3. 获取示例问题")
        print("-"*40)
        try:
            response = requests.get(f"{self.api_url}/examples")
            if response.status_code == 200:
                examples = response.json()["examples"]
                print(f"✅ 获取到 {len(examples)} 个示例问题")
                for ex in examples[:3]:
                    print(f"  - {ex['question']} ({ex['category']})")
            else:
                print("❌ 获取示例失败")
        except Exception as e:
            print(f"❌ 获取示例异常: {e}")
        
        # 4. 列出数据源
        print("\n4. 列出数据源")
        print("-"*40)
        try:
            response = requests.get(f"{self.api_url}/sources")
            if response.status_code == 200:
                sources_data = response.json()
                sources = sources_data.get("sources", [])
                print(f"✅ 找到 {len(sources)} 个数据源")
                for source in sources:
                    print(f"  - {source['name']} ({source['size']:,} bytes)")
            else:
                print("❌ 获取数据源失败")
        except Exception as e:
            print(f"❌ 获取数据源异常: {e}")
        
        print("\n" + "="*60)
        print("测试完成!")
        print("="*60)

def test_local_module():
    """测试本地模块（不需要API服务器）"""
    
    print("="*60)
    print("GraphRAG 本地模块测试")
    print("="*60)
    
    # 添加项目路径
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # 尝试导入GraphRAG模块
        from gradio_app import GraphRAGInterface
        
        print("\n1. 初始化GraphRAG接口")
        rag = GraphRAGInterface()
        print(f"✅ 接口初始化成功")
        print(f"图谱加载状态: {'已加载' if rag.graph_loaded else '未加载'}")
        
        print("\n2. 执行本地查询测试")
        test_questions = [
            "什么是量子计算？",
            "AI的核心技术有哪些？",
            "区块链的特点是什么？"
        ]
        
        for question in test_questions:
            print(f"\n问题: {question}")
            result = rag.query(question, "local")
            print(f"答案: {result['answer'][:150]}...")
            print(f"置信度: {result.get('confidence', 0):.2%}")
        
        print("\n✅ 本地模块测试完成")
        
    except ImportError as e:
        print(f"❌ 无法导入模块: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="测试GraphRAG查询功能")
    parser.add_argument(
        "--mode",
        choices=["api", "local", "both"],
        default="both",
        help="测试模式: api(测试API服务器), local(测试本地模块), both(两者都测试)"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="API服务器地址"
    )
    
    args = parser.parse_args()
    
    if args.mode in ["local", "both"]:
        test_local_module()
        print()
    
    if args.mode in ["api", "both"]:
        tester = GraphRAGTester(args.api_url)
        tester.run_tests()

if __name__ == "__main__":
    main()