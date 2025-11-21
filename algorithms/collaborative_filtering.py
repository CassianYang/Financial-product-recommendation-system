from database_utils import DatabaseManager
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFiltering:
    def __init__(self):
        self.db = DatabaseManager()
    
    def create_user_item_matrix(self):
        """创建用户-产品评分矩阵"""
        behavior_df = self.db.get_user_behavior()
        
        # 创建用户-产品评分矩阵
        rating_matrix = behavior_df.pivot_table(
            index='user_id', 
            columns='product_id', 
            values='rating', 
            fill_value=0
        )
        return rating_matrix
    
    def calculate_user_similarity(self, rating_matrix):
        """计算用户之间的相似度"""
        user_similarity = cosine_similarity(rating_matrix)
        user_similarity_df = pd.DataFrame(
            user_similarity, 
            index=rating_matrix.index, 
            columns=rating_matrix.index
        )
        return user_similarity_df
    
    def recommend_for_user(self, target_user_id,top_n=5 ,k=2):
        """为目标用户生成推荐"""
        rating_matrix = self.create_user_item_matrix()
        user_similarity = self.calculate_user_similarity(rating_matrix)
        
        # 获取目标用户的评分向量
        if target_user_id not in rating_matrix.index:
            return []  # 新用户，没有评分数据
        
        target_ratings = rating_matrix.loc[target_user_id]
        
        # 找到最相似的k个用户
        similar_users = user_similarity[target_user_id].sort_values(ascending=False)[1:k+1]
        
        # 计算加权平均评分
        all_products_df = self.db.get_all_products()
        recommendations = []
        
        for product_id in rating_matrix.columns:
            if target_ratings[product_id] == 0:  # 用户还没评分的产品
                weighted_sum = 0
                similarity_sum = 0
                
                for similar_user_id, similarity in similar_users.items():
                    similar_user_rating = rating_matrix.loc[similar_user_id, product_id]
                    if similar_user_rating > 0:
                        weighted_sum += similarity * similar_user_rating
                        similarity_sum += similarity
                
                if similarity_sum > 0:
                    predicted_rating = weighted_sum / similarity_sum
                    product_info = all_products_df[all_products_df['product_id'] == product_id].iloc[0]
                    recommendations.append({
                        'product_id': product_id,
                        'product_name': product_info['product_name'],
                        'predicted_rating': predicted_rating,
                        'similar_users_count': len(similar_users)
                    })
        
        # 按预测评分排序
        recommendations.sort(key=lambda x: x['predicted_rating'], reverse=True)
        return recommendations[:top_n]  # 返回前5个推荐

# 测试代码
if __name__ == "__main__":
    cf = CollaborativeFiltering()
    user_id = 2
    recommendations = cf.recommend_for_user(user_id)
    
    print(f"\n为用户 {user_id} 的协同过滤推荐结果:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['product_name']} (预测评分: {rec['predicted_rating']:.2f})")