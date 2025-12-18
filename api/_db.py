"""
共享数据库连接模块
"""
import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Supabase数据库连接信息
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres.jihfdpkcnuvkmarfkgoy:123456@aws-0-us-west-2.pooler.supabase.com:6543/postgres'
)

def get_db():
    """获取数据库连接"""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def json_response(data, status=200):
    """创建JSON响应"""
    return {
        'statusCode': status,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS'
        },
        'body': data
    }

