"""
用户注册 API
POST /api/register
"""
from http.server import BaseHTTPRequestHandler
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from _db import get_db

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """处理用户注册请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            if not data.get('username') or not data.get('password'):
                self.send_json_response({
                    'success': False,
                    'message': '请提供用户名和密码'
                }, 400)
                return
            
            username = data['username'].strip()
            password = data['password'].strip()
            
            if len(username) < 3:
                self.send_json_response({
                    'success': False,
                    'message': '用户名至少需要3个字符'
                }, 400)
                return
            
            if len(password) < 6:
                self.send_json_response({
                    'success': False,
                    'message': '密码至少需要6个字符'
                }, 400)
                return
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 检查用户名是否已存在
            cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                self.send_json_response({
                    'success': False,
                    'message': '用户名已存在'
                }, 400)
                return
            
            # 加密密码并插入新用户
            hashed_password = generate_password_hash(password)
            cursor.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id',
                (username, hashed_password)
            )
            user_id = cursor.fetchone()['id']
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_json_response({
                'success': True,
                'message': '注册成功',
                'user_id': user_id,
                'username': username
            }, 201)
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'message': f'错误: {str(e)}'
            }, 500)
    
    def send_json_response(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
