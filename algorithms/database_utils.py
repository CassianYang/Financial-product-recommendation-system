import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_path='./data/financial_data.db'):
        self.db_path = db_path
    
    def get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_path)
    
    def get_all_users(self):
        """获取所有用户数据"""
        conn = self.get_connection()
        users_df = pd.read_sql_query("SELECT * FROM users", conn)
        conn.close()
        return users_df
    
    def get_all_products(self):
        """获取所有产品数据"""
        conn = self.get_connection()
        products_df = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
        return products_df
    
    def get_user_behavior(self):
        """获取用户行为数据"""
        conn = self.get_connection()
        behavior_df = pd.read_sql_query("SELECT * FROM user_behavior", conn)
        conn.close()
        return behavior_df
    
    def get_user_by_id(self, user_id):
        """根据ID获取特定用户"""
        conn = self.get_connection()
        user_df = pd.read_sql_query(f"SELECT * FROM users WHERE user_id = {user_id}", conn)
        conn.close()
        return user_df
    
    def get_product_by_id(self, product_id):
        """根据ID获取特定产品"""
        conn = self.get_connection()
        product_df = pd.read_sql_query(f"SELECT * FROM products WHERE product_id = {product_id}", conn)
        conn.close()
        return product_df

# 测试数据库连接
if __name__ == "__main__":
    db = DatabaseManager()
    print("用户数据样例:")
    print(db.get_all_users().head())
    print("\n产品数据样例:")
    print(db.get_all_products().head())