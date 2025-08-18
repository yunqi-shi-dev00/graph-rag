#!/usr/bin/env python3
"""
GraphRAG FastAPI Server
GraphRAG REST API 服务
"""

import os
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import logging

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# 添加GraphRAG到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="GraphRAG API",
    description="基于知识图谱的检索增强生成API服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求和响应模型
class QueryRequest(BaseModel):
    """查询请求模型"""
    question: str = Field(..., description="用户问题", example="什么是量子计算？")
    search_type: str = Field("local", description="搜索类型: local或global")
    max_tokens: Optional[int] = Field(1024, description="最大返回token数")
    temperature: Optional[float] = Field(0.7, description="生成温度")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "什么是量子计算？",
                "search_type": "local",
                "max_tokens": 1024,
                "temperature": 0.7
            }
        }

class QueryResponse(BaseModel):
    """查询响应模型"""
    answer: str = Field(..., description="生成的答案")
    context: Optional[str] = Field(None, description="相关上下文")
    confidence: float = Field(..., description="置信度分数")
    sources: List[str] = Field([], description="信息来源")
    search_type: str = Field(..., description="使用的搜索类型")
    timestamp: str = Field(..., description="查询时间戳")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "量子计算是基于量子力学原理的新型计算方式...",
                "context": "使用local搜索模式",
                "confidence": 0.85,
                "sources": ["quantum_computing.txt"],
                "search_type": "local",
                "timestamp": "2024-01-01T12:00:00"
            }
        }

class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    graph_loaded: bool
    storage_path: str
    version: str
    timestamp: str

class GraphRAGService:
    """GraphRAG服务类"""
    
    def __init__(self, storage_path: str = "./graphrag_project/storage"):
        """初始化服务"""
        self.storage_path = Path(storage_path)
        self.graph_loaded = False
        self.load_graph()
    
    def load_graph(self):
        """加载知识图谱"""
        try:
            if not self.storage_path.exists():
                logger.warning(f"存储目录不存在: {self.storage_path}")
                return False
            
            # 这里应该加载实际的GraphRAG索引
            logger.info(f"从 {self.storage_path} 加载知识图谱...")
            self.graph_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"加载图谱失败: {e}")
            return False
    
    def query(self, request: QueryRequest) -> QueryResponse:
        """执行查询"""
        
        # 模拟查询结果（实际应调用GraphRAG API）
        logger.info(f"执行{request.search_type}查询: {request.question}")
        
        # 根据问题生成模拟答案
        answer = self._generate_answer(request.question, request.search_type)
        
        return QueryResponse(
            answer=answer["answer"],
            context=answer["context"],
            confidence=answer["confidence"],
            sources=answer["sources"],
            search_type=request.search_type,
            timestamp=datetime.now().isoformat()
        )
    
    def _generate_answer(self, question: str, search_type: str) -> Dict[str, Any]:
        """生成答案（模拟）"""
        
        # 简单的关键词匹配逻辑
        if "量子计算" in question or "quantum" in question.lower():
            return {
                "answer": "量子计算是一种基于量子力学原理的计算方式，使用量子比特（qubit）作为基本信息单元。它利用量子叠加和纠缠等特性，在某些问题上具有指数级的计算优势。",
                "context": f"基于{search_type}搜索的结果",
                "confidence": 0.9,
                "sources": ["quantum_computing.txt"]
            }
        elif "AI" in question or "人工智能" in question:
            return {
                "answer": "人工智能（AI）是计算机科学的分支，致力于创建能够执行需要人类智能的任务的系统。包括机器学习、深度学习、自然语言处理等核心技术。",
                "context": f"基于{search_type}搜索的结果",
                "confidence": 0.88,
                "sources": ["artificial_intelligence.txt"]
            }
        elif "区块链" in question or "blockchain" in question.lower():
            return {
                "answer": "区块链是一种分布式账本技术，通过密码学方法实现数据的不可篡改性。具有去中心化、透明性、不可篡改等核心特性。",
                "context": f"基于{search_type}搜索的结果",
                "confidence": 0.85,
                "sources": ["blockchain_technology.txt"]
            }
        elif "5G" in question:
            return {
                "answer": "5G是第五代移动通信技术，提供超高速度（理论峰值20Gbps）、超低延迟（1毫秒）和海量连接能力。支持增强移动宽带、超可靠低延迟通信和大规模机器通信。",
                "context": f"基于{search_type}搜索的结果",
                "confidence": 0.87,
                "sources": ["5g_network.txt"]
            }
        elif "云计算" in question or "cloud" in question.lower():
            return {
                "answer": "云计算是通过互联网提供计算资源和服务的模式。包括IaaS、PaaS、SaaS三种服务模型，以及公有云、私有云、混合云等部署模型。",
                "context": f"基于{search_type}搜索的结果",
                "confidence": 0.86,
                "sources": ["cloud_computing.txt"]
            }
        else:
            return {
                "answer": f"关于'{question}'的查询结果：这是一个示例响应。实际使用时，GraphRAG会在知识图谱中搜索相关信息并生成准确的答案。",
                "context": f"基于{search_type}搜索的结果",
                "confidence": 0.6,
                "sources": ["general_knowledge.txt"]
            }

# 初始化服务
rag_service = GraphRAGService()

# API端点

@app.get("/", tags=["Root"])
async def root():
    """根路径"""
    return {
        "message": "GraphRAG API Server",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """健康检查端点"""
    return HealthResponse(
        status="healthy" if rag_service.graph_loaded else "degraded",
        graph_loaded=rag_service.graph_loaded,
        storage_path=str(rag_service.storage_path),
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def query(request: QueryRequest = Body(...)):
    """
    执行GraphRAG查询
    
    - **question**: 用户的问题
    - **search_type**: 搜索类型 (local/global)
    - **max_tokens**: 最大返回token数
    - **temperature**: 生成温度
    """
    try:
        if not rag_service.graph_loaded:
            raise HTTPException(
                status_code=503,
                detail="知识图谱未加载，请先构建图谱"
            )
        
        response = rag_service.query(request)
        return response
        
    except Exception as e:
        logger.error(f"查询错误: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"查询失败: {str(e)}"
        )

@app.get("/query", response_model=QueryResponse, tags=["Query"])
async def query_get(
    question: str = Query(..., description="用户问题"),
    search_type: str = Query("local", description="搜索类型: local或global")
):
    """
    通过GET请求执行查询（便于测试）
    """
    request = QueryRequest(
        question=question,
        search_type=search_type
    )
    return await query(request)

@app.get("/sources", tags=["Data"])
async def list_sources():
    """列出可用的数据源"""
    data_dir = Path("./graphrag_project/data")
    
    if not data_dir.exists():
        return {"sources": [], "message": "数据目录不存在"}
    
    sources = []
    for file in data_dir.iterdir():
        if file.is_file():
            sources.append({
                "name": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    
    return {
        "sources": sources,
        "total": len(sources),
        "data_dir": str(data_dir)
    }

@app.get("/examples", tags=["Examples"])
async def get_examples():
    """获取示例问题"""
    return {
        "examples": [
            {
                "question": "什么是量子计算？",
                "search_type": "local",
                "category": "量子计算"
            },
            {
                "question": "人工智能的发展历程是怎样的？",
                "search_type": "global",
                "category": "人工智能"
            },
            {
                "question": "区块链技术有哪些应用？",
                "search_type": "local",
                "category": "区块链"
            },
            {
                "question": "5G网络的关键技术是什么？",
                "search_type": "local",
                "category": "5G"
            },
            {
                "question": "云计算的主要服务模型有哪些？",
                "search_type": "local",
                "category": "云计算"
            }
        ]
    }

@app.post("/reload", tags=["Admin"])
async def reload_graph():
    """重新加载知识图谱"""
    try:
        success = rag_service.load_graph()
        if success:
            return {"message": "知识图谱重新加载成功", "status": "success"}
        else:
            return {"message": "知识图谱重新加载失败", "status": "failed"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"重新加载失败: {str(e)}"
        )

def main():
    """主函数"""
    logger.info("启动GraphRAG FastAPI服务器...")
    
    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # 生产环境设置为False
        log_level="info"
    )

if __name__ == "__main__":
    main()