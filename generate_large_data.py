import sqlite3
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# 初始化Faker生成器
fake = Faker('zh_CN')

class DataGenerator:
    def __init__(self, db_path='data/financial_data.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.fake = Faker('zh_CN')
        
    def clear_existing_data(self):
        """清空现有数据"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM user_behavior")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM users")
        self.conn.commit()
        print("已清空现有数据")
    
    def generate_users(self, num_users=200):
        """生成用户数据"""
        occupations = ['工程师', '教师', '医生', '公务员', '企业家', '自由职业', '学生', '退休人员', '经理', '销售']
        income_levels = ['low', 'medium', 'high']
        risk_tolerances = ['low', 'medium', 'high']
        
        users_data = []
        for i in range(1, num_users + 1):
            age = random.randint(20, 65)
            occupation = random.choice(occupations)
            
            # 根据年龄和职业设置收入水平
            if age < 25:
                income = random.choices(income_levels, weights=[0.6, 0.3, 0.1])[0]
            elif age < 40:
                income = random.choices(income_levels, weights=[0.2, 0.5, 0.3])[0]
            else:
                income = random.choices(income_levels, weights=[0.1, 0.4, 0.5])[0]
            
            # 根据年龄和收入设置风险承受能力
            if age < 30 and income == 'high':
                risk = random.choices(risk_tolerances, weights=[0.1, 0.3, 0.6])[0]
            elif age > 50:
                risk = random.choices(risk_tolerances, weights=[0.6, 0.3, 0.1])[0]
            else:
                risk = random.choices(risk_tolerances, weights=[0.3, 0.4, 0.3])[0]
            
            users_data.append((i, age, occupation, income, risk))
        
        # 插入数据库
        cursor = self.conn.cursor()
        cursor.executemany('''
            INSERT INTO users (user_id, age, occupation, income_level, risk_tolerance) 
            VALUES (?, ?, ?, ?, ?)
        ''', users_data)
        self.conn.commit()
        print(f"已生成 {num_users} 个用户")
        
        return users_data
    
    def generate_products(self, num_products=50):
        """生成金融产品数据"""
        product_types = ['货币基金', '债券基金', '股票基金', '混合基金', '指数基金', 
                        '保险产品', '银行理财', '信托产品', '私募基金', '贵金属投资']
        
        risk_mapping = {
            '货币基金': 'low',
            '债券基金': 'low',
            '保险产品': 'low',
            '银行理财': 'low',
            '混合基金': 'medium', 
            '指数基金': 'medium',
            '信托产品': 'medium',
            '股票基金': 'high',
            '私募基金': 'high',
            '贵金属投资': 'high'
        }
        
        return_mapping = {
            'low': (1.5, 4.0),
            'medium': (4.0, 8.0),
            'high': (7.0, 15.0)
        }
        
        investment_mapping = {
            'low': (100, 5000),
            'medium': (1000, 20000),
            'high': (5000, 100000)
        }
        
        products_data = []
        for i in range(1, num_products + 1):
            product_type = random.choice(product_types)
            risk_level = risk_mapping[product_type]
            
            # 根据风险等级设置预期收益率范围
            min_return, max_return = return_mapping[risk_level]
            expected_return = round(random.uniform(min_return, max_return), 2)
            
            # 根据风险等级设置最低投资额
            min_invest, max_invest = investment_mapping[risk_level]
            min_investment = random.randint(min_invest, max_invest)
            
            # 生成产品名称
            if product_type == '货币基金':
                name = f"稳健货币基金{i}"
            elif product_type == '债券基金':
                name = f"安心债券基金{i}"
            elif product_type == '股票基金':
                name = f"成长股票基金{i}"
            elif product_type == '混合基金':
                name = f"平衡混合基金{i}"
            elif product_type == '指数基金':
                name = f"指数ETF基金{i}"
            elif product_type == '保险产品':
                name = f"综合保险计划{i}"
            elif product_type == '银行理财':
                name = f"银行理财产品{i}"
            elif product_type == '信托产品':
                name = f"信托投资计划{i}"
            elif product_type == '私募基金':
                name = f"私募股权基金{i}"
            else:
                name = f"贵金属投资{i}"
            
            products_data.append((i, name, product_type, risk_level, expected_return, min_investment))
        
        # 插入数据库
        cursor = self.conn.cursor()
        cursor.executemany('''
            INSERT INTO products (product_id, product_name, product_type, risk_level, expected_return, min_investment) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', products_data)
        self.conn.commit()
        print(f"已生成 {num_products} 个金融产品")
        
        return products_data
    
    def generate_user_behavior(self, num_users=200, num_products=50, min_actions_per_user=5, max_actions_per_user=30):
        """生成用户行为数据"""
        behavior_types = ['view', 'purchase']
        
        behavior_data = []
        
        for user_id in range(1, num_users + 1):
            # 每个用户的行为数量
            num_actions = random.randint(min_actions_per_user, max_actions_per_user)
            
            # 用户可能接触的产品ID列表（去重）
            user_product_ids = random.sample(range(1, num_products + 1), 
                                           min(num_actions, num_products))
            
            purchased_products = set()
            
            for product_id in user_product_ids:
                # 决定行为类型：浏览或购买
                # 如果产品已经被购买过，只能是浏览
                if product_id in purchased_products:
                    behavior_type = 'view'
                else:
                    behavior_type = random.choices(behavior_types, weights=[0.6, 0.4])[0]
                    if behavior_type == 'purchase':
                        purchased_products.add(product_id)
                
                # 生成评分（购买的产品更可能获得高评分）
                if behavior_type == 'purchase':
                    rating = random.choices([3, 4, 5], weights=[0.2, 0.3, 0.5])[0]
                else:
                    rating = random.choices([1, 2, 3, 4, 5], weights=[0.1, 0.2, 0.4, 0.2, 0.1])[0]
                
                # 生成随机时间戳（最近90天内）
                days_ago = random.randint(0, 90)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
                
                behavior_data.append((user_id, product_id, behavior_type, rating, timestamp))
        
        # 插入数据库
        cursor = self.conn.cursor()
        cursor.executemany('''
            INSERT INTO user_behavior (user_id, product_id, behavior_type, rating, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        ''', behavior_data)
        self.conn.commit()
        print(f"已生成用户行为数据，共 {len(behavior_data)} 条记录")
        
        return behavior_data
    
    def generate_realistic_behavior_patterns(self, num_users=200, num_products=50):
        """生成更真实的行为模式"""
        print("生成真实用户行为模式...")
        
        # 获取用户和产品数据
        users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
        products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
        
        behavior_data = []
        
        for user_idx, user in users_df.iterrows():
            user_id = user['user_id']
            user_risk = user['risk_tolerance']
            user_income = user['income_level']
            
            # 根据用户特征决定偏好
            if user_risk == 'low':
                preferred_products = products_df[products_df['risk_level'] == 'low']
                purchase_prob = 0.3  # 低风险用户购买概率较低
            elif user_risk == 'high':
                preferred_products = products_df[products_df['risk_level'].isin(['medium', 'high'])]
                purchase_prob = 0.6  # 高风险用户购买概率较高
            else:  # medium
                preferred_products = products_df[products_df['risk_level'].isin(['low', 'medium'])]
                purchase_prob = 0.4
            
            # 根据收入调整购买概率
            if user_income == 'high':
                purchase_prob += 0.2
            elif user_income == 'low':
                purchase_prob -= 0.1
            
            # 生成浏览和购买行为
            num_views = random.randint(10, 25)
            
            # 优先浏览偏好产品
            preferred_product_ids = preferred_products['product_id'].tolist()
            other_product_ids = products_df[~products_df['product_id'].isin(preferred_product_ids)]['product_id'].tolist()
            
            # 70%的浏览在偏好产品中，30%在其他产品中
            num_preferred_views = int(num_views * 0.7)
            num_other_views = num_views - num_preferred_views
            
            viewed_products = (random.sample(preferred_product_ids, min(num_preferred_views, len(preferred_product_ids))) +
                             random.sample(other_product_ids, min(num_other_views, len(other_product_ids))))
            
            purchased_products = set()
            
            for product_id in viewed_products:
                # 决定是否购买
                product = products_df[products_df['product_id'] == product_id].iloc[0]
                
                # 调整购买概率：偏好产品购买概率更高
                adjusted_purchase_prob = purchase_prob
                if product_id in preferred_product_ids:
                    adjusted_purchase_prob += 0.2
                
                if random.random() < adjusted_purchase_prob and product_id not in purchased_products:
                    behavior_type = 'purchase'
                    purchased_products.add(product_id)
                    # 购买的产品评分更高
                    rating = random.choices([4, 5], weights=[0.3, 0.7])[0]
                else:
                    behavior_type = 'view'
                    rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.15, 0.4, 0.3, 0.1])[0]
                
                # 生成时间戳
                days_ago = random.randint(0, 90)
                timestamp = datetime.now() - timedelta(days=days_ago)
                
                behavior_data.append((user_id, product_id, behavior_type, rating, timestamp))
        
        # 插入数据库
        cursor = self.conn.cursor()
        cursor.executemany('''
            INSERT INTO user_behavior (user_id, product_id, behavior_type, rating, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        ''', behavior_data)
        self.conn.commit()
        print(f"已生成真实行为模式数据，共 {len(behavior_data)} 条记录")
        
        return behavior_data
    
    def analyze_data_distribution(self):
        """分析数据分布"""
        print("\n=== 数据分布分析 ===")
        
        # 用户分布
        users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
        print(f"用户总数: {len(users_df)}")
        print(f"风险偏好分布:\n{users_df['risk_tolerance'].value_counts()}")
        print(f"收入水平分布:\n{users_df['income_level'].value_counts()}")
        
        # 产品分布
        products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
        print(f"\n产品总数: {len(products_df)}")
        print(f"产品类型分布:\n{products_df['product_type'].value_counts()}")
        print(f"风险等级分布:\n{products_df['risk_level'].value_counts()}")
        
        # 行为数据分布
        behavior_df = pd.read_sql_query("SELECT * FROM user_behavior", self.conn)
        print(f"\n行为数据总数: {len(behavior_df)}")
        print(f"行为类型分布:\n{behavior_df['behavior_type'].value_counts()}")
        print(f"评分分布:\n{behavior_df['rating'].value_counts().sort_index()}")
        
        # 用户平均行为数
        user_behavior_count = behavior_df.groupby('user_id').size()
        print(f"\n用户平均行为数: {user_behavior_count.mean():.2f}")
        print(f"最多行为的用户: {user_behavior_count.max()}")
        print(f"最少行为的用户: {user_behavior_count.min()}")
    
    def generate_all_data(self, num_users=200, num_products=50):
        """生成所有数据"""
        print("开始生成大规模模拟数据...")
        
        # 清空现有数据
        self.clear_existing_data()
        
        # 生成用户数据
        self.generate_users(num_users)
        
        # 生成产品数据  
        self.generate_products(num_products)
        
        # 生成用户行为数据（使用真实模式）
        self.generate_realistic_behavior_patterns(num_users, num_products)
        
        # 分析数据分布
        self.analyze_data_distribution()
        
        print("\n数据生成完成！")
        
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

if __name__ == "__main__":
    # 安装依赖：pip install faker pandas numpy
    
    generator = DataGenerator()
    
    try:
        # 生成200个用户，50个产品
        generator.generate_all_data(num_users=200, num_products=50)
        
        print("\n🎉 数据生成成功！")
        print("现在可以重新运行推荐系统测试效果了。")
        
    except Exception as e:
        print(f"数据生成失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        generator.close()
