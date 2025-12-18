"""
观看历史 API
GET /api/history/[user_id] - 获取历史
POST /api/history - 添加历史
DELETE /api/history/[user_id] - 清除历史
"""
from http.server import BaseHTTPRequestHandler
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
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """获取观看历史"""
        try:
            # 从路径中提取 user_id
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) < 3:
                self.send_json_response({'success': False, 'message': 'user_id does not exist.'}, 400)
                return
            
            user_id = int(path_parts[-1])
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 使用DISTINCT ON来只获取每个video_key的最新记录
            cursor.execute('''
                SELECT DISTINCT ON (video_key) 
                       id, movie_id, movie_title, poster_path, release_date, vote_average, 
                       video_key, video_title, watched_at
                FROM history 
                WHERE user_id = %s 
                ORDER BY video_key, watched_at DESC
                LIMIT 100
            ''', (user_id,))
            
            history = cursor.fetchall()
            cursor.close()
            conn.close()
            
            # 按观看时间重新排序
            history_sorted = sorted(history, key=lambda x: x['watched_at'], reverse=True)
            
            self.send_json_response({'success': True, 'history': history_sorted}, 200)
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': f'Error: {str(e)}'}, 500)
    
    def do_POST(self):
        """添加观看历史"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body) if body else {}
            
            if not data.get('user_id') or not data.get('movie_id'):
                self.send_json_response({'success': False, 'message': 'Please provide both user_id and movie_id'}, 400)
                return
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 插入新记录
            cursor.execute('''
                INSERT INTO history (user_id, movie_id, movie_title, poster_path, release_date, vote_average, video_key, video_title)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            ''', (
                data['user_id'],
                data['movie_id'],
                data.get('movie_title'),
                data.get('poster_path'),
                data.get('release_date'),
                data.get('vote_average'),
                data.get('video_key'),
                data.get('video_title')
            ))
            
            history_id = cursor.fetchone()['id']
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_json_response({'success': True, 'message': 'Added to watch history.', 'id': history_id}, 201)
            
        except Exception as e:
            self.send_json_response({'success': False, 'message': f'Error: {str(e)}'}, 500)
    
    def do_DELETE(self):
        """清除观看历史"""
        try:
            # 从路径中提取 user_id
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) < 3:
                self.send_json_response({'success': False, 'message': 'Please provide user_id.'}, 400)
                return
            
            user_id = int(path_parts[-1])
            
            conn = get_db()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute('DELETE FROM history WHERE user_id = %s', (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            self.send_json_response({'success': True, 'message': 'Watch history cleared.'}, 200)
            
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
