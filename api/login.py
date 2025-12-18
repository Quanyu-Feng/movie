"""
用户登录 API
POST /api/login
"""
from http.server import BaseHTTPRequestHandler
from werkzeug.security import check_password_hash
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
        """处理用户登录请求"""
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            if not data.get('username') or not data.get('password'):
                self.send_json_response({
                    'success': False,
                    'message': 'Please provide both username and password.'
                }, 400)
                return
            
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
                self.send_json_response({
                    'success': False,
                    'message': 'Sorry, that username is not associated with an account. Would you like to create a new account?'
                }, 404)
                return
            
            # 验证密码
            if not check_password_hash(user['password'], password):
                cursor.close()
                conn.close()
                self.send_json_response({
                    'success': False,
                    'message': 'Incorrect password. Please try again.'
                }, 401)
                return
            
            cursor.close()
            conn.close()
            
            self.send_json_response({
                'success': True,
                'message': f"Welcome back, {username}!",
                'user_id': user['id'],
                'username': user['username']
            }, 200)
            
        except Exception as e:
            self.send_json_response({
                'success': False,
                'message': f'Error: {str(e)}'
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
