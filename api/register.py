"""
用户注册 API
POST /api/register
"""
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from _db import get_db, json_response

def handler(request):
    """处理用户注册请求"""
    # 处理 CORS 预检请求
    if request.method == 'OPTIONS':
        return json_response('', 200)
    
    try:
        # 解析请求体
        if hasattr(request, 'get_json'):
            data = request.get_json()
        else:
            body = request.body if hasattr(request, 'body') else request.get('body', '{}')
            if isinstance(body, bytes):
                body = body.decode('utf-8')
            data = json.loads(body) if isinstance(body, str) else body
        
        if not data or not data.get('username') or not data.get('password'):
            return json_response(json.dumps({
                'success': False,
                'message': '请提供用户名和密码'
            }), 400)
        
        username = data['username'].strip()
        password = data['password'].strip()
        
        if len(username) < 3:
            return json_response(json.dumps({
                'success': False,
                'message': '用户名至少需要3个字符'
            }), 400)
        
        if len(password) < 6:
            return json_response(json.dumps({
                'success': False,
                'message': '密码至少需要6个字符'
            }), 400)
        
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 检查用户名是否已存在
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return json_response(json.dumps({
                'success': False,
                'message': '用户名已存在'
            }), 400)
        
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
        
        return json_response(json.dumps({
            'success': True,
            'message': '注册成功',
            'user_id': user_id,
            'username': username
        }), 201)
        
    except Exception as e:
        return json_response(json.dumps({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500)

