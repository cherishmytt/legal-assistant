# -*- coding: utf-8 -*-
import os
import json
from functools import lru_cache
import time

class KnowledgeService:
    """法律知识库服务（优化版）"""
    
    def __init__(self):
        """初始化知识库服务"""
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        print(f"知识库目录: {self.data_dir}")
        
        # 预加载所有法律数据到内存
        self._law_cache = {}
        self._load_all_laws()
        
        # 构建关键词索引
        self._keyword_index = {}
        self._build_keyword_index()
        
        print(f"知识库初始化完成，已加载 {len(self._law_cache)} 个法律类别")
    
    def _load_all_laws(self):
        """预加载所有法律数据到内存"""
        start_time = time.time()
        
        if not os.path.exists(self.data_dir):
            print(f"警告: 数据目录不存在: {self.data_dir}")
            os.makedirs(self.data_dir)
            self._create_default_laws()
            return
        
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        category = filename.replace('.json', '')
                        self._law_cache[category] = data
                        print(f"  ✓ 加载: {category}")
                except Exception as e:
                    print(f"  ✗ 加载失败 {filename}: {e}")
        
        load_time = time.time() - start_time
        print(f"数据加载耗时: {load_time:.2f}秒")
    
    def _build_keyword_index(self):
        """构建关键词索引以加速搜索"""
        print("构建关键词索引...")
        
        for category, law_data in self._law_cache.items():
            # 提取所有可能的关键词
            keywords = set()
            
            # 从标题提取
            title = law_data.get('title', '')
            keywords.update(self._extract_words(title))
            
            # 从类别提取
            keywords.add(category.lower())
            
            # 从法律名称提取
            for law in law_data.get('laws', []):
                law_name = law.get('name', '')
                keywords.update(self._extract_words(law_name))
                
                # 从条文内容提取关键词
                for article in law.get('articles', []):
                    content = article.get('content', '')
                    keywords.update(self._extract_words(content))
            
            # 建立反向索引
            for keyword in keywords:
                if keyword not in self._keyword_index:
                    self._keyword_index[keyword] = []
                self._keyword_index[keyword].append(category)
        
        print(f"关键词索引构建完成，共 {len(self._keyword_index)} 个关键词")
    
    def _extract_words(self, text):
        """从文本中提取关键词"""
        if not text:
            return set()
        
        # 简单的中文分词（可以使用jieba等库优化）
        words = set()
        text_lower = text.lower()
        
        # 常见法律关键词
        legal_terms = [
            '工资', '劳动', '合同', '赔偿', '违约', '解除', '终止',
            '社保', '公积金', '加班', '休假', '辞退', '裁员',
            '欺诈', '侵权', '债务', '借款', '担保', '抵押',
            '房产', '租赁', '物业', '拆迁', '征收',
            '离婚', '抚养', '赡养', '继承', '遗产',
            '交通', '事故', '保险', '医疗', '工伤',
            '刑事', '犯罪', '举报', '证据', '诉讼'
        ]
        
        for term in legal_terms:
            if term in text_lower:
                words.add(term)
        
        return words
    
    def search_relevant_laws(self, keywords, limit=10):
        """
        搜索相关法律（优化版 - 使用索引）
        
        Args:
            keywords: 关键词列表
            limit: 返回结果数量限制
            
        Returns:
            相关法律列表
        """
        start_time = time.time()
        print(f"\n{'='*60}")
        print(f"搜索关键词: {keywords}")
        print(f"{'='*60}")
        
        if not keywords:
            print("警告: 关键词为空")
            return []
        
        # 确保keywords是列表
        if isinstance(keywords, str):
            keywords = [keywords]
        
        # 转换为小写
        keywords_lower = [k.lower() for k in keywords]
        
        # 使用索引快速查找候选类别
        candidate_categories = set()
        for keyword in keywords_lower:
            if keyword in self._keyword_index:
                candidate_categories.update(self._keyword_index[keyword])
        
        print(f"通过索引找到 {len(candidate_categories)} 个候选类别")
        
        # 如果索引没找到，回退到全量搜索
        if not candidate_categories:
            candidate_categories = set(self._law_cache.keys())
            print("使用全量搜索")
        
        results = []
        
        # 对候选类别计算相关度
        for category in candidate_categories:
            law_data = self._law_cache.get(category)
            if not law_data:
                continue
            
            try:
                score = self._calculate_relevance(law_data, keywords_lower)
                
                if score > 0:
                    result = {
                        'category': category,
                        'title': law_data.get('title', category),
                        'laws': law_data.get('laws', []),
                        'procedures': law_data.get('procedures', []),
                        'score': score
                    }
                    results.append(result)
                    print(f"  ✓ 匹配: {category} (分数: {score})")
                
            except Exception as e:
                print(f"  ✗ 处理 {category} 时出错: {e}")
                continue
        
        # 按相关度排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # 移除score字段
        for result in results:
            result.pop('score', None)
        
        # 限制返回数量
        results = results[:limit]
        
        search_time = time.time() - start_time
        print(f"\n搜索完成:")
        print(f"  - 找到 {len(results)} 条相关法律")
        print(f"  - 耗时: {search_time:.3f}秒")
        print(f"{'='*60}\n")
        
        return results
    
    def _calculate_relevance(self, law_data, keywords_lower):
        """计算相关度分数"""
        score = 0
        
        # 1. 标题匹配（权重最高）
        title = law_data.get('title', '').lower()
        for keyword in keywords_lower:
            if keyword in title:
                score += 10
        
        # 2. 类别匹配
        category = law_data.get('category', '').lower()
        for keyword in keywords_lower:
            if keyword in category:
                score += 8
        
        # 3. 法律条文匹配
        laws = law_data.get('laws', [])
        for law in laws:
            law_name = law.get('name', '').lower()
            for keyword in keywords_lower:
                if keyword in law_name:
                    score += 5
            
            # 检查具体条文
            articles = law.get('articles', [])
            for article in articles:
                content = article.get('content', '').lower()
                for keyword in keywords_lower:
                    if keyword in content:
                        score += 2
        
        # 4. 处理流程匹配
        procedures = law_data.get('procedures', [])
        for procedure in procedures:
            procedure_lower = str(procedure).lower()
            for keyword in keywords_lower:
                if keyword in procedure_lower:
                    score += 3
        
        return score
    
    def _create_default_laws(self):
        """创建默认法律数据"""
        print("创建默认法律数据...")
        
        # 刑事法律
        criminal_law = {
            "category": "刑事法律",
            "title": "刑事犯罪相关法律规定",
            "laws": [
                {
                    "name": "中华人民共和国刑法",
                    "articles": [
                        {
                            "number": "第二百零一条（逃税罪）",
                            "content": "纳税人采取欺骗、隐瞒手段进行虚假纳税申报或者不申报，逃避缴纳税款数额较大并且占应纳税额百分之十以上的，处三年以下有期徒刑或者拘役，并处罚金；数额巨大并且占应纳税额百分之三十以上的，处三年以上七年以下有期徒刑，并处罚金。"
                        },
                        {
                            "number": "第二百零五条（虚开发票罪）",
                            "content": "虚开增值税专用发票或者虚开用于骗取出口退税、抵扣税款的其他发票的，处三年以下有期徒刑或者拘役，并处二万元以上二十万元以下罚金。"
                        },
                        {
                            "number": "第二百六十六条（诈骗罪）",
                            "content": "诈骗公私财物，数额较大的，处三年以下有期徒刑、拘役或者管制，并处或者单处罚金；数额巨大或者有其他严重情节的，处三年以上十年以下有期徒刑，并处罚金。"
                        }
                    ]
                }
            ],
            "procedures": [
                "发现犯罪线索后，应及时向公安机关、检察院或相关部门举报",
                "举报可以采用书面或口头形式，实名或匿名均可",
                "保存好相关证据材料，但不得采用违法手段获取",
                "配合司法机关调查，如实提供情况",
                "举报人的合法权益受法律保护"
            ]
        }
        
        # 举报指南
        reporting_guide = {
            "category": "举报维权",
            "title": "公民举报权利与义务",
            "laws": [
                {
                    "name": "中华人民共和国宪法",
                    "articles": [
                        {
                            "number": "第四十一条",
                            "content": "中华人民共和国公民对于任何国家机关和国家工作人员，有提出批评和建议的权利；对于任何国家机关和国家工作人员的违法失职行为，有向有关国家机关提出申诉、控告或者检举的权利。"
                        }
                    ]
                },
                {
                    "name": "刑事诉讼法",
                    "articles": [
                        {
                            "number": "第一百一十条",
                            "content": "任何单位和个人发现有犯罪事实或者犯罪嫌疑人，有权利也有义务向公安机关、人民检察院或者人民法院报案或者举报。"
                        }
                    ]
                }
            ],
            "procedures": [
                "确认举报事项：明确要举报的违法犯罪行为",
                "收集证据：在合法范围内收集相关证据材料",
                "选择举报途径：公安机关、检察院、纪委、税务局等",
                "提交举报材料：可实名或匿名，建议实名以便反馈",
                "配合调查：如实提供情况，不得作伪证",
                "保护自身安全：注意保密，避免打草惊蛇"
            ]
        }
        
        # 证据收集
        evidence_guide = {
            "category": "证据规则",
            "title": "合法证据收集指南",
            "laws": [
                {
                    "name": "中华人民共和国民事诉讼法",
                    "articles": [
                        {
                            "number": "第六十三条",
                            "content": "证据包括：（一）当事人的陈述；（二）书证；（三）物证；（四）视听资料；（五）电子数据；（六）证人证言；（七）鉴定意见；（八）勘验笔录。证据必须查证属实，才能作为认定事实的根据。"
                        },
                        {
                            "number": "第七十条",
                            "content": "以侵害他人合法权益或者违反法律禁止性规定的方法取得的证据，不能作为认定案件事实的依据。"
                        }
                    ]
                }
            ],
            "procedures": [
                "合法收集：不得侵犯他人隐私权、不得非法侵入他人住宅",
                "书证收集：合同、收据、聊天记录、邮件等",
                "录音录像：在不侵犯隐私的前提下，可以录制与案件相关的音视频",
                "证人证言：寻找知情人作证，记录证人信息",
                "电子数据：保存原始数据，避免篡改",
                "及时固定：证据可能灭失的，应及时申请保全",
                "禁止行为：不得伪造、变造证据；不得威胁、引诱证人作伪证"
            ]
        }
        
        # 保存文件
        laws_to_create = [
            ('criminal_law.json', criminal_law),
            ('reporting_guide.json', reporting_guide),
            ('evidence_collection.json', evidence_guide)
        ]
        
        for filename, data in laws_to_create:
            filepath = os.path.join(self.data_dir, filename)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  ✓ 创建: {filename}")
                self._law_cache[filename.replace('.json', '')] = data
            except Exception as e:
                print(f"  ✗ 创建失败 {filename}: {e}")
    
    @lru_cache(maxsize=100)
    def get_law_by_category(self, category):
        """根据类别获取法律（带缓存）"""
        return self._law_cache.get(category)
    
    def get_all_categories(self):
        """获取所有法律类别"""
        return list(self._law_cache.keys())
    
    def get_statistics(self):
        """获取知识库统计信息"""
        total_laws = 0
        total_articles = 0
        
        for law_data in self._law_cache.values():
            laws = law_data.get('laws', [])
            total_laws += len(laws)
            for law in laws:
                total_articles += len(law.get('articles', []))
        
        return {
            'categories': len(self._law_cache),
            'laws': total_laws,
            'articles': total_articles
        }


# 测试代码
if __name__ == "__main__":
    print("测试知识库服务...")
    
    service = KnowledgeService()
    
    # 显示统计信息
    stats = service.get_statistics()
    print(f"\n知识库统计:")
    print(f"  - 类别数: {stats['categories']}")
    print(f"  - 法律数: {stats['laws']}")
    print(f"  - 条文数: {stats['articles']}")
    
    # 测试搜索
    test_keywords = ['逃税', '举报', '证据']
    print(f"\n测试搜索: {test_keywords}")
    
    results = service.search_relevant_laws(test_keywords, limit=5)
    
    print(f"\n搜索结果:")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['category']} - {result['title']}")
