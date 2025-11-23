from large_model_service import large_model_service
from decision_tree_recommender import DecisionTreeRecommender
from content_based import ContentBasedRecommender
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LargeModelRecommender:
    """
    大模型推荐器，结合传统推荐算法和大模型的个性化建议
    """
    
    def __init__(self):
        # 初始化其他推荐器用于获取推荐结果
        self.decision_tree_recommender = DecisionTreeRecommender()
        self.content_recommender = ContentBasedRecommender()
        self.model_trained = False
    
    def train_model(self):
        """
        训练内部的决策树模型，为大模型推荐提供基础数据
        """
        try:
            result = self.decision_tree_recommender.train_model()
            if result:
                self.model_trained = True
                return result
            return None
        except Exception as e:
            logger.error(f"训练大模型推荐器的内部模型失败: {str(e)}")
            return None
    
    def recommend_with_advice(self, user_profile: dict, top_n: int = 5, algorithm: str = 'decision_tree'):
        """
        生成推荐结果并结合大模型的个性化建议
        
        Args:
            user_profile: 用户画像
            top_n: 推荐数量
            algorithm: 使用的推荐算法 ('decision_tree', 'content', 'combined')
            
        Returns:
            包含推荐结果和个性化建议的字典
        """
        try:
            # 获取推荐结果
            if algorithm == 'decision_tree':
                recommendations = self.decision_tree_recommender.recommend_for_profile(user_profile, top_n)
            elif algorithm == 'content':
                recommendations = self.content_recommender.recommend_for_profile(user_profile, top_n)
            elif algorithm == 'combined':
                # 结合两种算法的推荐结果
                dt_recs = self.decision_tree_recommender.recommend_for_profile(user_profile, top_n)
                cb_recs = self.content_recommender.recommend_for_profile(user_profile, top_n)
                
                # 合并并去重
                recommendations = []
                seen_products = set()
                
                for rec in dt_recs + cb_recs:
                    product_name = rec.get('product_name')
                    if product_name and product_name not in seen_products:
                        recommendations.append(rec)
                        seen_products.add(product_name)
                    
                    if len(recommendations) >= top_n:
                        break
            else:
                recommendations = self.decision_tree_recommender.recommend_for_profile(user_profile, top_n)
            
            # 生成大模型个性化建议
            advice = large_model_service.generate_financial_advice(user_profile, recommendations)
            
            return {
                'recommendations': recommendations,
                'advice': advice,
                'algorithm_used': algorithm
            }
            
        except Exception as e:
            logger.error(f"大模型推荐器出错: {str(e)}")
            raise e

    def recommend_for_profile(self, user_profile: dict, top_n: int = 5):
        """
        为用户画像生成推荐（兼容现有接口）
        """
        return self.recommend_with_advice(user_profile, top_n)