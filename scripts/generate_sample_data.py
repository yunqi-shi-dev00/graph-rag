#!/usr/bin/env python3
"""
Generate sample data for GraphRAG testing
生成用于GraphRAG测试的示例数据
"""

import os
import json
from pathlib import Path

def generate_tech_documents():
    """生成技术相关的文档"""
    
    documents = {
        "blockchain_technology.txt": """
区块链技术：去中心化的未来

区块链是一种分布式账本技术，它通过密码学方法将数据记录链接成不可篡改的链式结构。每个区块包含一批交易记录，
并通过哈希值与前一个区块相连，形成一个连续的链条。

核心特性：
1. 去中心化：没有单一的控制点，数据分布在网络的多个节点上
2. 透明性：所有参与者都可以查看完整的交易历史
3. 不可篡改：一旦数据被记录，就极难被修改或删除
4. 共识机制：通过工作量证明（PoW）或权益证明（PoS）等机制达成共识

应用领域：
- 加密货币：比特币、以太坊等数字货币
- 供应链管理：追踪产品从生产到消费的全过程
- 智能合约：自动执行的合约条款
- 数字身份：安全的身份验证和管理
- 医疗记录：安全共享患者医疗信息

挑战与机遇：
区块链技术面临着可扩展性、能源消耗和监管等挑战。但随着技术的不断发展，
如第二层解决方案和更高效的共识机制的出现，区块链有望在更多领域发挥重要作用。
""",
        
        "5g_network.txt": """
5G网络：连接万物的高速通道

5G是第五代移动通信技术，它不仅仅是4G的升级，而是一次通信技术的革命。
5G网络提供了前所未有的速度、低延迟和大规模设备连接能力。

技术特点：
1. 超高速度：理论峰值速度可达20Gbps
2. 超低延迟：延迟可低至1毫秒
3. 海量连接：每平方公里可支持100万个设备连接
4. 网络切片：为不同应用提供定制化的网络服务

关键技术：
- 毫米波：使用24GHz以上的高频段
- 大规模MIMO：使用大量天线提高频谱效率
- 波束成形：定向传输信号，提高覆盖和容量
- 边缘计算：将计算资源部署在网络边缘

应用场景：
1. 增强移动宽带（eMBB）：4K/8K视频、VR/AR应用
2. 超可靠低延迟通信（URLLC）：自动驾驶、远程手术
3. 大规模机器通信（mMTC）：智慧城市、工业物联网

对社会的影响：
5G将推动数字经济的发展，催生新的商业模式和服务。它将使智慧城市、
工业4.0、远程医疗等概念成为现实，深刻改变人们的生活和工作方式。
""",
        
        "cloud_computing.txt": """
云计算：数字化转型的基础设施

云计算是通过互联网提供计算资源和服务的模式，用户可以按需访问计算能力、
存储空间和各种应用程序，而无需拥有和维护物理基础设施。

服务模型：
1. 基础设施即服务（IaaS）：提供虚拟化的计算资源
2. 平台即服务（PaaS）：提供开发和部署应用的平台
3. 软件即服务（SaaS）：提供通过网络访问的应用程序

部署模型：
- 公有云：由第三方提供商运营，对公众开放
- 私有云：专门为单一组织运营
- 混合云：结合公有云和私有云的优势
- 多云：使用多个云服务提供商

主要优势：
1. 成本效益：按使用付费，减少资本支出
2. 可扩展性：根据需求快速扩展或缩减资源
3. 灵活性：随时随地访问资源和应用
4. 可靠性：自动备份和灾难恢复
5. 创新速度：快速部署新服务和应用

主要提供商：
- Amazon Web Services (AWS)
- Microsoft Azure
- Google Cloud Platform
- 阿里云
- 腾讯云

安全考虑：
虽然云计算带来了许多好处，但也引发了数据安全、隐私保护和合规性等问题。
组织需要carefully评估云服务提供商的安全措施，并实施适当的数据治理策略。

未来趋势：
云计算正在向边缘计算、无服务器架构和云原生应用发展。随着AI和机器学习
服务的集成，云计算将成为智能应用的基础平台。
"""
    }
    
    return documents

def generate_sample_json_data():
    """生成JSON格式的示例数据"""
    
    data = {
        "technology_trends_2024": {
            "title": "2024年技术趋势报告",
            "trends": [
                {
                    "name": "生成式AI",
                    "impact": "高",
                    "adoption_rate": "快速增长",
                    "key_players": ["OpenAI", "Google", "Microsoft", "Anthropic"],
                    "challenges": ["伦理问题", "计算成本", "数据隐私"]
                },
                {
                    "name": "量子计算",
                    "impact": "潜在革命性",
                    "adoption_rate": "早期阶段",
                    "key_players": ["IBM", "Google", "Microsoft", "中科院"],
                    "challenges": ["技术复杂性", "成本高昂", "人才短缺"]
                },
                {
                    "name": "元宇宙",
                    "impact": "中等",
                    "adoption_rate": "稳步增长",
                    "key_players": ["Meta", "Microsoft", "Nvidia", "Epic Games"],
                    "challenges": ["用户体验", "互操作性", "内容创建"]
                }
            ]
        }
    }
    
    return data

def main():
    """主函数"""
    # 确保数据目录存在
    data_dir = Path("/workspace/graphrag_project/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文本文档
    print("生成技术文档...")
    documents = generate_tech_documents()
    for filename, content in documents.items():
        filepath = data_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 创建: {filepath}")
    
    # 生成JSON数据
    print("\n生成JSON数据...")
    json_data = generate_sample_json_data()
    json_file = data_dir / "technology_trends.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ 创建: {json_file}")
    
    print(f"\n✅ 成功生成 {len(documents) + 1} 个数据文件到 {data_dir}")
    print("\n文件列表:")
    for file in data_dir.iterdir():
        if file.is_file():
            size = file.stat().st_size
            print(f"  - {file.name} ({size:,} bytes)")

if __name__ == "__main__":
    main()