from database_utils import DatabaseManager
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class DecisionTreeRecommender:
    def __init__(self):
        self.db = DatabaseManager()
        self.model = None
        self.label_encoders = {}
    
    def prepare_training_data(self):
        """准备训练数据：用户特征 -> 购买偏好"""
        users_df = self.db.get_all_users()
        behavior_df = self.db.get_user_behavior()
        products_df = self.db.get_all_products()
        
        # 获取每个用户最常购买的产品类型作为标签
        user_preferences = []
        
        for user_id in users_df['user_id']:
            user_behavior = behavior_df[behavior_df['user_id'] == user_id]
            purchases = user_behavior[user_behavior['behavior_type'] == 'purchase']
            
            if len(purchases) > 0:
                # 找到用户购买最多的产品类型
                purchased_products = purchases.merge(products_df, on='product_id')
                favorite_type = purchased_products['product_type'].mode()
                if len(favorite_type) > 0:
                    user_preferences.append({
                        'user_id': user_id,
                        'preferred_type': favorite_type.iloc[0]
                    })
        
        preference_df = pd.DataFrame(user_preferences)
        
        # 合并用户特征和偏好
        training_data = users_df.merge(preference_df, on='user_id', how='inner')
        
        return training_data
    
    def train_model(self):
        """训练决策树模型，并返回训练摘要"""
        training_data = self.prepare_training_data()
        
        if len(training_data) == 0:
            print("没有足够的训练数据")
            self.model = None
            self.label_encoders = {}
            return None
        
        # 特征编码
        feature_columns = ['age', 'occupation', 'income_level', 'risk_tolerance']
        X = training_data[feature_columns].copy()
        y = training_data['preferred_type']
        
        # 对分类特征进行编码
        for col in ['occupation', 'income_level', 'risk_tolerance']:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.label_encoders[col] = le
        
        # 训练决策树模型
        self.model = DecisionTreeClassifier(random_state=42)
        self.model.fit(X, y)
        
        summary = {
            'samples': len(X),
            'preferred_type_count': training_data['preferred_type'].nunique(),
            'feature_importances': dict(zip(feature_columns, self.model.feature_importances_))
        }
        
        print("决策树模型训练完成!")
        print(f"训练样本数: {summary['samples']}")
        print(f"特征重要性: {summary['feature_importances']}")
        return summary
    
    def predict_preference(self, user_data):
        """预测用户偏好"""
        if self.model is None or not self.label_encoders:
            summary = self.train_model()
            if summary is None:
                raise ValueError("模型尚未训练，无法完成预测")
        
        # 准备输入特征
        feature_columns = ['age', 'occupation', 'income_level', 'risk_tolerance']
        X_input = pd.DataFrame([user_data])[feature_columns]
        
        # 编码分类特征
        for col in ['occupation', 'income_level', 'risk_tolerance']:
            le = self.label_encoders.get(col)
            if le is None:
                raise ValueError("模型尚未训练，缺少编码器")
            # 处理未见过的类别
            if user_data[col] in le.classes_:
                X_input[col] = le.transform([user_data[col]])[0]
            else:
                X_input[col] = 0  # 默认值
        
        # 预测偏好
        predicted_type = self.model.predict(X_input)[0]
        return predicted_type
    
    def recommend_for_profile(self, user_data, top_n=3, exclude_product_ids=None):
        """基于用户画像（无需用户ID）生成推荐"""
        if user_data is None:
            return []
        
        preferred_type = self.predict_preference(user_data)
        
        products_df = self.db.get_all_products()
        type_products = products_df[products_df['product_type'] == preferred_type]
        
        if exclude_product_ids:
            type_products = type_products[~type_products['product_id'].isin(exclude_product_ids)]
        
        recommendations_df = type_products.sort_values('expected_return', ascending=False)
        
        recommendations = []
        for _, product in recommendations_df.head(top_n).iterrows():
            recommendations.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'product_type': product['product_type'],
                'expected_return': product['expected_return'],
                'risk_level': product['risk_level'],
                'reason': f'预测您偏好 {preferred_type} 产品'
            })
        
        return recommendations
    
    def recommend_for_user(self, user_id, top_n=3):
        """兼容旧逻辑，仍可通过用户ID获取推荐"""
        user_df = self.db.get_user_by_id(user_id)
        if len(user_df) == 0:
            return []
        
        user_data = user_df.iloc[0].to_dict()
        
        behavior_df = self.db.get_user_behavior()
        purchased_products = behavior_df[
            (behavior_df['user_id'] == user_id) & 
            (behavior_df['behavior_type'] == 'purchase')
        ]['product_id'].tolist()
        
        return self.recommend_for_profile(
            user_data,
            top_n=top_n,
            exclude_product_ids=purchased_products
        )

# 测试代码
if __name__ == "__main__":
    dt = DecisionTreeRecommender()
    user_id = 4
    recommendations = dt.recommend_for_user(user_id)
    
    print(f"\n为用户 {user_id} 的决策树推荐结果:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['product_name']} (预期收益: {rec['expected_return']}%) - {rec['reason']}")