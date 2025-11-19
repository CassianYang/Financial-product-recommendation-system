from database_utils import DatabaseManager
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder, StandardScaler

class ContentBasedRecommender:
    def __init__(self):
        self.db = DatabaseManager()
        self.label_encoders = {}
    
    def prepare_product_features(self):
        """准备产品特征向量"""
        products_df = self.db.get_all_products()
        
        # 对分类特征进行编码
        feature_columns = ['product_type', 'risk_level']
        
        for col in feature_columns:
            le = LabelEncoder()
            products_df[col + '_encoded'] = le.fit_transform(products_df[col])
            self.label_encoders[col] = le  # 保存编码器供后续使用
        
        # 选择数值特征
        numerical_features = ['expected_return', 'min_investment']
        
        # 创建特征矩阵
        feature_cols = ['product_type_encoded', 'risk_level_encoded'] + numerical_features
        feature_matrix = products_df[feature_cols].values
        
        # 标准化数值特征
        scaler = StandardScaler()
        feature_matrix_scaled = scaler.fit_transform(feature_matrix)
        
        return products_df, feature_matrix_scaled
    
    def get_user_profile(self, user_id):
        """基于用户历史购买构建用户画像"""
        behavior_df = self.db.get_user_behavior()
        user_df = self.db.get_user_by_id(user_id)
        
        if len(user_df) == 0:
            return None
            
        user_data = user_df.iloc[0]
        
        # 获取用户购买的产品
        user_purchases = behavior_df[
            (behavior_df['user_id'] == user_id) & 
            (behavior_df['behavior_type'] == 'purchase')
        ]['product_id'].tolist()
        
        if not user_purchases:
            # 如果用户没有购买历史，基于用户 demographic 信息
            return self.create_profile_from_demographics(user_df.iloc[0])
        
        # 基于购买历史构建画像
        products_df, feature_matrix = self.prepare_product_features()
        user_products_df = products_df[products_df['product_id'].isin(user_purchases)]
        
        if len(user_products_df) == 0:
            return self.create_profile_from_demographics(user_df.iloc[0])
        
        # 计算用户偏好向量（购买产品的平均特征）
        user_indices = user_products_df.index
        user_feature_matrix = feature_matrix[user_indices]
        user_profile = user_feature_matrix.mean(axis=0)
        
        return user_profile
    
    def create_profile_from_demographics(self, user_data):
        """基于用户人口统计信息创建画像（用于新用户）"""
        # 简化的映射逻辑
        risk_mapping = {'low': 0, 'medium': 1, 'high': 2}
        income_mapping = {'low': 0, 'medium': 1, 'high': 2}
        
        # 这里可以根据业务逻辑设计更复杂的画像
        profile = np.array([
            risk_mapping.get(user_data['risk_tolerance'], 1),  # 风险偏好
            income_mapping.get(user_data['income_level'], 1),  # 收入水平
            user_data['age'] / 100,  # 年龄归一化
            0.5, 0.5  # 其他特征占位符
        ])
        
        return profile
    
    def recommend_for_user(self, user_id, top_n=5):
        """为用户生成基于内容的推荐"""
        products_df, product_features = self.prepare_product_features()
        user_profile = self.get_user_profile(user_id)
        
        # 调整维度匹配（简化处理）
        min_dim = min(len(user_profile), product_features.shape[1])
        user_profile_adj = user_profile[:min_dim]
        product_features_adj = product_features[:, :min_dim]
        
        # 计算用户画像与所有产品的相似度
        similarities = cosine_similarity([user_profile_adj], product_features_adj)[0]
        
        # 获取用户已购买的产品（避免重复推荐）
        behavior_df = self.db.get_user_behavior()
        purchased_products = behavior_df[
            (behavior_df['user_id'] == user_id) & 
            (behavior_df['behavior_type'] == 'purchase')
        ]['product_id'].tolist()
        
        # 生成推荐列表
        recommendations = []
        for idx, similarity in enumerate(similarities):
            product = products_df.iloc[idx]
            if product['product_id'] not in purchased_products:
                recommendations.append({
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'similarity': similarity,
                    'product_type': product['product_type'],
                    'risk_level': product['risk_level']
                })
        
        # 按相似度排序
        recommendations.sort(key=lambda x: x['similarity'], reverse=True)
        return recommendations[:top_n]

# 测试代码
if __name__ == "__main__":
    cb = ContentBasedRecommender()
    user_id = 3
    recommendations = cb.recommend_for_user(user_id)
    
    print(f"\n为用户 {user_id} 的基于内容推荐结果:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['product_name']} (相似度: {rec['similarity']:.3f}) - 类型: {rec['product_type']}, 风险: {rec['risk_level']}")