"""
用户登录 API
POST /api/login
"""
from werkzeug.security import check_password_hash
from psycopg2.extras import RealDictCursor
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from _db import get_db, json_response

def handler(request):
    """处理用户登录请求"""
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
            return json_response(json.dumps({
                'success': False,
                'message': '用户不存在'
            }), 404)
        
        # 验证密码
        if not check_password_hash(user['password'], password):
            cursor.close()
            conn.close()
            return json_response(json.dumps({
                'success': False,
                'message': '密码错误'
            }), 401)
        
        cursor.close()
        conn.close()
        
        return json_response(json.dumps({
            'success': True,
            'message': '登录成功',
            'user_id': user['id'],
            'username': user['username']
        }), 200)
        
    except Exception as e:
        return json_response(json.dumps({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500)

