# -*- coding: utf-8 -*-
import json
import os

def create_comprehensive_knowledge_base():
    """创建完整的法律知识库"""
    
    knowledge_base = {
        "labor_law": {
            "name": "劳动法律",
            "cases": [
                # ... (使用上面的完整内容)
            ]
        },
        # ... 其他分类
    }
    
    # 保存到文件
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    file_path = os.path.join(data_dir, "knowledge_base.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 法律知识库已创建: {file_path}")
    
    # 统计信息
    total_cases = sum(len(category["cases"]) for category in knowledge_base.values())
    print(f"✓ 共包含 {len(knowledge_base)} 个法律分类")
    print(f"✓ 共包含 {total_cases} 个案例类型")

if __name__ == "__main__":
    create_comprehensive_knowledge_base()
