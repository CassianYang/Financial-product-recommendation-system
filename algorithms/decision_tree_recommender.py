import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.config import Config
try:
    from .database_utils import DatabaseManager
except ImportError:
    from database_utils import DatabaseManager

class DecisionTreeRecommender:
    def __init__(self, min_samples_for_training=10):
        self.db = DatabaseManager()
        self.model = None
        self.label_encoders = {}
        self.min_samples_for_training = min_samples_for_training
    
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
        """训练决策树模型，使用用户特征预测产品类型偏好"""
        try:
            print("开始训练决策树模型")
            
            # 从数据库获取数据
            behavior_df = self.db.get_user_behavior()
            users_df = self.db.get_all_users()
            
            # 只选择有购买行为的记录
            purchases_df = behavior_df[behavior_df['behavior_type'] == 'purchase']
            
            if len(purchases_df) < self.min_samples_for_training:
                print(f"数据不足，当前购买记录数: {len(purchases_df)}, 最少需要: {self.min_samples_for_training}")
                return None
            
            # 合并数据以获取用户特征和产品类型
            merged_df = pd.merge(purchases_df, users_df, on='user_id', how='left')
            merged_df = pd.merge(merged_df, self.db.get_all_products()[['product_id', 'product_type']], 
                                on='product_id', how='left')
            
            # 检查是否有足够的产品类型用于分类
            preferred_types = merged_df['product_type'].value_counts()
            if len(preferred_types) < 2:
                print("产品类型数量不足，无法训练分类模型")
                return None
            
            # 选择特征列
            feature_columns = ['age', 'income_level', 'risk_tolerance']
            
            # 添加职业列（需要编码）
            merged_df = pd.get_dummies(merged_df, columns=['occupation'], prefix='occupation')
            
            # 更新特征列
            all_feature_cols = [col for col in merged_df.columns if col.startswith('occupation_')]
            feature_columns.extend(all_feature_cols)
            
            # 准备特征和标签
            X = merged_df[feature_columns]
            y = merged_df['product_type']
            
            # 对分类特征进行编码
            categorical_columns = ['income_level', 'risk_tolerance']
            for col in categorical_columns:
                if col in X.columns:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))
                    self.label_encoders[col] = le
            
            # 训练模型
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            self.model = DecisionTreeClassifier(random_state=42, max_depth=10)
            self.model.fit(X_train, y_train)
            
            # 评估模型
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            print(f"模型训练完成！训练集准确率: {train_score:.3f}, 测试集准确率: {test_score:.3f}")
            
            # 保存特征列信息
            self.feature_columns = X.columns.tolist()
            
            # 计算特征重要性
            feature_importances = {}
            for i, col in enumerate(self.feature_columns):
                feature_importances[col] = float(self.model.feature_importances_[i])
            
            summary = {
                'samples': len(purchases_df),
                'preferred_type_count': len(preferred_types),
                'feature_importances': feature_importances,
                'train_accuracy': train_score,
                'test_accuracy': test_score
            }
            
            print(f"训练摘要: {summary}")
            return summary
            
        except Exception as e:
            print(f"模型训练失败: {e}")
            return None
    
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
    
    def _prepare_user_input(self, user_profile):
        """准备用户输入数据用于模型预测"""
        # 准备输入特征
        feature_columns = ['age', 'income_level', 'risk_tolerance']
        X_input = pd.DataFrame([user_profile])[feature_columns]
        
        # 编码分类特征
        for col in ['income_level', 'risk_tolerance']:
            le = self.label_encoders.get(col)
            if le is None:
                raise ValueError("模型尚未训练，缺少编码器")
            # 处理未见过的类别
            if user_profile[col] in le.classes_:
                X_input[col] = le.transform([user_profile[col]])[0]
            else:
                X_input[col] = 0  # 默认值
        
        # 为职业列创建独热编码
        # 首先创建所有职业列的零值
        for col in self.feature_columns:
            if col.startswith('occupation_'):
                X_input[col] = 0
        
        # 然后为用户的职业设置为1
        occupation_col = f"occupation_{user_profile['occupation']}"
        if occupation_col in X_input.columns:
            X_input[occupation_col] = 1
        
        return X_input[self.feature_columns]
    
    def recommend_for_profile(self, user_profile, top_n=5):
        """基于用户画像进行推荐"""
        if self.model is None:
            print("模型未训练，请先训练模型")
            return []
        
        try:
            print(f"基于用户画像生成推荐，top_n={top_n}")
            # 将用户画像转换为模型输入格式
            input_data = self._prepare_user_input(user_profile)
            
            if input_data is None:
                print("用户输入数据格式不正确")
                return []
            
            # 预测用户偏好类型
            predicted_type = self.model.predict(input_data)[0]
            
            # 获取该类型下的产品
            products_df = self.db.get_all_products()
            type_products = products_df[products_df['product_type'] == predicted_type]
            
            # 按预期收益率排序
            type_products = type_products.sort_values('expected_return', ascending=False)
            
            recommendations = []
            for _, product in type_products.head(top_n).iterrows():
                recommendations.append({
                    'product_id': int(product['product_id']),
                    'product_name': product['product_name'],
                    'product_type': product['product_type'],
                    'expected_return': float(product['expected_return']),
                    'reason': f'预测您偏好{predicted_type}类型，推荐该类型收益较高的产品'
                })
            
            print(f"决策树推荐完成，返回 {len(recommendations)} 个推荐")
            return recommendations
            
        except Exception as e:
            print(f"推荐过程出错: {e}")
            return []
    
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