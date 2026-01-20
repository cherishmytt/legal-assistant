# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from services.report_generator import ReportGenerator
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# 配置CORS - 允许所有来源
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 初始化报告生成器
report_generator = ReportGenerator()

@app.route('/')
def index():
    """首页"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """静态文件"""
    return send_from_directory(app.static_folder, path)

@app.route('/api/analyze', methods=['POST', 'OPTIONS'])
def analyze():
    """分析法律问题"""
    # 处理OPTIONS预检请求
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({
                'error': '问题不能为空'
            }), 400
        
        print(f"\n收到问题: {question}")
        
        # 生成报告
        report = report_generator.generate_report(question)
        
        print("报告生成成功")
        
        response = jsonify(report)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
        
        response = jsonify({
            'error': f'服务器错误: {str(e)}'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 500

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'message': '服务运行正常'
    })

if __name__ == '__main__':
    print("="*60)
    print("智能法律咨询助手 - 后端服务")
    print("="*60)
    print("服务地址: http://localhost:5000")
    print("API地址: http://localhost:5000/api/analyze")
    print("="*60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
