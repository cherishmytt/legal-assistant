# -*- coding: utf-8 -*-
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("测试导入...")

try:
    print("\n1. 测试导入 Config...")
    from config import Config
    print("   ✓ Config 导入成功")
    
    print("\n2. 测试导入 Database...")
    from models.database import Database
    print("   ✓ Database 导入成功")
    
    print("\n3. 测试导入 AIService...")
    from services.ai_service import AIService
    print("   ✓ AIService 导入成功")
    
    print("\n4. 测试导入 KnowledgeService...")
    from services.knowledge_service import KnowledgeService
    print("   ✓ KnowledgeService 导入成功")
    
    print("\n5. 测试导入 ReportGenerator...")
    from services.report_generator import ReportGenerator
    print("   ✓ ReportGenerator 导入成功")
    
    print("\n" + "="*50)
    print("所有导入测试通过！")
    print("="*50)
    
    # 测试实例化
    print("\n测试实例化...")
    ai_service = AIService()
    print("✓ AIService 实例化成功")
    
except ImportError as e:
    print(f"\n✗ 导入错误: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"\n✗ 其他错误: {e}")
    import traceback
    traceback.print_exc()
