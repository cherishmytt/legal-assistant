# -*- coding: utf-8 -*-
import json
import ssl
import websocket
import hmac
import hashlib
import base64
from datetime import datetime
from time import mktime
from urllib.parse import urlencode, urlparse
from wsgiref.handlers import format_date_time
import _thread as thread
import os
import re

class AIService:
    """AI分析服务 - 讯飞星火V4.0"""
    
    def __init__(self):
        """初始化AI服务"""
        # 读取JSON配置文件
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            'config', 
            'config.json'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.appid = config.get('SPARK_APPID', '')
            self.api_key = config.get('SPARK_API_KEY', '')
            self.api_secret = config.get('SPARK_API_SECRET', '')
            self.api_url = config.get('SPARK_API_URL', 'wss://spark-api.xf-yun.com/v4.0/chat')
            
            print("✓ 配置文件加载成功")
            
        except FileNotFoundError:
            print(f"✗ 配置文件不存在: {config_path}")
            self.appid = ''
            self.api_key = ''
            self.api_secret = ''
            self.api_url = 'wss://spark-api.xf-yun.com/v4.0/chat'
        except json.JSONDecodeError as e:
            print(f"✗ 配置文件格式错误: {e}")
            self.appid = ''
            self.api_key = ''
            self.api_secret = ''
            self.api_url = 'wss://spark-api.xf-yun.com/v4.0/chat'
        
        self.answer = ""
        self.error = None
        self.mock_mode = False
        
        # 验证配置
        if not self.appid or not self.api_key or not self.api_secret:
            print("⚠ API配置未完成")
            print(f"  APPID: {'已配置' if self.appid else '未配置'}")
            print(f"  API_KEY: {'已配置' if self.api_key else '未配置'}")
            print(f"  API_SECRET: {'已配置' if self.api_secret else '未配置'}")
            print(f"\n请编辑配置文件: {config_path}")
        elif self.appid == "your_app_id":
            print("⚠ 请在配置文件中填入真实的API密钥")
            print(f"配置文件位置: {config_path}")
        else:
            print("✓ AI服务初始化完成")
            print(f"  APPID: {self.appid}")
            print(f"  API版本: Spark Ultra V4.0")
    
    def analyze_question(self, question):
        """
        分析法律问题
        
        Args:
            question: 用户问题
            
        Returns:
            分析结果字典
        """
        print(f"\n{'='*60}")
        print("AI分析开始")
        print(f"{'='*60}")
        print(f"问题: {question}")
        
        # 1. 预分析：问题分类和风险识别
        pre_analysis = self._pre_analyze_question(question)
        print(f"\n预分析结果:")
        print(f"  - 问题类型: {pre_analysis['question_type']}")
        print(f"  - 信息完整度: {pre_analysis['completeness']}")
        print(f"  - 风险等级: {pre_analysis['risk_level']}")
        print(f"  - 是否需要澄清: {pre_analysis['needs_clarification']}")
        
        # 2. 根据预分析结果构建不同的提示词
        prompt = self._build_prompt(question, pre_analysis)
        
        # 3. 调用AI进行深度分析
        try:
            self._call_spark_api(prompt)
            
            if self.error:
                raise Exception(self.error)
            
            # 4. 解析AI返回结果
            analysis = self._parse_ai_response(self.answer, pre_analysis)
            
            print(f"\n✓ AI分析完成")
            print(f"{'='*60}\n")
            
            return analysis
            
        except Exception as e:
            print(f"✗ AI分析失败: {e}")
            return self._get_fallback_analysis(question, pre_analysis)
    
    def _pre_analyze_question(self, question):
        """预分析问题"""
        question_lower = question.lower()
        
        question_type = "general"
        risk_level = "low"
        needs_clarification = False
        completeness = "complete"
        
        # 刑事犯罪关键词
        criminal_keywords = [
            '偷税', '逃税', '假账', '造假', '贪污', '受贿', '诈骗', 
            '盗窃', '抢劫', '杀人', '伤害', '强奸', '绑架', '贩毒',
            '洗钱', '走私', '非法集资', '传销'
        ]
        
        # 强模糊关键词
        strong_vague_keywords = [
            '心情不好', '感觉被骗', '不太清楚', '不太确定',
            '听别人说', '据说', '有人告诉我'
        ]
        
        # 敏感操作关键词
        sensitive_keywords = [
            '如何取证', '怎么偷拍', '怎么录音', '如何窃取', 
            '私下调查', '跟踪', '监控'
        ]
        
        # 具体事实指标
        fact_indicators = {
            '时间': ['年', '月', '日', '天', '小时', '周', '季度'],
            '金额': ['元', '万', '块', '工资', '薪', '钱', '费用', '赔偿'],
            '数量': ['个', '次', '人', '份', '件'],
            '地点': ['公司', '单位', '工厂', '店', '家', '办公室'],
            '关系': ['老板', '领导', '同事', '员工', '经理', '主管'],
            '行为': ['签', '发', '给', '扣', '拖欠', '不给', '要求', '通知']
        }
        
        # 检查刑事犯罪
        if any(keyword in question for keyword in criminal_keywords):
            question_type = "criminal"
            risk_level = "high"
            print("  ⚠ 检测到刑事犯罪相关内容")
        
        # 检查强模糊
        has_strong_vague = any(keyword in question for keyword in strong_vague_keywords)
        
        # 检查长度
        is_too_short = len(question) < 15
        
        # 检查具体事实
        fact_score = 0
        for category, indicators in fact_indicators.items():
            if any(indicator in question for indicator in indicators):
                fact_score += 1
        
        has_sufficient_facts = fact_score >= 2
        
        # 检查数字
        has_numbers = bool(re.search(r'\d+', question))
        
        # 判断是否需要澄清
        if has_strong_vague:
            needs_clarification = True
            completeness = "vague"
            print("  ⚠ 检测到强模糊表述")
        elif is_too_short and not has_sufficient_facts:
            needs_clarification = True
            completeness = "too_short"
            print("  ⚠ 问题过于简短且缺乏具体信息")
        elif not has_sufficient_facts and not has_numbers:
            needs_clarification = True
            completeness = "lack_facts"
            print("  ⚠ 缺少具体事实和数据")
        else:
            completeness = "complete"
            needs_clarification = False
            print("  ✓ 问题信息充分")
        
        # 检查敏感操作
        if any(keyword in question for keyword in sensitive_keywords):
            risk_level = "high"
            print("  ⚠ 检测到敏感操作询问")
        
        # 特殊处理：明确的法律咨询意图
        consultation_indicators = [
            '怎么办', '如何', '怎样', '应该', '可以', '能不能',
            '赔偿', '维权', '仲裁', '起诉', '找哪个部门', '合法吗', '权利'
        ]
        has_clear_intent = any(indicator in question for indicator in consultation_indicators)
        
        if has_clear_intent and has_sufficient_facts:
            needs_clarification = False
            completeness = "complete"
            print("  ✓ 检测到明确的法律咨询意图且信息充分")
        
        return {
            'question_type': question_type,
            'risk_level': risk_level,
            'needs_clarification': needs_clarification,
            'completeness': completeness,
            'has_facts': has_sufficient_facts,
            'fact_score': fact_score,
            'has_numbers': has_numbers
        }
    
    def _build_prompt(self, question, pre_analysis):
        """构建提示词"""
        base_prompt = f"""你是一个专业智能法律咨询助手，接收用户用自然语言描述的法律问题（例如：“老板拖欠工资三个月怎么办？”），对问题进行意图识别和关键信息提取。然后，生成一份清晰、结构化、易于理解的初步咨询报告，重点在于给用户清晰的行动建议：

问题：{question}

"""
        
        if pre_analysis['needs_clarification']:
            base_prompt += """
【重要提示】这个问题信息不够完整或表述过于模糊。

请你：
1. 指出问题中缺少哪些关键信息
2. 列出需要用户澄清的具体问题
3. 不要强行给出法律建议

"""
        else:
            base_prompt += """
【重要提示】用户已提供了较为完整的信息，请给出明确的法律分析和行动建议，如何行动是重点，需要详细。

"""
            
            if pre_analysis['question_type'] == 'criminal':
                base_prompt += """
【刑事案件提示】这个问题涉及刑事犯罪。

请你：
1. 明确指出可能涉及的罪名
2. 强调公民的举报权利和义务
3. 说明应向哪些机关举报（公安、检察院、纪委等）
4. 提醒保护证据的合法方式
5. 警告不要采取违法手段取证
6. 建议寻求专业律师帮助

"""
        
        base_prompt += """
请按以下JSON格式返回分析结果：

{
    "问题评估": {
        "信息完整度": "完整/不完整/模糊",
        "需要澄清": true/false,
        "澄清问题": ["问题1", "问题2"]
    },
    "案由分析": "详细的案由分析...",
    "核心争议点": ["争议点1", "争议点2"],
    "关键词": ["关键词1", "关键词2", "关键词3"],
    "行动建议": ["建议1", "建议2", "建议3"],
    "风险提示": ["风险1", "风险2"],
    "特别说明": "特殊情况说明"
}

注意：
1. 关键词要准确（如：劳动合同、经济补偿、裁员、工资、怀孕、三期保护等）
2. 行动建议要具体、可操作、合法
3. 如果涉及计算（如赔偿金额），请给出计算公式和结果
4. 如果问题信息充分，请给出明确的法律分析
"""
        
        return base_prompt
    
    def _parse_ai_response(self, response, pre_analysis):
        """解析AI响应"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)
                
                analysis = {
                    '问题评估': result.get('问题评估', {
                        '信息完整度': pre_analysis['completeness'],
                        '需要澄清': pre_analysis['needs_clarification'],
                        '澄清问题': []
                    }),
                    '案由分析': result.get('案由分析', '正在分析您的问题...'),
                    '核心争议点': result.get('核心争议点', []),
                    '关键词': result.get('关键词', ['法律咨询']),
                    '行动建议': result.get('行动建议', []),
                    '风险提示': result.get('风险提示', []),
                    '特别说明': result.get('特别说明', '')
                }
                
                return analysis
            else:
                raise ValueError("未找到JSON格式")
                
        except Exception as e:
            print(f"解析AI响应失败: {e}")
            return self._parse_text_response(response, pre_analysis)
    
    def _parse_text_response(self, response, pre_analysis):
        """文本解析后备方案"""
        lines = response.split('\n')
        
        analysis = {
            '问题评估': {
                '信息完整度': pre_analysis['completeness'],
                '需要澄清': pre_analysis['needs_clarification'],
                '澄清问题': []
            },
            '案由分析': '',
            '核心争议点': [],
            '关键词': [],
            '行动建议': [],
            '风险提示': [],
            '特别说明': ''
        }
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if '案由' in line or '分析' in line:
                current_section = '案由分析'
            elif '争议' in line or '焦点' in line:
                current_section = '核心争议点'
            elif '建议' in line:
                current_section = '行动建议'
            elif '关键词' in line:
                current_section = '关键词'
            elif '风险' in line or '注意' in line:
                current_section = '风险提示'
            elif current_section:
                if current_section == '案由分析':
                    analysis['案由分析'] += line + ' '
                elif line.startswith(('1.', '2.', '3.', '•', '-', '·')):
                    content = line.lstrip('0123456789.•-· ')
                    if current_section in ['核心争议点', '行动建议', '风险提示']:
                        analysis[current_section].append(content)
        
        if not analysis['关键词']:
            analysis['关键词'] = self._extract_keywords(response)
        
        return analysis
    
    def _extract_keywords(self, text):
        """提取关键词"""
        legal_keywords = [
            '劳动合同', '工资', '加班', '社保', '辞退', '赔偿', '裁员', '经济补偿',
            '合同', '违约', '欺诈', '侵权', '债务', '借款',
            '房产', '租赁', '物业', '拆迁', '继承', '离婚',
            '抚养', '赡养', '交通事故', '医疗', '保险',
            '怀孕', '三期', '女职工', '产假', '哺乳期',
            '逃税', '偷税', '举报', '证据', '刑事', '犯罪'
        ]
        
        found_keywords = []
        for keyword in legal_keywords:
            if keyword in text:
                found_keywords.append(keyword)
        
        return found_keywords[:5] if found_keywords else ['法律咨询']
    
    def _get_fallback_analysis(self, question, pre_analysis):
        """后备分析结果"""
        if pre_analysis['needs_clarification']:
            case_analysis = """您的问题信息不够完整，为了给您提供准确的法律建议，我需要了解更多细节。"""
            suggestions = [
                "请详细描述具体情况，包括时间、地点、人物、经过",
                "说明涉及的金额、财产或其他利益",
                "列出您目前掌握的证据材料"
            ]
            clarification_questions = [
                "具体发生了什么事情？请描述详细经过",
                "事情发生的时间是什么时候？",
                "涉及的金额或财产价值是多少？"
            ]
        elif pre_analysis['question_type'] == 'criminal':
            case_analysis = """您提到的情况可能涉及刑事犯罪。这是一个严肃的法律问题，需要谨慎处理。

作为公民，您有权利也有义务向相关部门举报违法犯罪行为。但请注意：
1. 不要采取违法手段收集证据
2. 不要私自调查或对抗
3. 保护好自己的人身安全
4. 通过合法途径反映问题"""
            suggestions = [
                "保存您已经掌握的合法证据材料",
                "向公安机关、检察院或相关监管部门举报",
                "咨询专业刑事律师，了解具体的法律程序",
                "注意保护自己的人身安全，不要打草惊蛇",
                "不要采取违法手段获取证据"
            ]
            clarification_questions = []
        else:
            case_analysis = "根据您的描述，这是一个典型的法律问题。建议您参考相关法律规定，并根据具体情况采取适当的维权措施。"
            suggestions = [
                "收集和保存所有相关证据材料（合同、聊天记录、转账记录等）",
                "先尝试与对方协商解决",
                "协商不成可向劳动监察部门投诉或申请劳动仲裁",
                "必要时可咨询专业律师或寻求法律援助",
                "注意诉讼时效，及时采取法律行动"
            ]
            clarification_questions = []
        
        return {
            '问题评估': {
                '信息完整度': pre_analysis['completeness'],
                '需要澄清': pre_analysis['needs_clarification'],
                '澄清问题': clarification_questions
            },
            '案由分析': case_analysis,
            '核心争议点': ['需要补充更多信息才能准确判断'] if pre_analysis['needs_clarification'] else ['请参考相关法律规定'],
            '关键词': self._extract_keywords(question),
            '行动建议': suggestions,
            '风险提示': ['请提供完整信息以获得准确的法律建议'] if pre_analysis['needs_clarification'] else [],
            '特别说明': ''
        }
    
    def _call_spark_api(self, prompt):
        """调用讯飞星火API"""
        print(f"\n{'='*60}")
        print("准备调用讯飞星火API")
        print(f"{'='*60}")
        
        if not self.appid or not self.api_key or not self.api_secret:
            self.error = "API配置不完整"
            print(f"✗ {self.error}")
            return
        
        if self.appid == "your_app_id":
            self.error = "请填入真实的API密钥"
            print(f"✗ {self.error}")
            return
        
        self.answer = ""
        self.error = None
        
        try:
            print("创建WebSocket连接...")
            wsUrl = self._create_url()
            
            print("正在连接到讯飞服务器...")
            ws = websocket.WebSocketApp(
                wsUrl,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open
            )
            
            ws.prompt = prompt
            ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
            
            if self.answer:
                print(f"✓ 收到响应（长度: {len(self.answer)}）")
            else:
                if not self.error:
                    self.error = "API调用超时或无响应"
                print(f"✗ {self.error}")
            
        except Exception as e:
            self.error = f"API调用异常: {str(e)}"
            print(f"✗ {self.error}")
    
    def _create_url(self):
        """创建WebSocket URL"""
        url = urlparse(self.api_url)
        date = format_date_time(mktime(datetime.now().timetuple()))
        
        signature_origin = "host: " + url.netloc + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + url.path + " HTTP/1.1"
        
        signature_sha = hmac.new(
            self.api_secret.encode('utf-8'),
            signature_origin.encode('utf-8'),
            digestmod=hashlib.sha256
        ).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
        
        authorization_origin = 'api_key="' + self.api_key + '", '
        authorization_origin += 'algorithm="hmac-sha256", '
        authorization_origin += 'headers="host date request-line", '
        authorization_origin += 'signature="' + signature_sha_base64 + '"'
        
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        
        params = {
            "authorization": authorization,
            "date": date,
            "host": url.netloc
        }
        
        return self.api_url + "?" + urlencode(params)
    
    def _on_message(self, ws, message):
        """处理消息"""
        data = json.loads(message)
        code = data['header']['code']
        
        if code != 0:
            self.error = f"API错误: {code}, {data}"
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            self.answer += content
            
            if status == 2:
                ws.close()
    
    def _on_error(self, ws, error):
        """处理错误"""
        self.error = str(error)
        print(f"✗ WebSocket错误: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """关闭连接"""
        pass
    
    def _on_open(self, ws):
        """打开连接"""
        def run():
            data = {
                "header": {
                    "app_id": self.appid,
                    "uid": "user123"
                },
                "parameter": {
                    "chat": {
                        "domain": "4.0Ultra",
                        "temperature": 0.5,
                        "max_tokens": 2048
                    }
                },
                "payload": {
                    "message": {
                        "text": [
                            {"role": "user", "content": ws.prompt}
                        ]
                    }
                }
            }
            ws.send(json.dumps(data))
        
        thread.start_new_thread(run, ())
