import os
import openai
from dotenv import load_dotenv
from typing import Dict, List, Optional
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LargeModelService:
    """
    大模型服务类，用于处理与大模型API的交互
    """
    
    def __init__(self):
        # 从环境变量获取API密钥
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
        self.model = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
        
        if self.api_key:
            openai.api_key = self.api_key
            if self.base_url:
                openai.base_url = self.base_url
        else:
            logger.warning("未找到API密钥，将使用模拟响应")
    
    def generate_financial_advice(self, user_profile: Dict, recommendations: List[Dict]) -> str:
        """
        基于用户画像和推荐结果生成个性化建议
        
        Args:
            user_profile: 用户画像信息
            recommendations: 推荐的产品列表
            
        Returns:
            个性化建议文本
        """
        if not self.api_key:
            return self._generate_mock_advice(user_profile, recommendations)
        
        try:
            # 构建提示词
            prompt = self._build_financial_prompt(user_profile, recommendations)
            
            # 调用大模型API
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一位专业的金融理财顾问，擅长根据用户画像和金融产品特点提供个性化的投资建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            logger.error(f"大模型API调用失败: {str(e)}")
            # 发生错误时返回模拟响应
            return self._generate_mock_advice(user_profile, recommendations)
    
    def _build_financial_prompt(self, user_profile: Dict, recommendations: List[Dict]) -> str:
        """
        构建金融建议的提示词
        """
        profile_str = f"""
用户画像信息：
- 年龄: {user_profile.get('age', '未知')}
- 职业: {user_profile.get('occupation', '未知')}
- 收入水平: {user_profile.get('income_level', '未知')}
- 风险偏好: {user_profile.get('risk_tolerance', '未知')}
- 投资目标: {user_profile.get('investment_goal', '未知')}
- 投资经验: {user_profile.get('investment_experience', '未知')}
- 投资金额: {user_profile.get('investment_amount', '未知')}
- 特殊需求: {user_profile.get('special_needs', '无')}
"""
        
        recommendations_str = "推荐的金融产品：\n"
        for i, rec in enumerate(recommendations, 1):
            recommendations_str += f"{i}. {rec.get('product_name', '未知产品')} - {rec.get('product_type', '未知类型')}\n"
            if 'expected_return' in rec:
                recommendations_str += f"   预期收益: {rec['expected_return']}%\n"
            if 'risk_level' in rec:
                recommendations_str += f"   风险等级: {rec['risk_level']}\n"
            if 'reason' in rec:
                recommendations_str += f"   推荐理由: {rec['reason']}\n"
            recommendations_str += "\n"
        
        prompt = f"""
{profile_str}

{recommendations_str}

请根据以上用户画像和推荐产品，提供以下内容：
1. 个性化投资建议
2. 为什么这些产品适合该用户
3. 投资组合配置建议
4. 风险提示和注意事项
5. 未来投资规划建议

请使用中文回复，语言专业但易懂。
"""
        
        return prompt
    
    def _generate_mock_advice(self, user_profile: Dict, recommendations: List[Dict]) -> str:
        """
        生成模拟的金融建议（当没有API密钥时使用）
        """
        advice = "【模拟建议 - 请配置API密钥以获得真实大模型建议】\n\n"
        
        # 根据用户画像生成个性化内容
        age = user_profile.get('age', 30)
        risk_tolerance = user_profile.get('risk_tolerance', '中等')
        investment_experience = user_profile.get('investment_experience', '有经验')
        
        if risk_tolerance == 'high':
            advice += "根据您的高风险偏好，推荐的这些产品具有较高的增长潜力。\n"
        elif risk_tolerance == 'low':
            advice += "根据您的低风险偏好，推荐的这些产品注重本金安全和稳定收益。\n"
        else:
            advice += "根据您的中等风险偏好，推荐的这些产品在风险和收益之间取得了良好平衡。\n"
        
        if age < 30:
            advice += "作为年轻投资者，您有较长的投资期限，可以考虑增加一些成长型投资。\n"
        elif age > 50:
            advice += "接近退休年龄，建议重点关注资本保值和稳定收益的产品。\n"
        else:
            advice += "您的年龄阶段适合平衡型投资组合，兼顾增长和稳定。\n"
        
        advice += "\n投资组合建议：\n"
        for i, rec in enumerate(recommendations[:3], 1):
            advice += f"{i}. {rec.get('product_name', '产品')} - 适合您的{risk_tolerance}风险偏好\n"
        
        advice += "\n风险提示：\n"
        advice += "1. 投资有风险，过往业绩不代表未来表现\n"
        advice += "2. 请根据自身财务状况合理配置投资比例\n"
        advice += "3. 定期审视投资组合，必要时进行调整\n"
        
        return advice


# 全局实例
large_model_service = LargeModelService()