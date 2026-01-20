# -*- coding: utf-8 -*-
import json

print("="*60)
print("测试法律知识库")
print("="*60)

# 读取知识库
with open('data/knowledge_base.json', 'r', encoding='utf-8') as f:
    kb = json.load(f)

print(f"\n共有 {len(kb)} 个法律分类\n")

# 显示每个分类的内容
for category_key, category in kb.items():
    print(f"\n【{category['name']}】")
    print(f"包含 {len(category['cases'])} 个案例类型:")
    for case in category['cases']:
        print(f"  - {case['title']}")
        print(f"    关键词: {', '.join(case['keywords'])}")
        print(f"    法律依据: {len(case['laws'])} 部")

print("\n" + "="*60)
print("测试完成")
