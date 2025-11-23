import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from .database_utils import DatabaseManager
except ImportError:
    from database_utils import DatabaseManager


class ContentBasedRecommender:
    def __init__(self):
        self.db = DatabaseManager()
        self.label_encoders = {}
    
    def prepare_product_features(self):
        """准备产品特征向量 - 修复版本"""
        products_df = self.db.get_all_products()
        
        # 对分类特征进行编码
        feature_columns = ['product_type', 'risk_level']
        
        for col in feature_columns:
            le = LabelEncoder()
            products_df[col + '_encoded'] = le.fit_transform(products_df[col])
            self.label_encoders[col] = le
        
        # 选择数值特征并归一化
        numerical_features = ['expected_return', 'min_investment']
        
        # 归一化数值特征到 [0, 1] 范围
        for feature in numerical_features:
            min_val = products_df[feature].min()
            max_val = products_df[feature].max()
            if max_val > min_val:
                products_df[feature + '_norm'] = (products_df[feature] - min_val) / (max_val - min_val)
            else:
                products_df[feature + '_norm'] = 0.5
        
        # 创建特征矩阵 - 使用编码后的分类特征和归一化的数值特征
        feature_cols = ['product_type_encoded', 'risk_level_encoded', 
                       'expected_return_norm', 'min_investment_norm']
        feature_matrix = products_df[feature_cols].values
        
        return products_df, feature_matrix
    
    def get_user_profile(self, user_id):
        """基于用户历史购买构建用户画像 - 修复版本"""
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
        
        products_df, feature_matrix = self.prepare_product_features()
        
        if not user_purchases:
            # 如果用户没有购买历史，基于用户特征创建画像
            return self.create_profile_from_demographics(user_data, feature_matrix.shape[1])
        
        # 基于购买历史构建画像
        user_products_df = products_df[products_df['product_id'].isin(user_purchases)]
        
        if len(user_products_df) == 0:
            return self.create_profile_from_demographics(user_data, feature_matrix.shape[1])
        
        # 计算用户偏好向量（购买产品的平均特征）
        user_indices = user_products_df.index
        user_feature_matrix = feature_matrix[user_indices]
        user_profile = user_feature_matrix.mean(axis=0)
        
        return user_profile
    
    def create_profile_from_demographics(self, user_data, feature_dim):
        """基于用户人口统计信息创建画像 - 修复版本"""
        # 创建基于用户特征的简单画像
        risk_mapping = {'low': 0, 'medium': 1, 'high': 2}
        income_mapping = {'low': 0, 'medium': 1, 'high': 2}
        occupation_mapping = {'工程师': 2, '教师': 1, '医生': 2, '自由职业': 1, '企业家': 3}
        
        # 简化的特征映射
        profile = np.zeros(feature_dim)
        
        # 根据特征维度调整
        if feature_dim >= 2:
            profile[0] = risk_mapping.get(user_data['risk_tolerance'], 1) / 2.0  # 风险偏好
            profile[1] = income_mapping.get(user_data['income_level'], 1) / 2.0  # 收入水平
        
        if feature_dim >= 4:
            profile[2] = min(user_data['age'] / 80.0, 1.0)  # 年龄归一化
            profile[3] = occupation_mapping.get(user_data['occupation'], 1) / 3.0  # 职业
        
        return profile
    
    def convert_to_serializable(self, obj):
        """将numpy类型转换为Python原生类型，确保JSON可序列化"""
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return obj

    
    def recommend_for_profile(self, user_data, top_n=5):
        """基于用户画像（年龄/职业等）生成推荐"""
        try:
            print(f"开始基于用户画像生成推荐，top_n={top_n}")
            if user_data is None:
                print("用户画像数据为空")
                return []
            
            products_df, product_features = self.prepare_product_features()
            feature_dim = product_features.shape[1]
            user_profile = self.create_profile_from_demographics(user_data, feature_dim)
            
            # 计算用户画像与所有产品的相似度
            similarities = cosine_similarity([user_profile], product_features)[0]
            
            recommendations = []
            for idx, similarity in enumerate(similarities):
                if similarity <= 0:
                    continue
                product = products_df.iloc[idx]
                recommendations.append({
                    'product_id': self.convert_to_serializable(product['product_id']),
                    'product_name': str(product['product_name']),
                    'product_type': str(product['product_type']),
                    'risk_level': str(product['risk_level']),
                    'similarity': self.convert_to_serializable(similarity),
                    'reason': f'画像匹配度 {float(similarity):.3f}'
                })
            
            recommendations.sort(key=lambda x: x['similarity'], reverse=True)
            result = recommendations[:top_n]
            print(f"基于内容推荐完成，返回 {len(result)} 个推荐")
            return result
        except Exception as e:
            print(f"基于内容推荐出错: {e}")
            return []
    
    def recommend_for_user(self, user_id, top_n=5):
        """兼容旧逻辑：继续支持根据用户ID推荐"""
        try:
            products_df, product_features = self.prepare_product_features()
            user_profile = self.get_user_profile(user_id)
            
            if user_profile is None:
                return []
            
            # 确保维度匹配
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
                if product['product_id'] not in purchased_products and similarity > 0:
                    recommendations.append({
                        'product_id': self.convert_to_serializable(product['product_id']),
                        'product_name': str(product['product_name']),
                        'product_type': str(product['product_type']),
                        'risk_level': str(product['risk_level']),
                        'similarity': self.convert_to_serializable(similarity),
                        'reason': f'与您的画像匹配度: {float(similarity):.3f}'
                    })
            
            # 按相似度排序
            recommendations.sort(key=lambda x: x['similarity'], reverse=True)
            return recommendations[:top_n]
            
        except Exception as e:
            print(f"基于内容推荐出错: {e}")
            return []


# 测试代码
if __name__ == "__main__":
    cb = ContentBasedRecommender()
    user_id = 3
    recommendations = cb.recommend_for_user(user_id)
    
    print(f"\n为用户 {user_id} 的基于内容推荐结果:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['product_name']} (相似度: {rec['similarity']:.3f}) - 类型: {rec['product_type']}, 风险: {rec['risk_level']}")