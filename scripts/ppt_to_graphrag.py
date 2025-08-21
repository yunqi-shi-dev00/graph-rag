#!/usr/bin/env python3
"""
PPT解析数据到GraphRAG格式转换器

该脚本将PPT解析生成的JSON数据转换为GraphRAG可以处理的格式。
主要功能：
1. 合并多个字段内容为单一text字段
2. 保留元数据信息
3. 支持批量处理
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


def transform_ppt_json_to_graphrag(input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    将PPT解析的JSON数据转换为GraphRAG兼容格式
    
    Args:
        input_data: PPT解析生成的JSON数据列表
        
    Returns:
        转换后的GraphRAG兼容格式数据
    """
    transformed_data = []
    
    for item in input_data:
        # 构建主要文本内容
        text_parts = []
        
        # 添加页面标识
        if 'page_number' in item:
            text_parts.append(f"【页面 {item['page_number']}】")
        
        # 添加目录信息
        if 'directory_name' in item:
            text_parts.append(f"【文档】{item['directory_name']}")
        
        # 添加查询内容（通常是任务描述）
        if 'query' in item:
            text_parts.append(f"【任务说明】\n{item['query']}")
        
        # 添加参考输出（实际的内容解析结果）
        if 'ref_orpo' in item:
            text_parts.append(f"【内容解析】\n{item['ref_orpo']}")
        
        # 合并为单一文本字段
        text_content = "\n\n".join(text_parts)
        
        # 构建GraphRAG格式的文档
        graphrag_doc = {
            'text': text_content,  # GraphRAG需要的主要文本字段
            'title': f"{item.get('directory_name', 'Unknown')} - 第{item.get('page_number', 'N/A')}页",
            'metadata': {
                'source_type': 'ppt_analysis',
                'directory_name': item.get('directory_name', ''),
                'image_name': item.get('image_name', ''),
                'page_number': item.get('page_number', 0),
                'display': item.get('display', 1),
                'hashvalue': item.get('hashvalue', ''),
                'inference_time': item.get('inference_time', 0),
                'is_success': item.get('is_success', 1),
                'start_time': item.get('start_time', ''),
                'end_time': item.get('end_time', '')
            }
        }
        
        # 如果有图片路径，也加入元数据
        if 'images' in item and item['images']:
            graphrag_doc['metadata']['image_paths'] = item['images']
        
        transformed_data.append(graphrag_doc)
    
    return transformed_data


def process_file(input_path: Path, output_path: Path, format: str = 'json'):
    """
    处理单个文件的转换
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        format: 输出格式 ('json' 或 'csv')
    """
    # 读取输入文件
    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # 确保输入是列表
    if not isinstance(input_data, list):
        input_data = [input_data]
    
    # 转换数据
    transformed_data = transform_ppt_json_to_graphrag(input_data)
    
    # 保存输出
    if format == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transformed_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已将数据转换并保存到: {output_path}")
    elif format == 'csv':
        # 转换为DataFrame并保存为CSV
        df = pd.DataFrame(transformed_data)
        # 将metadata字典转换为JSON字符串
        df['metadata'] = df['metadata'].apply(json.dumps, ensure_ascii=False)
        df.to_csv(output_path, index=False, encoding='utf-8')
        print(f"✅ 已将数据转换并保存到CSV: {output_path}")
    else:
        raise ValueError(f"不支持的格式: {format}")


def main():
    parser = argparse.ArgumentParser(
        description='将PPT解析的JSON数据转换为GraphRAG兼容格式'
    )
    parser.add_argument(
        'input',
        type=str,
        help='输入的PPT解析JSON文件路径'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='输出文件路径（默认为input_graphrag.json）'
    )
    parser.add_argument(
        '-f', '--format',
        type=str,
        choices=['json', 'csv'],
        default='json',
        help='输出格式（默认为json）'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    # 确定输出路径
    if args.output:
        output_path = Path(args.output)
    else:
        suffix = '.json' if args.format == 'json' else '.csv'
        output_path = input_path.parent / f"{input_path.stem}_graphrag{suffix}"
    
    # 检查输入文件是否存在
    if not input_path.exists():
        print(f"❌ 错误：输入文件不存在: {input_path}")
        return 1
    
    try:
        process_file(input_path, output_path, args.format)
        return 0
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return 1


if __name__ == '__main__':
    exit(main())