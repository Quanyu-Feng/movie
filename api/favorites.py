"""
收藏列表 API
GET /api/favorites/[user_id] - 获取收藏
POST /api/favorites - 添加收藏
DELETE /api/favorites/[user_id]/[movie_id] - 删除收藏
"""
from http.server import BaseHTTPRequestHandler
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse, parse_qs
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """获取收藏列表"""
        try:
            # 从路径中提取 user_id
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) < 3:
                self.send_json_response({'success': False, 'message': 'Please provide user_id.'}, 400)
                return
            
            user_id = int(path_parts[-1])
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute('''
                SELECT id, movie_id, movie_title, poster_path, release_date, vote_average, added_at
                FROM favorites 
                WHERE user_id = %s 
                ORDER BY added_at DESC
            ''', (user_id,))
            
            favorites = cursor.fetchall()
            cursor.close()
            conn.close()
            
            self.send_json_response({'success': True, 'favorites': favorites}, 200)
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': f'Error: {str(e)}'}, 500)
    
    def do_POST(self):
        """添加收藏"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            if not data.get('user_id') or not data.get('movie_id'):
                self.send_json_response({'success': False, 'message': 'Please provide both user_id and movie_id.'}, 400)
                return
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 检查是否已存在
            cursor.execute(
                'SELECT id FROM favorites WHERE user_id = %s AND movie_id = %s',
                (data['user_id'], data['movie_id'])
            )
            
            if cursor.fetchone():
                cursor.close()
                conn.close()
                self.send_json_response({'success': False, 'message': 'The movie is already in the favorites list!'}, 400)
                return
            
            # 插入新记录
            cursor.execute('''
                INSERT INTO favorites (user_id, movie_id, movie_title, poster_path, release_date, vote_average)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                data['user_id'],
                data['movie_id'],
                data.get('movie_title'),
                data.get('poster_path'),
                data.get('release_date'),
                data.get('vote_average')
            ))
            
            favorite_id = cursor.fetchone()['id']
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_json_response({'success': True, 'message': 'Added to favorites successfully.', 'id': favorite_id}, 201)
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': f'Error: {str(e)}'}, 500)
    
    def do_DELETE(self):
        """删除收藏"""
        try:
            # 从路径中提取 user_id 和 movie_id
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) < 4:
                self.send_json_response({'success': False, 'message': 'Please provide user_id and movie_id.'}, 400)
                return
            
            user_id = int(path_parts[-2])
            movie_id = int(path_parts[-1])
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(
                'DELETE FROM favorites WHERE user_id = %s AND movie_id = %s',
                (user_id, movie_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_json_response({'success': True, 'message': 'Removed from favorite list successfully.'}, 200)
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': f'Error: {str(e)}'}, 500)
    
    def send_json_response(self, data, status=200):
        """发送 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        # 处理日期时间对象
        json_str = json.dumps(data, default=str)
        self.wfile.write(json_str.encode('utf-8'))
