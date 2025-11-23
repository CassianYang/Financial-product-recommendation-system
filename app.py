# app.py
# 金融产品推荐系统 - Web界面版本

from flask import Flask, render_template, request, jsonify
import sys
import os

# 添加项目根目录和algorithms目录到Python路径
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))
  
from content_based import ContentBasedRecommender
from decision_tree_recommender import DecisionTreeRecommender
from large_model_recommender import LargeModelRecommender
from apriori_recommender import AprioriRecommender
from collaborative_filtering import CollaborativeFiltering
import numpy as np

app = Flask(__name__)

# 初始化推荐器与模型状态
decision_tree_recommender = DecisionTreeRecommender()
content_recommender = ContentBasedRecommender()
large_model_recommender = LargeModelRecommender()
apriori_recommender = AprioriRecommender()
collaborative_filtering = CollaborativeFiltering()

profile_recommenders = {
    'decision_tree': ('决策树推荐', decision_tree_recommender),
    'content': ('基于内容推荐', content_recommender),
    'large_model': ('大模型推荐', large_model_recommender),
    'apriori': ('关联规则推荐', apriori_recommender),
    'collaborative': ('协同过滤推荐', collaborative_filtering)
}

model_trained = False
training_summary = None

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/train-model', methods=['POST'])
def train_model():
    """训练决策树模型"""
    global model_trained, training_summary
    try:
        print("开始训练模型")
        summary = decision_tree_recommender.train_model()
        if summary is None:
            model_trained = False
            training_summary = None
            error_msg = '没有足够的历史数据用于训练，请检查数据库。'
            print(error_msg)
            return jsonify({
                'success': False,
                'error': error_msg
            })
        
        model_trained = True
        training_summary = summary
        print(f"模型训练完成，样本数: {summary['samples']}")
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        model_trained = False
        training_summary = None
        error_msg = f"模型训练失败: {str(e)}"
        print(error_msg)
        return jsonify({'success': False, 'error': error_msg})


def serialize_recommendations(recommendations):
    """确保推荐结果可序列化"""
    serializable_recommendations = []
    for rec in recommendations:
        serializable_rec = {}
        for key, value in rec.items():
            if hasattr(value, 'item'):
                serializable_rec[key] = value.item()
            elif isinstance(value, (np.integer, np.int64)):
                serializable_rec[key] = int(value)
            elif isinstance(value, (np.floating, np.float64)):
                serializable_rec[key] = float(value)
            else:
                serializable_rec[key] = value
        serializable_recommendations.append(serializable_rec)
    return serializable_recommendations


def run_recommender(algo_key, user_profile, top_n):
    """执行指定推荐器"""
    if algo_key not in profile_recommenders:
        raise ValueError('无效的算法选择')
    
    algo_name, recommender = profile_recommenders[algo_key]
    
    if algo_key == 'decision_tree' and not model_trained:
        raise ValueError('请先完成模型训练，再进行推荐。')
    
    # 特殊处理大模型推荐器
    if algo_key == 'large_model':
        result = recommender.recommend_with_advice(user_profile, top_n=top_n)
        return algo_name, serialize_recommendations(result['recommendations']), result.get('advice', '')
    # 特殊处理关联规则推荐器和协同过滤推荐器
    elif algo_key in ['apriori', 'collaborative']:
        # 对于关联规则和协同过滤，需要用户ID，而不是用户画像
        # 使用默认用户ID或从用户画像中获取ID
        user_id = user_profile.get('user_id', 1)  # 默认使用用户ID 1
        if algo_key == 'apriori':
            recommendations = recommender.recommend_for_user(user_id, top_n=top_n)
        else:  # collaborative
            recommendations = recommender.recommend_for_user(user_id, top_n=top_n, k=2)  # k参数只对协同过滤有效
        return algo_name, serialize_recommendations(recommendations), None
    else:
        recommendations = recommender.recommend_for_profile(user_profile, top_n=top_n)
        return algo_name, serialize_recommendations(recommendations), None


@app.route('/recommend', methods=['POST'])
def recommend():
    """基于用户画像生成推荐"""
    try:
        data = request.json
        algorithm = data.get('algorithm', 'decision_tree')
        top_n = data.get('top_n', 5)
        user_profile = data.get('user_profile')
        
        if not user_profile:
            error_msg = '缺少用户画像数据'
            print(error_msg)
            return jsonify({'success': False, 'error': error_msg})
        
        # 对于大模型推荐，我们不需要强制要求基础字段，因为可能有其他扩展字段
        if algorithm != 'large_model':
            required_fields = ['age', 'occupation', 'income_level', 'risk_tolerance']
            missing_fields = [field for field in required_fields if field not in user_profile]
            if missing_fields:
                error_msg = f"缺少字段: {', '.join(missing_fields)}"
                print(error_msg)
                return jsonify({'success': False, 'error': error_msg})
        
        # 确保年龄为整数（如果提供了年龄）
        if 'age' in user_profile:
            try:
                user_profile['age'] = int(user_profile['age'])
            except (ValueError, TypeError):
                error_msg = '年龄必须为数字'
                print(error_msg)
                return jsonify({'success': False, 'error': error_msg})
        
        print(f"收到推荐请求: 算法{algorithm}, 特征{user_profile}, 数量{top_n}")
        
        if algorithm == 'all':
            results = {}
            for algo_key in profile_recommenders:
                try:
                    algo_name, recs, advice = run_recommender(algo_key, user_profile, top_n)
                    if advice is not None:  # 大模型推荐
                        results[algo_name] = {
                            'recommendations': recs,
                            'advice': advice
                        }
                    else:  # 其他算法推荐
                        results[algo_name] = recs
                    print(f"{algo_name}完成: 找到{len(recs)}个推荐")
                except Exception as e:
                    error_msg = f"{profile_recommenders[algo_key][0]} 执行错误: {str(e)}"
                    print(error_msg)
                    if algo_key == 'large_model':
                        results[profile_recommenders[algo_key][0]] = {
                            'recommendations': [{'error': error_msg}],
                            'advice': ''
                        }
                    else:
                        results[profile_recommenders[algo_key][0]] = [{'error': error_msg}]
                    
            return jsonify({
                'success': True,
                'recommendations': results
            })
        else:
            algo_name, recommendations, advice = run_recommender(algorithm, user_profile, top_n)
            print(f"{algo_name}完成: 找到{len(recommendations)}个推荐")
            
            response_data = {
                'success': True,
                'algorithm_name': algo_name,
                'recommendations': recommendations
            }
            
            # 如果是大模型推荐，添加个性化建议
            if advice is not None:
                response_data['advice'] = advice
            
            return jsonify(response_data)
            
    except Exception as e:
        error_msg = f"系统错误: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': error_msg
        })

if __name__ == '__main__':
    print("启动金融产品推荐系统Web服务...")
    print("访问地址: http://127.0.0.1:5002")
    app.run(debug=True, port=5002)