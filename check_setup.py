#!/usr/bin/env python3
"""
GraphRAG 项目设置检查脚本
Check GraphRAG Project Setup Status
"""

import os
import sys
from pathlib import Path
import subprocess

def check_mark(status):
    """返回检查标记"""
    return "✅" if status else "❌"

def check_setup():
    """检查项目设置状态"""
    
    print("="*60)
    print("GraphRAG 项目设置状态检查")
    print("="*60)
    
    checks = []
    
    # 1. Python环境
    print("\n📦 1. Python环境")
    print("-"*40)
    
    venv_exists = Path(".venv").exists()
    checks.append(("虚拟环境", venv_exists))
    print(f"{check_mark(venv_exists)} 虚拟环境 (.venv): {'已创建' if venv_exists else '未创建'}")
    
    # 检查Python版本
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        python_version = result.stdout.strip()
        print(f"✅ Python版本: {python_version}")
        checks.append(("Python", True))
    except:
        print(f"❌ 无法检查Python版本")
        checks.append(("Python", False))
    
    # 2. 依赖包
    print("\n📚 2. 核心依赖包")
    print("-"*40)
    
    packages = ["graphrag", "gradio", "fastapi", "torch", "transformers", "langchain"]
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package}: 已安装")
            checks.append((package, True))
        except ImportError:
            print(f"❌ {package}: 未安装")
            checks.append((package, False))
    
    # 3. 项目结构
    print("\n📁 3. 项目结构")
    print("-"*40)
    
    directories = {
        "GraphRAG项目": "graphrag_project",
        "数据目录": "graphrag_project/data",
        "存储目录": "graphrag_project/storage",
        "配置文件": "graphrag_project/settings.yaml",
        "环境变量": "graphrag_project/.env"
    }
    
    for name, path in directories.items():
        exists = Path(path).exists()
        checks.append((name, exists))
        print(f"{check_mark(exists)} {name}: {path}")
    
    # 4. 数据文件
    print("\n📄 4. 示例数据")
    print("-"*40)
    
    data_dir = Path("graphrag_project/data")
    if data_dir.exists():
        data_files = list(data_dir.glob("*"))
        print(f"✅ 找到 {len(data_files)} 个数据文件:")
        for file in data_files[:5]:
            print(f"   - {file.name} ({file.stat().st_size:,} bytes)")
        checks.append(("示例数据", len(data_files) > 0))
    else:
        print(f"❌ 数据目录不存在")
        checks.append(("示例数据", False))
    
    # 5. 服务脚本
    print("\n🚀 5. 服务脚本")
    print("-"*40)
    
    scripts = {
        "Gradio界面": "gradio_app.py",
        "FastAPI服务": "api_server.py",
        "测试脚本": "test_query.py",
        "构建脚本": "build_graph.py",
        "数据生成": "scripts/generate_sample_data.py"
    }
    
    for name, path in scripts.items():
        exists = Path(path).exists()
        checks.append((name, exists))
        print(f"{check_mark(exists)} {name}: {path}")
    
    # 6. API配置
    print("\n🔑 6. API配置")
    print("-"*40)
    
    env_file = Path("graphrag_project/.env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            has_openai = "OPENAI_API_KEY" in content
            has_real_key = "sk-" in content and "sk-xxxx" not in content
            
            if has_real_key:
                print(f"✅ OpenAI API密钥: 已配置")
                checks.append(("API密钥", True))
            elif has_openai:
                print(f"⚠️  OpenAI API密钥: 需要替换为实际密钥")
                checks.append(("API密钥", False))
            else:
                print(f"❌ OpenAI API密钥: 未配置")
                checks.append(("API密钥", False))
    else:
        print(f"❌ .env文件不存在")
        checks.append(("API密钥", False))
    
    # 7. 知识图谱
    print("\n🗺️ 7. 知识图谱状态")
    print("-"*40)
    
    storage_dir = Path("graphrag_project/storage")
    if storage_dir.exists() and any(storage_dir.iterdir()):
        print(f"✅ 知识图谱: 已构建")
        checks.append(("知识图谱", True))
    else:
        print(f"⚠️  知识图谱: 未构建（需要运行 graphrag index）")
        checks.append(("知识图谱", False))
    
    # 总结
    print("\n" + "="*60)
    print("📊 检查总结")
    print("="*60)
    
    total = len(checks)
    passed = sum(1 for _, status in checks if status)
    percentage = (passed / total) * 100 if total > 0 else 0
    
    print(f"\n总检查项: {total}")
    print(f"通过项: {passed}")
    print(f"失败项: {total - passed}")
    print(f"完成度: {percentage:.1f}%")
    
    if percentage == 100:
        print("\n🎉 恭喜！所有配置已完成，系统可以正常运行。")
    elif percentage >= 80:
        print("\n✅ 基本配置已完成，需要添加API密钥或构建图谱。")
    elif percentage >= 60:
        print("\n⚠️  大部分配置已完成，请检查缺失的组件。")
    else:
        print("\n❌ 配置不完整，请按照README完成设置。")
    
    # 下一步建议
    print("\n💡 下一步建议:")
    print("-"*40)
    
    if not any(status for name, status in checks if name == "API密钥"):
        print("1. 配置OpenAI API密钥:")
        print("   编辑 graphrag_project/.env 文件")
        print("   将 OPENAI_API_KEY='sk-xxxx' 替换为实际密钥")
    
    if not any(status for name, status in checks if name == "知识图谱"):
        print("2. 构建知识图谱:")
        print("   source .venv/bin/activate")
        print("   graphrag index --root ./graphrag_project")
    
    print("\n3. 启动服务:")
    print("   # Gradio界面")
    print("   python gradio_app.py")
    print("   ")
    print("   # 或 FastAPI服务")
    print("   uvicorn api_server:app --reload")
    
    print("\n4. 测试功能:")
    print("   python test_query.py --mode local")
    
    print("\n📖 详细说明请查看: README_GRAPHRAG.md")
    print("="*60)

if __name__ == "__main__":
    check_setup()