"""
初始化Supabase数据库表
运行此脚本来创建所有必要的表
"""

import psycopg2
from psycopg2 import sql

# Supabase连接信息
DATABASE_URL = "postgresql://postgres.jihfdpkcnuvkmarfkgoy:123456@aws-0-us-west-2.pooler.supabase.com:6543/postgres"

def init_database():
    """初始化数据库表"""
    try:
        # 连接到数据库
        print("正在连接到Supabase...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 读取SQL文件
        print("正在读取SQL脚本...")
        with open('init_database.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 执行SQL脚本
        print("正在创建数据库表...")
        cursor.execute(sql_script)
        conn.commit()
        
        print("✅ 数据库初始化成功！")
        
        # 显示创建的表
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print("\n📋 已创建的表:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        raise

if __name__ == '__main__':
    init_database()

