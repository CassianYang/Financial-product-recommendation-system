import sqlite3
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# 确保数据目录存在
os.makedirs('data', exist_ok=True)

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
    
    def generate_users(self, num_users=500):
        """生成更多用户数据，更符合实际情况"""
        # 更多样化的用户职业
        occupations = [
            '工程师', '教师', '医生', '公务员', '企业家', '自由职业', '学生', '退休人员', 
            '经理', '销售', '律师', '会计师', '设计师', '分析师', '研究员', '行政人员',
            '市场专员', 'IT专业人员', '金融从业者', '建筑师', '护士', '警察', '消防员',
            '记者', '艺术家', '音乐家', '厨师', '飞行员', '律师助理', '医生助理'
        ]
        
        # 年龄与职业的关联性
        occupation_age_ranges = {
            '学生': (18, 25),
            '退休人员': (55, 80),
        }
        
        users_data = []
        for i in range(1, num_users + 1):
            # 根据职业选择合适的年龄
            occupation = random.choice(occupations)
            
            # 职业特定的年龄范围
            if occupation in occupation_age_ranges:
                age_min, age_max = occupation_age_ranges[occupation]
                age = random.randint(age_min, age_max)
            else:
                if occupation in ['工程师', 'IT专业人员', '金融从业者', '律师', '会计师', '设计师', '分析师']:
                    # 职业相关年龄范围
                    age = random.randint(23, 50)
                elif occupation in ['医生', '律师', '建筑师']:
                    # 需要更多经验的职业
                    age = random.randint(28, 55)
                else:
                    # 普通职业年龄范围
                    age = random.randint(18, 65)
            
            # 根据年龄、职业和收入水平设定风险承受能力
            if age < 25:
                income = random.choices(['low', 'medium'], weights=[0.7, 0.3])[0]
                risk = random.choices(['low', 'medium'], weights=[0.6, 0.4])[0]
            elif age < 35:
                income = random.choices(['low', 'medium', 'high'], weights=[0.4, 0.4, 0.2])[0]
                risk = random.choices(['low', 'medium', 'high'], weights=[0.2, 0.5, 0.3])[0]
            elif age < 50:
                income = random.choices(['low', 'medium', 'high'], weights=[0.2, 0.5, 0.3])[0]
                risk = random.choices(['low', 'medium', 'high'], weights=[0.1, 0.4, 0.5])[0]
            else:
                income = random.choices(['medium', 'high'], weights=[0.6, 0.4])[0]
                risk = random.choices(['low', 'medium'], weights=[0.5, 0.5])[0]
                
            # 职业与收入、风险的关联
            if occupation in ['企业家', 'IT专业人员', '金融从业者', '律师', '医生', '建筑师', '经理']:
                if income == 'low':
                    income = random.choices(['medium', 'high'], weights=[0.4, 0.6])[0]
                risk = random.choices(['medium', 'high'], weights=[0.3, 0.7])[0]
            elif occupation in ['教师', '公务员', '护士']:
                income = random.choices(['low', 'medium'], weights=[0.2, 0.8])[0]
                risk = random.choices(['low', 'medium'], weights=[0.7, 0.3])[0]
            elif occupation == '学生':
                income = 'low'
                risk = 'high' if random.random() > 0.5 else 'medium'
            elif occupation == '退休人员':
                income = random.choices(['low', 'medium'], weights=[0.7, 0.3])[0]
                risk = 'low'
            
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
    
    def generate_products(self, num_products=100):
        """生成更多金融产品数据，更符合实际情况"""
        # 产品类别和子类别的映射
        product_subtypes = {
            '货币基金': ['现金管理', '短期理财', '流动性管理'],
            '债券基金': ['国债基金', '企业债基金', '可转债基金', '信用债基金'],
            '股票基金': ['大盘股基金', '中小盘股基金', '行业主题基金', '价值型基金', '成长型基金', '科技股基金'],
            '混合基金': ['偏股混合', '偏债混合', '平衡型混合', '灵活配置型'],
            '指数基金': ['宽基指数', '行业指数', '主题指数', '国际指数', 'ETF基金'],
            '保险产品': ['养老保险', '健康保险', '投资连结保险', '万能险', '分红险'],
            '银行理财': ['固定收益类', '权益类', '混合类', '商品及金融衍生品类', '现金管理类'],
            '信托产品': ['房地产信托', '工商企业信托', '基础产业信托', '证券投资信托'],
            '私募基金': ['私募股权', '私募证券', '创业投资', '并购基金', '定增基金'],
            '贵金属投资': ['实物黄金', '纸黄金', '黄金ETF', '白银投资', '铂金投资']
        }
        
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
            'low': (2.0, 6.0),      # 低风险产品收益较低但稳定
            'medium': (5.0, 10.0),  # 中等风险产品收益适中
            'high': (8.0, 20.0)     # 高风险产品收益较高但波动大
        }
        
        investment_mapping = {
            'low': (100, 10000),     # 低风险产品投资门槛较低
            'medium': (1000, 50000), # 中等风险产品投资门槛中等
            'high': (10000, 500000)  # 高风险产品投资门槛较高
        }
        
        products_data = []
        product_id = 1
        
        for product_type, subtypes in product_subtypes.items():
            # 每种产品类型生成不同数量的产品
            if product_type == '股票基金':
                num_type_products = int(num_products * 0.15)  # 股票基金占15%
            elif product_type == '混合基金':
                num_type_products = int(num_products * 0.12)  # 混合基金占12%
            elif product_type == '债券基金':
                num_type_products = int(num_products * 0.12)  # 债券基金占12%
            elif product_type == '银行理财':
                num_type_products = int(num_products * 0.12)  # 银行理财占12%
            elif product_type == '指数基金':
                num_type_products = int(num_products * 0.10)  # 指数基金占10%
            elif product_type == '货币基金':
                num_type_products = int(num_products * 0.10)  # 货币基金占10%
            else:
                num_type_products = int(num_products * (0.29 / (len(product_subtypes) - 6)))  # 其他产品平均分配剩余份额
            
            for _ in range(num_type_products):
                if product_id > num_products:
                    break
                
                # 随机选择子类型
                subtype = random.choice(subtypes)
                
                risk_level = risk_mapping[product_type]
                
                # 根据风险等级和产品类型设置预期收益率范围
                min_return, max_return = return_mapping[risk_level]
                
                # 根据产品类型调整收益率（如股票基金通常收益率更高）
                if product_type == '股票基金':
                    min_return = min_return * 1.2
                    max_return = max_return * 1.2
                elif product_type == '私募基金':
                    min_return = min_return * 1.3
                    max_return = max_return * 1.3
                elif product_type == '贵金属投资':
                    # 贵金属投资收益率波动较大
                    min_return = min_return * 0.8
                    max_return = max_return * 1.5
                
                expected_return = round(random.uniform(min_return, max_return), 2)
                
                # 根据风险等级和产品类型设置最低投资额
                min_invest, max_invest = investment_mapping[risk_level]
                
                # 根据产品类型调整最低投资额
                if product_type in ['私募基金', '信托产品']:
                    min_investment = random.randint(min(100000, max_invest), max(100000, max_invest))
                elif product_type in ['银行理财', '保险产品']:
                    min_investment = random.randint(min(10000, max_invest), max(10000, max_invest))
                else:
                    min_investment = random.randint(min_invest, max_invest)
                
                # 生成产品名称
                name = f"{subtype}{product_id}"
                
                products_data.append((product_id, name, product_type, risk_level, expected_return, min_investment))
                product_id += 1
        
        # 插入数据库
        cursor = self.conn.cursor()
        cursor.executemany('''
            INSERT INTO products (product_id, product_name, product_type, risk_level, expected_return, min_investment) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', products_data)
        self.conn.commit()
        print(f"已生成 {len(products_data)} 个金融产品")
        
        return products_data
    
    def generate_realistic_behavior_patterns(self, num_users=500, num_products=100):
        """生成更真实的行为模式，模拟真实的用户投资行为"""
        print("生成真实用户行为模式...")
        
        # 获取用户和产品数据
        users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
        products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
        
        behavior_data = []
        
        # 首先为每类用户生成典型的投资行为模式
        for user_idx, user in users_df.iterrows():
            user_id = user['user_id']
            user_age = user['age']
            user_risk = user['risk_tolerance']
            user_income = user['income_level']
            user_occupation = user['occupation']
            
            # 根据用户特征确定偏好产品类型
            preferred_product_types = []
            if user_risk == 'low':
                preferred_product_types = ['货币基金', '债券基金', '银行理财', '保险产品']
            elif user_risk == 'medium':
                preferred_product_types = ['混合基金', '指数基金', '银行理财', '债券基金']
            else:  # high
                preferred_product_types = ['股票基金', '混合基金', '私募基金', '指数基金']
            
            # 职业对投资偏好的影响
            if user_occupation in ['金融从业者', 'IT专业人员', '律师', '会计师']:
                # 金融相关职业可能更倾向于高收益产品
                if user_risk in ['medium', 'high']:
                    preferred_product_types.extend(['股票基金', '私募基金'])
            elif user_occupation in ['教师', '公务员', '护士']:
                # 稳定职业更倾向于低风险产品
                preferred_product_types = ['货币基金', '债券基金', '银行理财', '保险产品']
            elif user_occupation == '退休人员':
                # 退休人员倾向于保本产品
                preferred_product_types = ['货币基金', '债券基金', '银行理财', '养老保险']
            
            # 根据年龄调整投资策略
            if user_age < 30:
                # 年轻用户可能更愿意承担风险
                if user_risk == 'low':
                    preferred_product_types.extend(['混合基金', '指数基金'])
            elif user_age > 50:
                # 年长用户倾向于保守投资
                preferred_product_types = ['货币基金', '债券基金', '银行理财', '养老保险']
            
            # 去重并确定最终偏好
            preferred_product_types = list(set(preferred_product_types))
            
            # 根据用户特征确定行为频率
            if user_income == 'high':
                num_actions = random.randint(20, 40)  # 高收入用户行为更多
            elif user_income == 'medium':
                num_actions = random.randint(10, 25)  # 中等收入用户行为适中
            else:  # low
                num_actions = random.randint(5, 15)   # 低收入用户行为较少
            
            # 根据年龄调整行为频率
            if user_age < 30:
                num_actions = int(num_actions * 1.2)  # 年轻用户更活跃
            elif user_age > 50:
                num_actions = int(num_actions * 0.8)  # 年长用户较少
            elif user_age > 60:
                num_actions = int(num_actions * 0.6)  # 退休用户更少
            
            # 确保用户至少有5次行为
            num_actions = max(5, num_actions)
            
            # 获取该用户偏好的产品
            preferred_products = products_df[products_df['product_type'].isin(preferred_product_types)]
            
            # 确保用户能看到一些非偏好的产品（多样化）
            non_preferred_products = products_df[~products_df['product_type'].isin(preferred_product_types)]
            
            viewed_products = set()
            purchased_products = set()
            
            # 优先浏览偏好产品
            preferred_product_ids = preferred_products['product_id'].tolist()
            non_preferred_ids = non_preferred_products['product_id'].tolist()
            
            # 根据用户特征决定浏览偏好产品的比例
            if user_risk == 'low':
                preferred_view_ratio = 0.8  # 低风险用户80%浏览偏好产品
            elif user_risk == 'high':
                preferred_view_ratio = 0.6  # 高风险用户60%浏览偏好产品
            else:  # medium
                preferred_view_ratio = 0.7  # 中等风险用户70%浏览偏好产品
            
            # 计算应该浏览的偏好产品和非偏好产品数量
            num_preferred_views = int(num_actions * preferred_view_ratio)
            num_other_views = num_actions - num_preferred_views
            
            # 浏览偏好产品
            if preferred_product_ids:
                preferred_sample = random.sample(
                    preferred_product_ids, 
                    min(num_preferred_views, len(preferred_product_ids))
                )
                viewed_products.update(preferred_sample)
            
            # 浏览非偏好产品
            if non_preferred_ids and len(viewed_products) < num_actions:
                remaining_views = num_actions - len(viewed_products)
                other_sample = random.sample(
                    non_preferred_ids,
                    min(remaining_views, len(non_preferred_ids))
                )
                viewed_products.update(other_sample)
            
            # 生成浏览和购买行为
            for product_id in viewed_products:
                product = products_df[products_df['product_id'] == product_id].iloc[0]
                
                # 根据用户特征和产品特征计算购买概率
                purchase_prob = 0.05  # 基础购买概率
                
                # 如果是偏好产品，增加购买概率
                if product['product_type'] in preferred_product_types:
                    purchase_prob += 0.3
                
                # 根据收入水平调整购买概率
                if user_income == 'high':
                    purchase_prob += 0.15
                elif user_income == 'medium':
                    purchase_prob += 0.05
                
                # 根据风险偏好与产品风险的匹配度调整
                if user_risk == product['risk_level']:
                    purchase_prob += 0.1
                elif (user_risk == 'high' and product['risk_level'] == 'medium') or \
                     (user_risk == 'medium' and product['risk_level'] == 'low'):
                    purchase_prob += 0.08
                
                # 根据预期收益率调整（收益率适中的产品更容易被购买）
                if 5 <= product['expected_return'] <= 12:
                    purchase_prob += 0.05
                elif 12 < product['expected_return'] <= 15:
                    if user_risk == 'high':
                        purchase_prob += 0.03
                elif product['expected_return'] > 15:
                    if user_risk == 'high':
                        purchase_prob += 0.02
                    else:
                        purchase_prob -= 0.05  # 高收益高风险产品对低风险用户吸引力下降
                
                # 根据最低投资额调整
                if product['min_investment'] <= 5000:  # 小额投资门槛低
                    purchase_prob += 0.1
                elif product['min_investment'] > 50000:  # 高门槛产品需要高收入用户
                    if user_income == 'high':
                        purchase_prob += 0.05
                    else:
                        purchase_prob -= 0.1
                
                # 决定是否购买（如果产品还没被购买过）
                if random.random() < purchase_prob and product_id not in purchased_products:
                    behavior_type = 'purchase'
                    purchased_products.add(product_id)
                    
                    # 购买的产品评分更高
                    if product['risk_level'] == user_risk:
                        rating = random.choices([4, 5], weights=[0.2, 0.8])[0]
                    else:
                        rating = random.choices([3, 4, 5], weights=[0.1, 0.4, 0.5])[0]
                else:
                    behavior_type = 'view'
                    
                    # 浏览产品的评分
                    if product['risk_level'] == user_risk:
                        rating = random.choices([3, 4, 5], weights=[0.1, 0.5, 0.4])[0]
                    else:
                        rating = random.choices([1, 2, 3, 4, 5], weights=[0.15, 0.25, 0.4, 0.15, 0.05])[0]
                
                # 生成时间戳（最近180天内，最近的活动更频繁）
                days_ago = random.randint(0, 180)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
                
                behavior_data.append((user_id, product_id, behavior_type, rating, timestamp))
        
        # 批量插入数据库
        cursor = self.conn.cursor()
        batch_size = 10000
        for i in range(0, len(behavior_data), batch_size):
            batch = behavior_data[i:i + batch_size]
            cursor.executemany('''
                INSERT INTO user_behavior (user_id, product_id, behavior_type, rating, timestamp) 
                VALUES (?, ?, ?, ?, ?)
            ''', batch)
            print(f"已插入 {min(i + batch_size, len(behavior_data))} / {len(behavior_data)} 条行为记录")
        
        self.conn.commit()
        print(f"已生成真实行为模式数据，共 {len(behavior_data)} 条记录")
        
        return behavior_data
    
    def analyze_data_distribution(self):
        """分析数据分布"""
        print("\n=== 数据分布分析 ===")
        
        # 用户分布
        users_df = pd.read_sql_query("SELECT * FROM users", self.conn)
        print(f"用户总数: {len(users_df)}")
        print(f"年龄分布:\n{users_df['age'].describe()}")
        print(f"职业分布:\n{users_df['occupation'].value_counts().head(10)}")
        print(f"风险偏好分布:\n{users_df['risk_tolerance'].value_counts()}")
        print(f"收入水平分布:\n{users_df['income_level'].value_counts()}")
        
        # 产品分布
        products_df = pd.read_sql_query("SELECT * FROM products", self.conn)
        print(f"\n产品总数: {len(products_df)}")
        print(f"产品类型分布:\n{products_df['product_type'].value_counts()}")
        print(f"风险等级分布:\n{products_df['risk_level'].value_counts()}")
        print(f"预期收益率范围: {products_df['expected_return'].describe()}")
        print(f"最低投资额范围: {products_df['min_investment'].describe()}")
        
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
        
        # 购买率分析
        purchase_rate = behavior_df[behavior_df['behavior_type'] == 'purchase'].shape[0] / len(behavior_df)
        print(f"整体购买率: {purchase_rate:.2%}")
        
        # 不同产品类型的购买率
        product_purchase_rate = behavior_df.groupby('product_id').apply(
            lambda x: (x['behavior_type'] == 'purchase').sum() / len(x)
        ).reset_index(name='purchase_rate')
        avg_product_purchase_rate = product_purchase_rate['purchase_rate'].mean()
        print(f"产品平均购买率: {avg_product_purchase_rate:.2%}")
    
    def generate_all_data(self, num_users=500, num_products=100):
        """生成所有数据"""
        print("开始生成大规模模拟数据...")
        print(f"计划生成 {num_users} 个用户，{num_products} 个产品")
        
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
        
        print(f"\n数据生成完成！数据库文件: {self.db_path}")
        
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

if __name__ == "__main__":
    # 安装依赖：pip install faker pandas numpy
    
    print("金融产品推荐系统 - 模拟数据生成器")
    print("="*50)
    print("即将生成更符合实际情况的大规模模拟数据...")
    print("用户数量: 500")
    print("产品数量: 100")
    print("行为记录: 约 15000-20000 条")
    print("="*50)
    
    generator = DataGenerator()
    
    try:
        # 生成500个用户，100个产品（比以前更多更真实的数据）
        generator.generate_all_data(num_users=500, num_products=100)
        
        print("\n🎉 数据生成成功！")
        print("现在可以运行推荐系统测试效果了。")
        print("\n使用示例:")
        print("  - 运行 Web 界面: python app.py")
        print("  - 运行 控制台模式: python main.py")
        
    except Exception as e:
        print(f"数据生成失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        generator.close()