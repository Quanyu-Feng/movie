from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# Supabase数据库连接信息
DATABASE_URL = "postgresql://postgres.jihfdpkcnuvkmarfkgoy:123456@aws-0-us-west-2.pooler.supabase.com:6543/postgres"

# 获取数据库连接
def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# ==================== 用户注册 ====================
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': '请提供用户名和密码'
        }), 400
    
    username = data['username'].strip()
    password = data['password'].strip()
    
    if len(username) < 3:
        return jsonify({
            'success': False,
            'message': '用户名至少需要3个字符'
        }), 400
    
    if len(password) < 6:
        return jsonify({
            'success': False,
            'message': '密码至少需要6个字符'
        }), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 检查用户名是否已存在
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            return jsonify({
                'success': False,
                'message': '用户名已存在'
            }), 400
        
        # 加密密码并插入新用户
        hashed_password = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id',
            (username, hashed_password)
        )
        user_id = cursor.fetchone()['id']
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': '注册成功',
            'user_id': user_id,
            'username': username
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==================== 用户登录 ====================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': '请提供用户名和密码'
        }), 400
    
    username = data['username'].strip()
    password = data['password'].strip()
    
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 查找用户
        cursor.execute(
            'SELECT id, username, password FROM users WHERE username = %s',
            (username,)
        )
        user = cursor.fetchone()
        
        if not user:
            return jsonify({
                'success': False,
                'message': '用户不存在'
            }), 404
        
        # 验证密码
        if not check_password_hash(user['password'], password):
            return jsonify({
                'success': False,
                'message': '密码错误'
            }), 401
        
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
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==================== 健康检查 ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 检查各表的数据量
        cursor.execute('SELECT COUNT(*) FROM users')
        users_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) FROM favorites')
        favorites_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) FROM history')
        history_count = cursor.fetchone()['count']
        
        return jsonify({
            'status': 'healthy',
            'database': 'Supabase PostgreSQL',
            'tables': {
                'users': users_count,
                'favorites': favorites_count,
                'history': history_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==================== History API ====================

# 获取用户的观看历史
@app.route('/api/history/<int:user_id>', methods=['GET'])
def get_history(user_id):
    try:
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
        
        # 按观看时间重新排序（因为DISTINCT ON改变了排序）
        history_sorted = sorted(history, key=lambda x: x['watched_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'history': history_sorted
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 添加观看历史记录
@app.route('/api/history', methods=['POST'])
def add_to_history():
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('movie_id'):
        return jsonify({
            'success': False,
            'message': '请提供user_id和movie_id'
        }), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 插入新记录（允许重复，每次点击都记录）
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
        
        return jsonify({
            'success': True,
            'message': '已添加到观看历史',
            'id': history_id
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 清除用户观看历史
@app.route('/api/history/<int:user_id>', methods=['DELETE'])
def clear_history(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            'DELETE FROM history WHERE user_id = %s',
            (user_id,)
        )
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': '已清除观看历史'
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==================== Favorites API ====================

# 获取用户的favorites
@app.route('/api/favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute('''
            SELECT id, movie_id, movie_title, poster_path, release_date, vote_average, added_at
            FROM favorites 
            WHERE user_id = %s 
            ORDER BY added_at DESC
        ''', (user_id,))
        
        favorites = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'favorites': favorites
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 添加电影到favorites
@app.route('/api/favorites', methods=['POST'])
def add_to_favorites():
    data = request.get_json()
    
    if not data or not data.get('user_id') or not data.get('movie_id'):
        return jsonify({
            'success': False,
            'message': '请提供user_id和movie_id'
        }), 400
    
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # 检查是否已存在
        cursor.execute(
            'SELECT id FROM favorites WHERE user_id = %s AND movie_id = %s',
            (data['user_id'], data['movie_id'])
        )
        
        if cursor.fetchone():
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
        
        return jsonify({
            'success': True,
            'message': '已添加到收藏列表',
            'id': favorite_id
        }), 201
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# 从favorites中删除电影
@app.route('/api/favorites/<int:user_id>/<int:movie_id>', methods=['DELETE'])
def remove_from_favorites(user_id, movie_id):
    try:
        conn = get_db()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(
            'DELETE FROM favorites WHERE user_id = %s AND movie_id = %s',
            (user_id, movie_id)
        )
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': '已从收藏列表中移除'
        }), 200
        
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({
            'success': False,
            'message': f'错误: {str(e)}'
        }), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# ==================== 根路由 ====================
@app.route('/')
def index():
    return jsonify({
        'message': '电影系统API',
        'version': '3.0',
        'database': 'Supabase PostgreSQL',
        'endpoints': {
            'register': 'POST /api/register',
            'login': 'POST /api/login',
            'health': 'GET /api/health',
            'get_history': 'GET /api/history/<user_id>',
            'add_to_history': 'POST /api/history',
            'clear_history': 'DELETE /api/history/<user_id>',
            'get_favorites': 'GET /api/favorites/<user_id>',
            'add_to_favorites': 'POST /api/favorites',
            'remove_from_favorites': 'DELETE /api/favorites/<user_id>/<movie_id>'
        }
    })

if __name__ == '__main__':
    print('🎬 电影系统后端服务器启动中...')
    print('📁 数据库: Supabase PostgreSQL')
    print('🌐 服务器地址: http://localhost:5000')
    print('📡 API文档: http://localhost:5000/')
    print('=' * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

