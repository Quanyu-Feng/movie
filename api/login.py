"""
用户登录 API
POST /api/login
"""
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from psycopg2.extras import RealDictCursor
import sys
import os
sys.path.append(os.path.dirname(__file__))
from _db import get_db

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def handler(request):
    """处理用户登录请求"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': '请提供用户名和密码'
            }), 400
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 查找用户
        cursor.execute(
            'SELECT id, username, password FROM users WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        
        if not user:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 404
        
        # 验证密码
        if not check_password_hash(user['password'], password):
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': '密码错误'
            }), 401
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': '登录成功',
            'user_id': user['id'],
            'username': user['username']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500

