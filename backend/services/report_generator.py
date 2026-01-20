# -*- coding: utf-8 -*-
from datetime import datetime
from .ai_service import AIService
from .knowledge_service import KnowledgeService

class ReportGenerator:
    """法律咨询报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.ai_service = AIService()
        self.knowledge_service = KnowledgeService()
        print("报告生成器初始化完成")
    
    def generate_report(self, question):
        """生成完整的法律咨询报告"""
        print(f"\n{'='*60}")
        print(f"开始生成报告")
        print(f"{'='*60}")
        print(f"问题: {question}")
        
        # 1. AI分析
        print(f"\n{'='*60}")
        print("步骤1: AI分析")
        print(f"{'='*60}")
        try:
            ai_analysis = self.ai_service.analyze_question(question)
            print(f"✓ AI分析成功")
            print(f"  - 分析结果类型: {type(ai_analysis)}")
            if isinstance(ai_analysis, dict):
                print(f"  - 包含的键: {list(ai_analysis.keys())}")
                for key, value in ai_analysis.items():
                    if isinstance(value, list):
                        print(f"  - {key}: {len(value)} 项")
                    else:
                        print(f"  - {key}: {type(value).__name__}")
        except Exception as e:
            print(f"✗ AI分析失败: {e}")
            import traceback
            traceback.print_exc()
            # 使用默认值
            ai_analysis = {
                "案由分析": "系统正在分析您的问题，请稍后...",
                "核心争议点": ["正在分析中..."],
                "关键词": ["法律咨询"],
                "行动建议": [
                    "收集和保存所有相关证据材料",
                    "咨询专业律师，了解详细的法律规定",
                    "根据具体情况选择协商、调解、仲裁或诉讼"
                ]
            }
        
        # 2. 搜索相关法律
        print(f"\n{'='*60}")
        print("步骤2: 搜索相关法律")
        print(f"{'='*60}")
        try:
            keywords = ai_analysis.get('关键词', ['法律咨询'])
            print(f"  - 搜索关键词: {keywords}")
            relevant_laws = self.knowledge_service.search_relevant_laws(keywords, limit=5)
            print(f"✓ 找到 {len(relevant_laws)} 条相关法律")
        except Exception as e:
            print(f"✗ 法律搜索失败: {e}")
            relevant_laws = []
        
        # 3. 生成报告 - 确保所有字段都是正确的类型和格式
        print(f"\n{'='*60}")
        print("步骤3: 组装报告")
        print(f"{'='*60}")
        
        # 安全获取并转换数据
        case_analysis = ai_analysis.get('案由分析', '暂无分析')
        if not isinstance(case_analysis, str):
            case_analysis = str(case_analysis)
        
        dispute_points = ai_analysis.get('核心争议点', [])
        if not isinstance(dispute_points, list):
            dispute_points = [str(dispute_points)]
        dispute_points = [str(p) for p in dispute_points]
        
        keywords_list = ai_analysis.get('关键词', [])
        if not isinstance(keywords_list, list):
            keywords_list = [str(keywords_list)]
        keywords_list = [str(k) for k in keywords_list]
        
        action_suggestions = ai_analysis.get('行动建议', [])
        if not isinstance(action_suggestions, list):
            action_suggestions = [str(action_suggestions)]
        action_suggestions = [str(a) for a in action_suggestions]
        
        # 确保至少有一些行动建议
        if len(action_suggestions) == 0:
            action_suggestions = [
                "收集和保存所有相关证据材料，包括合同、聊天记录、邮件等",
                "咨询专业律师，了解详细的法律规定和维权途径",
                "尝试与对方协商解决，保留协商记录",
                "如协商不成，可考虑申请劳动仲裁或提起诉讼",
                "注意诉讼时效，及时采取法律行动"
            ]
        
        report = {
            'question': str(question),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ai_analysis': {
                '案由分析': case_analysis,
                '核心争议点': dispute_points,
                '关键词': keywords_list,
                '行动建议': action_suggestions
            },
            'relevant_laws': self._format_laws(relevant_laws),
            'summary': self._generate_summary(ai_analysis, relevant_laws)
        }
        
        # 打印报告结构用于调试
        print(f"\n生成的报告结构:")
        print(f"  - question: {report['question'][:50]}...")
        print(f"  - timestamp: {report['timestamp']}")
        print(f"  - ai_analysis:")
        print(f"    - 案由分析: {len(report['ai_analysis']['案由分析'])} 字符")
        print(f"    - 核心争议点: {len(report['ai_analysis']['核心争议点'])} 项")
        print(f"    - 关键词: {len(report['ai_analysis']['关键词'])} 个")
        print(f"    - 行动建议: {len(report['ai_analysis']['行动建议'])} 条")
        print(f"  - relevant_laws: {len(report['relevant_laws'])} 条")
        print(f"  - summary: {len(report['summary'])} 字符")
        
        # 打印行动建议内容
        print(f"\n行动建议详情:")
        for i, suggestion in enumerate(report['ai_analysis']['行动建议'], 1):
            print(f"  {i}. {suggestion}")
        
        print(f"\n{'='*60}")
        print("✓ 报告生成完成")
        print(f"{'='*60}\n")
        
        return report
    
    def _format_laws(self, laws):
        """格式化法律数据"""
        if not laws or not isinstance(laws, list):
            return []
        
        formatted_laws = []
        for law in laws:
            try:
                formatted_law = {
                    'category': str(law.get('category', '法律依据')),
                    'title': str(law.get('title', law.get('name', '相关法律'))),
                    'laws': [],
                    'procedures': []
                }
                
                # 格式化法律条文
                if 'laws' in law and isinstance(law['laws'], list):
                    for law_doc in law['laws']:
                        formatted_doc = {
                            'name': str(law_doc.get('name', '法律条文')),
                            'articles': []
                        }
                        
                        if 'articles' in law_doc and isinstance(law_doc['articles'], list):
                            for article in law_doc['articles']:
                                formatted_article = {
                                    'number': str(article.get('number', '')),
                                    'content': str(article.get('content', ''))
                                }
                                formatted_doc['articles'].append(formatted_article)
                        
                        formatted_law['laws'].append(formatted_doc)
                
                # 格式化处理流程
                if 'procedures' in law and isinstance(law['procedures'], list):
                    formatted_law['procedures'] = [str(p) for p in law['procedures']]
                
                formatted_laws.append(formatted_law)
                
            except Exception as e:
                print(f"格式化法律数据时出错: {e}")
                continue
        
        return formatted_laws
    
    def _generate_summary(self, ai_analysis, relevant_laws):
        """生成报告摘要"""
        try:
            case_analysis = ai_analysis.get('案由分析', '')
            dispute_points = ai_analysis.get('核心争议点', [])
            suggestions = ai_analysis.get('行动建议', [])
            
            summary_parts = []
            
            # 案由
            if case_analysis:
                summary_parts.append(f"案由：{case_analysis[:100]}...")
            
            # 争议点
            if dispute_points:
                points_text = "、".join(dispute_points[:3])
                summary_parts.append(f"主要争议点包括：{points_text}")
            
            # 建议
            if suggestions:
                summary_parts.append(f"建议采取{len(suggestions)}项行动措施")
            
            # 法律依据
            if relevant_laws:
                summary_parts.append(f"涉及{len(relevant_laws)}项相关法律规定")
            
            summary = "。".join(summary_parts) + "。"
            return summary
            
        except Exception as e:
            print(f"生成摘要时出错: {e}")
            return "法律咨询报告已生成，请查看详细内容。"
    
    def export_to_dict(self, report):
        """导出报告为字典格式（用于JSON序列化）"""
        try:
            return {
                'question': str(report.get('question', '')),
                'timestamp': str(report.get('timestamp', '')),
                'ai_analysis': {
                    '案由分析': str(report['ai_analysis'].get('案由分析', '')),
                    '核心争议点': list(report['ai_analysis'].get('核心争议点', [])),
                    '关键词': list(report['ai_analysis'].get('关键词', [])),
                    '行动建议': list(report['ai_analysis'].get('行动建议', []))
                },
                'relevant_laws': list(report.get('relevant_laws', [])),
                'summary': str(report.get('summary', ''))
            }
        except Exception as e:
            print(f"导出报告时出错: {e}")
            return report
    
    def export_to_text(self, report):
        """导出报告为文本格式"""
        try:
            lines = []
            lines.append("="*60)
            lines.append("法律咨询报告")
            lines.append("="*60)
            lines.append(f"\n问题：{report['question']}")
            lines.append(f"时间：{report['timestamp']}")
            
            lines.append(f"\n{'='*60}")
            lines.append("一、案由分析")
            lines.append(f"{'='*60}")
            lines.append(report['ai_analysis']['案由分析'])
            
            lines.append(f"\n{'='*60}")
            lines.append("二、核心争议点")
            lines.append(f"{'='*60}")
            for i, point in enumerate(report['ai_analysis']['核心争议点'], 1):
                lines.append(f"{i}. {point}")
            
            lines.append(f"\n{'='*60}")
            lines.append("三、行动建议")
            lines.append(f"{'='*60}")
            for i, suggestion in enumerate(report['ai_analysis']['行动建议'], 1):
                lines.append(f"{i}. {suggestion}")
            
            if report['relevant_laws']:
                lines.append(f"\n{'='*60}")
                lines.append("四、相关法律依据")
                lines.append(f"{'='*60}")
                for law in report['relevant_laws']:
                    lines.append(f"\n【{law['category']}】{law['title']}")
                    if law.get('laws'):
                        for law_doc in law['laws']:
                            lines.append(f"\n  {law_doc['name']}")
                            for article in law_doc.get('articles', []):
                                lines.append(f"    {article['number']}")
                                lines.append(f"    {article['content']}")
            
            lines.append(f"\n{'='*60}")
            lines.append("报告结束")
            lines.append(f"{'='*60}")
            
            return "\n".join(lines)
            
        except Exception as e:
            print(f"导出文本时出错: {e}")
            return str(report)
    
    def validate_report(self, report):
        """验证报告数据完整性"""
        try:
            required_fields = ['question', 'timestamp', 'ai_analysis', 'relevant_laws', 'summary']
            for field in required_fields:
                if field not in report:
                    print(f"警告: 报告缺少字段 '{field}'")
                    return False
            
            required_ai_fields = ['案由分析', '核心争议点', '关键词', '行动建议']
            for field in required_ai_fields:
                if field not in report['ai_analysis']:
                    print(f"警告: AI分析缺少字段 '{field}'")
                    return False
            
            # 检查数据类型
            if not isinstance(report['ai_analysis']['核心争议点'], list):
                print("警告: '核心争议点' 应该是列表类型")
                return False
            
            if not isinstance(report['ai_analysis']['关键词'], list):
                print("警告: '关键词' 应该是列表类型")
                return False
            
            if not isinstance(report['ai_analysis']['行动建议'], list):
                print("警告: '行动建议' 应该是列表类型")
                return False
            
            if not isinstance(report['relevant_laws'], list):
                print("警告: 'relevant_laws' 应该是列表类型")
                return False
            
            print("✓ 报告数据验证通过")
            return True
            
        except Exception as e:
            print(f"验证报告时出错: {e}")
            return False


# 测试代码
if __name__ == "__main__":
    print("测试报告生成器...")
    
    generator = ReportGenerator()
    
    test_question = "老板拖欠我三个月工资，我该怎么办？"
    print(f"\n测试问题: {test_question}")
    
    try:
        report = generator.generate_report(test_question)
        
        print("\n" + "="*60)
        print("验证报告")
        print("="*60)
        is_valid = generator.validate_report(report)
        print(f"报告有效性: {is_valid}")
        
        print("\n" + "="*60)
        print("导出为文本")
        print("="*60)
        text_report = generator.export_to_text(report)
        print(text_report)
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
