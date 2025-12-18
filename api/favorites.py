"""
收藏列表 API
GET /api/favorites/[user_id] - 获取收藏
POST /api/favorites - 添加收藏
DELETE /api/favorites/[user_id]/[movie_id] - 删除收藏
"""
from flask import Flask, request, jsonify
from psycopg2.extras import RealDictCursor
import sys
import os
sys.path.append(os.path.dirname(__file__))
from _db import get_db

app = Flask(__name__)

def handler(request):
    """处理收藏列表请求"""
    try:
        path = request.path
        method = request.method
        
        if method == 'GET':
            # GET /api/favorites/[user_id]
            user_id = int(path.split('/')[-1])
            return get_favorites(user_id)
        
        elif method == 'POST':
            # POST /api/favorites
            return add_favorite(request)
        
        elif method == 'DELETE':
            # DELETE /api/favorites/[user_id]/[movie_id]
            parts = path.split('/')
            user_id = int(parts[-2])
            movie_id = int(parts[-1])
            return remove_favorite(user_id, movie_id)
        
        else:
            return jsonify({'success': False, 'message': 'Method not allowed'}), 405
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500

def get_favorites(user_id):
    """获取用户收藏列表"""
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
    
    return jsonify({
        'success': True,
        'favorites': favorites
    }), 200

def add_favorite(request):
    """添加到收藏列表"""
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('movie_id'):
        return jsonify({
            'success': False,
            'message': '请提供user_id和movie_id'
        }), 400
    
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
        return jsonify({
            'success': False,
            'message': '该电影已在收藏列表中'
        }), 400
    
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
    
    return jsonify({
        'success': True,
        'message': '已添加到收藏列表',
        'id': favorite_id
    }), 201

def remove_favorite(user_id, movie_id):
    """从收藏列表删除"""
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute(
        'DELETE FROM favorites WHERE user_id = %s AND movie_id = %s',
        (user_id, movie_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': '已从收藏列表中移除'
    }), 200

