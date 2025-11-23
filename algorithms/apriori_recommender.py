try:
    from .database_utils import DatabaseManager
except ImportError:
    from database_utils import DatabaseManager
import pandas as pd
from itertools import combinations

class AprioriRecommender:
    def __init__(self, min_support=0.2, min_confidence=0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.db = DatabaseManager()
    
    def prepare_transaction_data(self):
        """准备交易数据：每个用户的购买记录作为一个事务"""
        behavior_df = self.db.get_user_behavior()
        # 只考虑购买行为
        purchase_df = behavior_df[behavior_df['behavior_type'] == 'purchase']
        
        # 按用户分组，收集购买的产品ID
        transactions = purchase_df.groupby('user_id')['product_id'].apply(list).tolist()
        return transactions
    
    def find_frequent_itemsets(self, transactions):
        """实现Apriori算法找频繁项集"""
        # 这里先实现一个简化版本，你可以后续完善
        itemsets = {}
        
        # 计算单项支持度
        for transaction in transactions:
            for item in transaction:
                itemsets[frozenset([item])] = itemsets.get(frozenset([item]), 0) + 1
        
        # 过滤支持度
        num_transactions = len(transactions)
        frequent_itemsets = {}
        for itemset, count in itemsets.items():
            support = count / num_transactions
            if support >= self.min_support:
                frequent_itemsets[itemset] = support
        
        print(f"找到 {len(frequent_itemsets)} 个频繁项集")
        return frequent_itemsets
    
    def recommend_for_user(self, user_id, top_n=3):
        """为用户生成推荐"""
        transactions = self.prepare_transaction_data()
        frequent_itemsets = self.find_frequent_itemsets(transactions)
        
        # 获取用户历史购买记录
        user_behavior = self.db.get_user_behavior()
        user_purchases = user_behavior[
            (user_behavior['user_id'] == user_id) & 
            (user_behavior['behavior_type'] == 'purchase')
        ]['product_id'].tolist()
        
        print(f"用户 {user_id} 的历史购买: {user_purchases}")
        
        # 简化推荐逻辑：推荐其他用户常买但该用户没买的产品
        all_products_df = self.db.get_all_products()
        recommendations = []
        
        for product_id in all_products_df['product_id']:
            if product_id not in user_purchases:
                # 计算该产品的购买频率作为推荐分数
                product_count = sum(1 for transaction in transactions if product_id in transaction)
                score = product_count / len(transactions)
                if score > 0:  # 至少有一个用户购买过
                    product_info = all_products_df[all_products_df['product_id'] == product_id].iloc[0]
                    recommendations.append({
                        'product_id': product_id,
                        'product_name': product_info['product_name'],
                        'score': score,
                        'reason': f'购买频率: {score:.2%}'
                    })
        
        # 按分数排序，返回前top_n个推荐
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:top_n]

# 测试代码
if __name__ == "__main__":
    recommender = AprioriRecommender()
    user_id = 1  # 测试用户ID
    recommendations = recommender.recommend_for_user(user_id)
    
    print(f"\n为用户 {user_id} 的关联规则推荐结果:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['product_name']} (分数: {rec['score']:.3f}) - {rec['reason']}")