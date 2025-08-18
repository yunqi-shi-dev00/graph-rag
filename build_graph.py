#!/usr/bin/env python3
"""
构建知识图谱脚本
Build Knowledge Graph Script
"""

import os
import sys
import argparse
from pathlib import Path
import subprocess
import logging

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def build_graph(
    input_dir: str = "./graphrag_project/data",
    output_dir: str = "./graphrag_project/storage",
    project_root: str = "./graphrag_project",
    chunk_size: int = 1024,
    model_name: str = "gpt-3.5-turbo"
):
    """
    构建知识图谱
    
    Args:
        input_dir: 输入数据目录
        output_dir: 输出存储目录
        project_root: GraphRAG项目根目录
        chunk_size: 文本块大小
        model_name: 使用的模型名称
    """
    
    # 确保目录存在
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    project_path = Path(project_root)
    
    if not input_path.exists():
        logger.error(f"输入目录不存在: {input_dir}")
        return False
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 检查是否有输入文件
    input_files = list(input_path.glob("*.txt")) + list(input_path.glob("*.json"))
    if not input_files:
        logger.error(f"输入目录中没有找到数据文件: {input_dir}")
        return False
    
    logger.info(f"找到 {len(input_files)} 个输入文件")
    for file in input_files[:5]:  # 显示前5个文件
        logger.info(f"  - {file.name}")
    
    # 构建GraphRAG索引
    logger.info("开始构建知识图谱...")
    logger.info(f"项目根目录: {project_root}")
    logger.info(f"使用模型: {model_name}")
    logger.info(f"块大小: {chunk_size}")
    
    try:
        # 使用GraphRAG CLI构建索引
        cmd = [
            "graphrag", "index",
            "--root", str(project_path),
            "--verbose"
        ]
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        # 注意：实际运行需要有效的OpenAI API密钥
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            logger.info("✅ 知识图谱构建成功!")
            logger.info(f"输出保存在: {output_dir}")
            return True
        else:
            logger.error(f"构建失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"构建过程中出错: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="构建GraphRAG知识图谱")
    parser.add_argument(
        "--input_dir",
        default="./graphrag_project/data",
        help="输入数据目录"
    )
    parser.add_argument(
        "--output_dir",
        default="./graphrag_project/storage",
        help="输出存储目录"
    )
    parser.add_argument(
        "--project_root",
        default="./graphrag_project",
        help="GraphRAG项目根目录"
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=1024,
        help="文本块大小"
    )
    parser.add_argument(
        "--model_name",
        default="gpt-3.5-turbo",
        help="使用的模型名称"
    )
    
    args = parser.parse_args()
    
    # 构建图谱
    success = build_graph(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        project_root=args.project_root,
        chunk_size=args.chunk_size,
        model_name=args.model_name
    )
    
    if success:
        logger.info("\n" + "="*50)
        logger.info("知识图谱构建完成!")
        logger.info("下一步：运行查询服务进行测试")
        logger.info("  - Gradio UI: python gradio_app.py")
        logger.info("  - FastAPI: uvicorn api_server:app --reload")
        logger.info("="*50)
    else:
        logger.error("\n知识图谱构建失败，请检查配置和API密钥")
        sys.exit(1)

if __name__ == "__main__":
    main()