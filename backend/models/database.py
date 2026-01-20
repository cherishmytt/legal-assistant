import sqlite3
from datetime import datetime
import json

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 法律知识表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS legal_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                keywords TEXT,
                law_name TEXT,
                article_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 用户查询表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_query (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                question TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 生成报告表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generated_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER,
                raw_ai_response TEXT,
                structured_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (query_id) REFERENCES user_query(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # 插入示例法律知识
        self.insert_sample_knowledge()
    
    def insert_sample_knowledge(self):
        """插入示例法律知识"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 检查是否已有数据
        cursor.execute("SELECT COUNT(*) as count FROM legal_knowledge")
        if cursor.fetchone()['count'] > 0:
            conn.close()
            return
        
        sample_data = [
            {
                'category': '劳动纠纷',
                'title': '拖欠工资的法律规定',
                'content': '用人单位应当按照劳动合同约定和国家规定，向劳动者及时足额支付劳动报酬。用人单位拖欠或者未足额支付劳动报酬的，劳动者可以依法向当地人民法院申请支付令。',
                'keywords': '拖欠工资,劳动报酬,支付令',
                'law_name': '劳动合同法',
                'article_number': '第三十条、第八十五条'
            },
            {
                'category': '劳动纠纷',
                'title': '劳动仲裁时效',
                'content': '劳动争议申请仲裁的时效期间为一年。仲裁时效期间从当事人知道或者应当知道其权利被侵害之日起计算。',
                'keywords': '劳动仲裁,时效,一年',
                'law_name': '劳动争议调解仲裁法',
                'article_number': '第二十七条'
            },
            {
                'category': '交通事故',
                'title': '交通事故责任认定',
                'content': '公安机关交通管理部门应当根据当事人的行为对发生道路交通事故所起的作用以及过错的严重程度，确定当事人的责任。',
                'keywords': '交通事故,责任认定,过错',
                'law_name': '道路交通安全法',
                'article_number': '第七十三条'
            },
            {
                'category': '婚姻家庭',
                'title': '离婚财产分割原则',
                'content': '离婚时，夫妻的共同财产由双方协议处理；协议不成的，由人民法院根据财产的具体情况，按照照顾子女、女方和无过错方权益的原则判决。',
                'keywords': '离婚,财产分割,共同财产',
                'law_name': '民法典',
                'article_number': '第一千零八十七条'
            },
            {
                'category': '合同纠纷',
                'title': '合同违约责任',
                'content': '当事人一方不履行合同义务或者履行合同义务不符合约定的，应当承担继续履行、采取补救措施或者赔偿损失等违约责任。',
                'keywords': '违约,赔偿,合同',
                'law_name': '民法典',
                'article_number': '第五百七十七条'
            }
        ]
        
        for data in sample_data:
            cursor.execute('''
                INSERT INTO legal_knowledge 
                (category, title, content, keywords, law_name, article_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['category'], data['title'], data['content'], 
                  data['keywords'], data['law_name'], data['article_number']))
        
        conn.commit()
        conn.close()
    
    def save_query(self, question, session_id=None):
        """保存用户查询"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_query (question, session_id) VALUES (?, ?)",
            (question, session_id)
        )
        query_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return query_id
    
    def save_report(self, query_id, raw_response, structured_data):
        """保存生成的报告"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO generated_report (query_id, raw_ai_response, structured_data)
            VALUES (?, ?, ?)
        ''', (query_id, raw_response, json.dumps(structured_data, ensure_ascii=False)))
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return report_id
    
    def search_knowledge(self, keywords):
        """根据关键词搜索法律知识"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        results = []
        for keyword in keywords:
            cursor.execute('''
                SELECT * FROM legal_knowledge 
                WHERE keywords LIKE ? OR title LIKE ? OR content LIKE ?
                LIMIT 5
            ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
            results.extend([dict(row) for row in cursor.fetchall()])
        
        conn.close()
        
        # 去重
        unique_results = []
        seen_ids = set()
        for result in results:
            if result['id'] not in seen_ids:
                unique_results.append(result)
                seen_ids.add(result['id'])
        
        return unique_results[:5]
    
    def get_query_history(self, limit=10):
        """获取查询历史"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, question, created_at 
            FROM user_query 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
