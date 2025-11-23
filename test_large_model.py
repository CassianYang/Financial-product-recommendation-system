#!/usr/bin/env python
# test_large_model.py
# 测试大模型推荐功能

import sys
import os

# 添加 algorithms 目录到 Python 路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from large_model_recommender import LargeModelRecommender

def test_large_model_recommender():
    print("开始测试大模型推荐功能...")
    
    # 创建大模型推荐器实例
    recommender = LargeModelRecommender()
    
    # 尝试训练模型
    print("\n1. 训练大模型推荐器...")
    try:
        summary = recommender.train_model()
        if summary:
            print("✓ 大模型推荐器训练成功")
        else:
            print("? 大模型推荐器训练未完成（可能由于缺少数据）")
    except Exception as e:
        print(f"✗ 大模型推荐器训练失败: {e}")
    
    # 创建测试用户画像
    test_profile = {
        'age': 30,
        'occupation': '工程师',
        'income_level': 'high',
        'risk_tolerance': 'medium',
        'investment_goal': 'long_term',
        'investment_experience': 'intermediate',
        'investment_amount': 'medium',
        'special_needs': 'none'
    }
    
    print("\n2. 测试大模型个性化推荐...")
    try:
        result = recommender.recommend_with_advice(test_profile, top_n=3)
        print("✓ 大模型推荐成功")
        print(f"  - 推荐产品数量: {len(result['recommendations'])}")
        print(f"  - 算法使用: {result['algorithm_used']}")
        print(f"  - 个性化建议长度: {len(result['advice'])} 字符")
        
        print("\n  推荐产品:")
        for i, rec in enumerate(result['recommendations'], 1):
            print(f"    {i}. {rec.get('product_name', '未知产品')} - {rec.get('product_type', '未知类型')}")
        
        print(f"\n  个性化建议预览 (前200字符):")
        print(f"    {result['advice'][:200]}...")
        
    except Exception as e:
        print(f"✗ 大模型推荐失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_large_model_recommender()
