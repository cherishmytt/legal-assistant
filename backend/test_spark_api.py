# -*- coding: utf-8 -*-
"""
测试讯飞星火API连接
"""
import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from services.ai_service import AIService

def test_api():
    """测试API连接"""
    print("="*60)
    print("讯飞星火API连接测试")
    print("="*60)
    
    # 创建服务实例
    ai_service = AIService()
    
    # 测试简单问题
    test_question = "你好，请介绍一下劳动合同法。"
    
    print(f"\n测试问题: {test_question}")
    print("\n开始测试...\n")
    
    try:
        result = ai_service.analyze_question(test_question)
        
        print("\n" + "="*60)
        print("测试结果")
        print("="*60)
        
        if ai_service.error:
            print(f"✗ 测试失败: {ai_service.error}")
            print("\n请检查:")
            print("1. config/config.py 中的API密钥是否正确")
            print("2. 讯飞控制台中该应用是否已开通星火大模型服务")
            print("3. 账号是否有可用额度")
            print("4. 网络连接是否正常")
        else:
            print("✓ 测试成功!")
            print(f"\n案由分析: {result.get('案由分析', '')[:100]}...")
            print(f"关键词: {result.get('关键词', [])}")
            print(f"行动建议数量: {len(result.get('行动建议', []))}")
        
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_api()
