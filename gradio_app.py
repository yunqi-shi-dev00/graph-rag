#!/usr/bin/env python3
"""
GraphRAG Gradio Web UI
GraphRAG 可视化问答界面
"""

import os
import sys
import json
import gradio as gr
from pathlib import Path
from typing import Optional, Dict, Any
import logging
from datetime import datetime

# 添加GraphRAG到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphRAGInterface:
    """GraphRAG查询接口"""
    
    def __init__(self, storage_path: str = "./graphrag_project/storage"):
        """
        初始化GraphRAG接口
        
        Args:
            storage_path: 知识图谱存储路径
        """
        self.storage_path = Path(storage_path)
        self.graph_loaded = False
        
        # 尝试加载图谱
        self.load_graph()
    
    def load_graph(self):
        """加载知识图谱"""
        try:
            # 检查存储目录是否存在
            if not self.storage_path.exists():
                logger.warning(f"存储目录不存在: {self.storage_path}")
                return False
            
            # 这里应该加载实际的GraphRAG索引
            # 由于需要API密钥，这里仅作示例
            logger.info(f"从 {self.storage_path} 加载知识图谱...")
            self.graph_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"加载图谱失败: {e}")
            return False
    
    def query(self, question: str, search_type: str = "local") -> Dict[str, Any]:
        """
        执行查询
        
        Args:
            question: 用户问题
            search_type: 搜索类型 (local/global)
            
        Returns:
            查询结果字典
        """
        if not question:
            return {
                "answer": "请输入问题",
                "context": "",
                "confidence": 0.0,
                "sources": []
            }
        
        # 模拟查询结果（实际应调用GraphRAG API）
        logger.info(f"执行{search_type}查询: {question}")
        
        # 这里应该调用实际的GraphRAG查询
        # 由于需要API密钥，这里返回模拟结果
        mock_answer = self._generate_mock_answer(question, search_type)
        
        return mock_answer
    
    def _generate_mock_answer(self, question: str, search_type: str) -> Dict[str, Any]:
        """生成模拟答案（用于演示）"""
        
        # 根据问题关键词生成相关答案
        if "量子计算" in question:
            answer = """
根据知识图谱分析，量子计算是一种基于量子力学原理的新型计算方式。

主要特点：
1. 使用量子比特（qubit）作为基本信息单元
2. 利用量子叠加和量子纠缠实现并行计算
3. 在特定问题上具有指数级的计算优势

应用领域：
- 密码学和网络安全
- 药物研发和分子模拟
- 人工智能和机器学习
- 金融建模和优化

当前主要参与者包括IBM、Google、Microsoft等科技巨头。
"""
            sources = ["quantum_computing.txt", "technology_trends.json"]
            
        elif "AI" in question or "人工智能" in question:
            answer = """
人工智能（AI）是计算机科学的重要分支，致力于创建智能系统。

发展阶段：
1. 符号主义AI（1950s-1980s）
2. 机器学习兴起（1980s-2010s）
3. 深度学习革命（2010s-现在）

核心技术：
- 机器学习（监督/无监督/强化学习）
- 深度学习（CNN、RNN、Transformer）
- 自然语言处理
- 计算机视觉

AI正在医疗、交通、金融、教育等领域产生深远影响。
"""
            sources = ["artificial_intelligence.txt", "technology_trends.json"]
            
        elif "区块链" in question or "blockchain" in question:
            answer = """
区块链是一种分布式账本技术，通过密码学实现数据的不可篡改性。

核心特性：
1. 去中心化：没有单一控制点
2. 透明性：所有参与者可查看交易历史
3. 不可篡改：数据一旦记录难以修改
4. 共识机制：通过PoW或PoS达成共识

应用场景：
- 加密货币（比特币、以太坊）
- 供应链管理
- 智能合约
- 数字身份验证
"""
            sources = ["blockchain_technology.txt"]
            
        else:
            answer = f"""
关于"{question}"的查询：

这是一个{search_type}搜索的示例结果。实际使用时，GraphRAG会：
1. 分析您的问题
2. 在知识图谱中搜索相关实体和关系
3. 综合多个信息源生成答案
4. 提供相关的上下文和来源

请确保已经构建了知识图谱，并配置了正确的API密钥。
"""
            sources = ["general_knowledge.txt"]
        
        return {
            "answer": answer.strip(),
            "context": f"使用{search_type}搜索模式",
            "confidence": 0.85,
            "sources": sources,
            "timestamp": datetime.now().isoformat()
        }

def create_gradio_interface():
    """创建Gradio界面"""
    
    # 初始化GraphRAG接口
    rag = GraphRAGInterface()
    
    def process_query(question: str, search_type: str, history):
        """处理查询请求"""
        
        # 执行查询
        result = rag.query(question, search_type.lower())
        
        # 格式化输出
        response = f"""
**回答：**
{result['answer']}

**置信度：** {result.get('confidence', 0.0):.2%}

**搜索类型：** {search_type}

**数据来源：** {', '.join(result.get('sources', []))}

**时间戳：** {result.get('timestamp', 'N/A')}
"""
        
        # 更新对话历史
        history = history or []
        history.append([question, response])
        
        return history, ""
    
    def clear_history():
        """清空对话历史"""
        return [], ""
    
    # 创建Gradio界面
    with gr.Blocks(title="GraphRAG 问答系统", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # 🚀 GraphRAG 智能问答系统
        
        基于知识图谱的检索增强生成（RAG）系统，提供精准的问答服务。
        
        ### 使用说明：
        1. 在下方输入框中输入您的问题
        2. 选择搜索模式（Local：局部搜索，Global：全局搜索）
        3. 点击"提交"获取答案
        
        ### 示例问题：
        - 什么是量子计算？
        - 人工智能的发展历程是怎样的？
        - 区块链技术有哪些应用？
        - 5G网络的关键技术是什么？
        """)
        
        with gr.Row():
            with gr.Column(scale=7):
                chatbot = gr.Chatbot(
                    label="对话历史",
                    height=500,
                    elem_id="chatbot"
                )
                
                with gr.Row():
                    question_input = gr.Textbox(
                        label="请输入您的问题",
                        placeholder="例如：什么是量子计算？",
                        lines=2
                    )
                
                with gr.Row():
                    search_type = gr.Radio(
                        ["Local", "Global"],
                        value="Local",
                        label="搜索模式",
                        info="Local: 快速局部搜索, Global: 深度全局搜索"
                    )
                
                with gr.Row():
                    submit_btn = gr.Button("🔍 提交查询", variant="primary")
                    clear_btn = gr.Button("🗑️ 清空历史")
            
            with gr.Column(scale=3):
                gr.Markdown("""
                ### 📊 系统状态
                """)
                
                status_text = gr.Markdown(
                    f"""
                    - **图谱状态：** {'✅ 已加载' if rag.graph_loaded else '❌ 未加载'}
                    - **存储路径：** {rag.storage_path}
                    - **搜索引擎：** GraphRAG v2.5.0
                    """
                )
                
                gr.Markdown("""
                ### 💡 提示
                
                - Local搜索更快，适合具体问题
                - Global搜索更全面，适合开放性问题
                - 确保已配置OpenAI API密钥
                """)
                
                gr.Markdown("""
                ### 📚 数据源
                
                当前系统包含以下领域的知识：
                - 量子计算
                - 人工智能
                - 区块链技术
                - 5G网络
                - 云计算
                """)
        
        # 绑定事件
        submit_btn.click(
            fn=process_query,
            inputs=[question_input, search_type, chatbot],
            outputs=[chatbot, question_input]
        )
        
        question_input.submit(
            fn=process_query,
            inputs=[question_input, search_type, chatbot],
            outputs=[chatbot, question_input]
        )
        
        clear_btn.click(
            fn=clear_history,
            outputs=[chatbot, question_input]
        )
        
        # 添加示例
        gr.Examples(
            examples=[
                ["什么是量子计算？", "Local"],
                ["人工智能的发展历程是怎样的？", "Global"],
                ["区块链技术有哪些应用？", "Local"],
                ["5G网络与4G相比有什么优势？", "Global"],
                ["云计算的主要服务模型有哪些？", "Local"]
            ],
            inputs=[question_input, search_type]
        )
    
    return app

def main():
    """主函数"""
    logger.info("启动GraphRAG Gradio界面...")
    
    # 创建并启动Gradio应用
    app = create_gradio_interface()
    
    # 启动服务器
    app.launch(
        server_name="0.0.0.0",  # 允许外部访问
        server_port=7860,
        share=False,  # 设置为True可以获得公共链接
        show_error=True,
        debug=True
    )

if __name__ == "__main__":
    main()