-- myMovie Super Database Schema for Supabase (PostgreSQL)
-- 创建数据库表

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 收藏列表表
CREATE TABLE IF NOT EXISTS favorites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    movie_title VARCHAR(255),
    poster_path VARCHAR(255),
    release_date VARCHAR(20),
    vote_average DECIMAL(3, 1),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, movie_id)
);

-- 观看历史表
CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    movie_title VARCHAR(255),
    poster_path VARCHAR(255),
    release_date VARCHAR(20),
    vote_average DECIMAL(3, 1),
    video_key VARCHAR(255),
    video_title VARCHAR(255),
    watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_movie_id ON favorites(movie_id);
CREATE INDEX IF NOT EXISTS idx_history_user_id ON history(user_id);
CREATE INDEX IF NOT EXISTS idx_history_movie_id ON history(movie_id);
CREATE INDEX IF NOT EXISTS idx_history_watched_at ON history(watched_at DESC);

-- 插入测试用户（可选）
-- 密码是 'test123' 的哈希值，使用 werkzeug.security.generate_password_hash 生成
-- INSERT INTO users (username, password) VALUES 
-- ('test', 'scrypt:32768:8:1$...');  -- 需要在Python中生成实际的哈希值

