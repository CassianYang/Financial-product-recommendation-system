# create_database.py
import sqlite3
import pandas as pd

# 连接到数据库文件（如果不存在则会自动创建）
conn = sqlite3.connect('./data/financial_data.db')
c = conn.cursor()

# 1. 创建用户表 (users)
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        age INTEGER,
        occupation TEXT,
        income_level TEXT, -- e.g., 'low', 'medium', 'high'
        risk_tolerance TEXT -- e.g., 'low', 'medium', 'high'
    )
''')

# 2. 创建金融产品表 (products)
c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        product_name TEXT,
        product_type TEXT, -- e.g., '基金', '保险', '股票'
        risk_level TEXT,
        expected_return REAL, -- 预期收益率
        min_investment INTEGER -- 最低投资额
    )
''')

# 3. 创建用户行为表 (user_behavior) - 用于协同过滤和关联规则
c.execute('''
    CREATE TABLE IF NOT EXISTS user_behavior (
        user_id INTEGER,
        product_id INTEGER,
        behavior_type TEXT, -- e.g., 'view', 'purchase'
        rating INTEGER, -- 评分 1-5
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
''')

# --- 插入模拟数据 ---

# 插入用户数据
users_data = [
    (1, 25, '工程师', 'high', 'medium'),
    (2, 35, '教师', 'medium', 'low'),
    (3, 45, '医生', 'high', 'high'),
    (4, 28, '自由职业', 'low', 'medium'),
    (5, 52, '企业家', 'high', 'high'),
]
c.executemany('INSERT INTO users VALUES (?,?,?,?,?)', users_data)

# 插入产品数据
products_data = [
    (101, '稳健货币基金', '基金', 'low', 3.5, 1000),
    (102, '成长型股票基金', '基金', 'high', 12.0, 5000),
    (103, '人寿保险计划', '保险', 'low', 2.5, 2000),
    (104, '高收益债券', '债券', 'medium', 6.0, 10000),
    (105, '指数ETF', '基金', 'medium', 8.0, 1000),
]
c.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', products_data)

# 插入用户行为数据（浏览、购买、评分）
behavior_data = [
    (1, 101, 'view', 5),
    (1, 102, 'purchase', 4),
    (2, 101, 'purchase', 5),
    (2, 103, 'view', 3),
    (3, 102, 'purchase', 5),
    (3, 104, 'purchase', 4),
    (4, 101, 'purchase', 5),
    (4, 105, 'view', 4),
    (5, 104, 'purchase', 5),
    (5, 102, 'purchase', 5),
]
c.executemany('INSERT INTO user_behavior (user_id, product_id, behavior_type, rating) VALUES (?,?,?,?)', behavior_data)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("数据库 financial_data.db 已成功创建，并填入模拟数据！")
print("请将该文件从 data/ 文件夹分享给所有组员。")