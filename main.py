# main.py
# 金融产品推荐系统 - 主程序
import sys
import os

# 添加 algorithms 目录到 Python 路径，这样可以直接导入算法模块
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from database_utils import DatabaseManager
from apriori_recommender import AprioriRecommender
from collaborative_filtering import CollaborativeFiltering
from content_based import ContentBasedRecommender
from decision_tree_recommender import DecisionTreeRecommender

class FinancialRecommendationSystem:
    def __init__(self):
        self.db = DatabaseManager()
        self.recommenders = {
            '1': ('关联规则推荐 (Apriori)', AprioriRecommender()),
            '2': ('协同过滤推荐', CollaborativeFiltering()),
            '3': ('基于内容推荐', ContentBasedRecommender()),
            '4': ('决策树推荐', DecisionTreeRecommender())
        }
    
    def display_welcome(self):
        """显示欢迎界面"""
        print("=" * 50)
        print("      金融产品推荐系统")
        print("=" * 50)
        print("本系统提供多种智能推荐算法：")
        for key, (name, _) in self.recommenders.items():
            print(f"  {key}. {name}")
        print("=" * 50)
    
    def get_user_input(self):
        """获取用户输入"""
        while True:
            try:
                user_id = int(input("请输入用户ID (1-5): "))
                if 1 <= user_id <= 5:
                    break
                else:
                    print("用户ID范围是1-5，请重新输入！")
            except ValueError:
                print("请输入有效的数字！")
        
        print("\n请选择推荐算法：")
        for key, (name, _) in self.recommenders.items():
            print(f"  {key}. {name}")
        print("  5. 全部算法对比")
        
        while True:
            choice = input("请选择 (1-5): ")
            if choice in ['1', '2', '3', '4', '5']:
                break
            else:
                print("请输入1-5之间的数字！")
        
        return user_id, choice
    
    def get_user_info(self, user_id):
        """获取并显示用户信息"""
        user_df = self.db.get_user_by_id(user_id)
        if len(user_df) > 0:
            user = user_df.iloc[0]
            print(f"\n当前用户: ID{user_id}")
            print(f"  年龄: {user['age']} | 职业: {user['occupation']}")
            print(f"  收入水平: {user['income_level']} | 风险承受: {user['risk_tolerance']}")
        return user_df
    
    def run_single_algorithm(self, user_id, algorithm_choice):
        """运行单个算法 - 增强错误处理"""
        algorithm_name, recommender = self.recommenders[algorithm_choice]
        print(f"\n{'='*60}")
        print(f"正在使用 {algorithm_name}...")
        print(f"{'='*60}")
        
        try:
            # 确保算法有recommend_for_user方法
            if hasattr(recommender, 'recommend_for_user'):
                recommendations = recommender.recommend_for_user(user_id)
            else:
                print(f"  错误: {algorithm_name} 缺少 recommend_for_user 方法")
                return
            
            if not recommendations:
                print("  暂无推荐结果")
                return
            
            print(f"\n推荐结果 (共{len(recommendations)}个):")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec['product_name']}")
                
                # 显示产品信息
                print(f"     类型: {rec.get('product_type', '未知')}, 风险: {rec.get('risk_level', '未知')}")
                
                # 显示推荐指标
                if 'score' in rec:
                    print(f"     推荐度: {rec['score']:.3f}")
                elif 'predicted_rating' in rec:
                    print(f"     预测评分: {rec['predicted_rating']:.2f}")
                elif 'similarity' in rec:
                    print(f"     匹配度: {rec['similarity']:.3f}")
                elif 'expected_return' in rec:
                    print(f"     预期收益: {rec['expected_return']}%")
                
                # 显示推荐原因
                if 'reason' in rec:
                    print(f"     原因: {rec['reason']}")
                print()
                    
        except Exception as e:
            print(f"  算法执行出错: {e}")
            import traceback
            traceback.print_exc()  # 打印详细错误信息
    
    def run_all_algorithms(self, user_id):
        """运行所有算法进行对比"""
        print(f"\n{'='*60}")
        print(f"为用户 {user_id} 的全面推荐分析")
        print(f"{'='*60}")
        
        for algo_key, (algo_name, recommender) in self.recommenders.items():
            print(f"\n{algo_name}:")
            print("-" * 40)
            
            try:
                recommendations = recommender.recommend_for_user(user_id, top_n=2)
                
                if not recommendations:
                    print("  暂无推荐")
                    continue
                
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec['product_name']}")
                    # 显示关键指标
                    if 'score' in rec:
                        print(f"     推荐度: {rec['score']:.3f}")
                    elif 'predicted_rating' in rec:
                        print(f"     预测评分: {rec['predicted_rating']:.2f}")
                    elif 'similarity' in rec:
                        print(f"     匹配度: {rec['similarity']:.3f}")
                    elif 'expected_return' in rec:
                        print(f"     预期收益: {rec['expected_return']}%")
            except Exception as e:
                print(f"  执行出错: {e}")
    
    def run(self):
        """运行主程序"""
        self.display_welcome()
        
        while True:
            try:
                user_id, choice = self.get_user_input()
                self.get_user_info(user_id)
                
                if choice == '5':
                    self.run_all_algorithms(user_id)
                else:
                    self.run_single_algorithm(user_id, choice)
                
                # 询问是否继续
                continue_choice = input("\n是否继续推荐？(y/n): ").lower()
                if continue_choice != 'y':
                    print("\n感谢使用金融产品推荐系统！")
                    break
                print("\n" + "="*60 + "\n")
                    
            except KeyboardInterrupt:
                print("\n\n程序已退出！")
                break
            except Exception as e:
                print(f"发生错误: {e}")
                continue_choice = input("是否继续？(y/n): ").lower()
                if continue_choice != 'y':
                    break

if __name__ == "__main__":
    system = FinancialRecommendationSystem()
    system.run()