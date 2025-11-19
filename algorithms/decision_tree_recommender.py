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
        """训练决策树模型"""
        training_data = self.prepare_training_data()
        
        if len(training_data) == 0:
            print("没有足够的训练数据")
            return
        
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
        
        print("决策树模型训练完成!")
        print(f"训练样本数: {len(X)}")
        print(f"特征重要性: {dict(zip(feature_columns, self.model.feature_importances_))}")
    
    def predict_preference(self, user_data):
        """预测用户偏好"""
        if self.model is None:
            self.train_model()
        
        # 准备输入特征
        feature_columns = ['age', 'occupation', 'income_level', 'risk_tolerance']
        X_input = pd.DataFrame([user_data])[feature_columns]
        
        # 编码分类特征
        for col in ['occupation', 'income_level', 'risk_tolerance']:
            le = self.label_encoders[col]
            # 处理未见过的类别
            if user_data[col] in le.classes_:
                X_input[col] = le.transform([user_data[col]])[0]
            else:
                X_input[col] = 0  # 默认值
        
        # 预测偏好
        predicted_type = self.model.predict(X_input)[0]
        return predicted_type
    
    def recommend_for_user(self, user_id, top_n=3):
        """为用户生成推荐"""
        user_df = self.db.get_user_by_id(user_id)
        if len(user_df) == 0:
            return []
        
        user_data = user_df.iloc[0].to_dict()
        
        # 预测用户偏好类型
        preferred_type = self.predict_preference(user_data)
        
        # 获取该类型的所有产品
        products_df = self.db.get_all_products()
        type_products = products_df[products_df['product_type'] == preferred_type]
        
        # 获取用户已购买的产品
        behavior_df = self.db.get_user_behavior()
        purchased_products = behavior_df[
            (behavior_df['user_id'] == user_id) & 
            (behavior_df['behavior_type'] == 'purchase')
        ]['product_id'].tolist()
        
        # 过滤掉已购买的产品
        recommendations_df = type_products[~type_products['product_id'].isin(purchased_products)]
        
        # 按预期收益排序
        recommendations_df = recommendations_df.sort_values('expected_return', ascending=False)
        
        # 转换为推荐列表
        recommendations = []
        for _, product in recommendations_df.head(top_n).iterrows():
            recommendations.append({
                'product_id': product['product_id'],
                'product_name': product['product_name'],
                'product_type': product['product_type'],
                'expected_return': product['expected_return'],
                'risk_level': product['risk_level'],
                'reason': f'匹配您的偏好类型: {preferred_type}'
            })
        
        return recommendations

# 测试代码
if __name__ == "__main__":
    dt = DecisionTreeRecommender()
    user_id = 4
    recommendations = dt.recommend_for_user(user_id)
    
    print(f"\n为用户 {user_id} 的决策树推荐结果:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['product_name']} (预期收益: {rec['expected_return']}%) - {rec['reason']}")