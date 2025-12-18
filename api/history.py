"""
观看历史 API
GET /api/history/[user_id] - 获取历史
POST /api/history - 添加历史
DELETE /api/history/[user_id] - 清除历史
"""
from psycopg2.extras import RealDictCursor
import json
import sys
import os
sys.path.append(os.path.dirname(__file__))
from _db import get_db, json_response

def handler(request):
    """处理历史记录请求"""
    # 处理 CORS 预检请求
    if request.method == 'OPTIONS':
        return json_response('', 200)
    
    try:
        # 解析路径获取user_id
        path = request.path if hasattr(request, 'path') else request.get('path', '')
        method = request.method if hasattr(request, 'method') else request.get('method', 'GET')
        
        if method == 'GET':
            # GET /api/history/[user_id]
            user_id = int(path.split('/')[-1])
            return get_history(user_id)
        
        elif method == 'POST':
            # POST /api/history
            return add_history(request)
        
        elif method == 'DELETE':
            # DELETE /api/history/[user_id]
            user_id = int(path.split('/')[-1])
            return clear_history(user_id)
        
        else:
            return json_response(json.dumps({'success': False, 'message': 'Method not allowed'}), 405)
            
    except Exception as e:
        return json_response(json.dumps({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500)

def get_history(user_id):
    """获取用户观看历史"""
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
    
    return json_response(json.dumps({
        'success': True,
        'history': history_sorted
    }, default=str), 200)

def add_history(request):
    """添加观看历史"""
    # 解析请求体
    if hasattr(request, 'get_json'):
        data = request.get_json()
    else:
        body = request.body if hasattr(request, 'body') else request.get('body', '{}')
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        data = json.loads(body) if isinstance(body, str) else body
    
    if not data or not data.get('user_id') or not data.get('movie_id'):
        return json_response(json.dumps({
            'success': False,
            'message': '请提供user_id和movie_id'
        }), 400)
    
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
    
    return json_response(json.dumps({
        'success': True,
        'message': '已添加到观看历史',
        'id': history_id
    }), 201)

def clear_history(user_id):
    """清除用户观看历史"""
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute('DELETE FROM history WHERE user_id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return json_response(json.dumps({
        'success': True,
        'message': '已清除观看历史'
    }), 200)

