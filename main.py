#!/usr/bin/env python
# main.py
# 金融产品推荐系统 - 控制台模式（用户画像驱动）
import sys
import os

# 添加 algorithms 目录到 Python 路径，这样可以直接导入算法模块
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from content_based import ContentBasedRecommender
from decision_tree_recommender import DecisionTreeRecommender
from large_model_recommender import LargeModelRecommender


class FinancialRecommendationSystem:
    def __init__(self):
        self.decision_tree = DecisionTreeRecommender()
        self.content_based = ContentBasedRecommender()
        self.large_model = LargeModelRecommender()
        self.model_trained = False
        self.training_summary = None
        self.occupation_choices = [
            ('工程师', '工程师 / 技术'),
            ('教师', '教师'),
            ('医生', '医生'),
            ('自由职业', '自由职业'),
            ('企业家', '企业家'),
        ]
        self.income_choices = [
            ('low', '低收入 (<8K/月)'),
            ('medium', '中等收入 (8K-20K)'),
            ('high', '高收入 (>20K)'),
        ]
        self.risk_choices = [
            ('low', '低风险'),
            ('medium', '中等风险'),
            ('high', '高风险'),
        ]
        self.investment_goal_choices = [
            ('short_term', '短期(1年以内)'),
            ('medium_term', '中期(1-5年)'),
            ('long_term', '长期(5年以上)'),
            ('retirement', '退休规划'),
            ('education', '教育基金'),
            ('house', '购房计划'),
        ]
        self.investment_experience_choices = [
            ('beginner', '新手'),
            ('intermediate', '有一定经验'),
            ('advanced', '经验丰富'),
            ('professional', '专业投资者'),
        ]
        self.investment_amount_choices = [
            ('small', '小额(<5万)'),
            ('medium', '中等(5-20万)'),
            ('large', '大额(>20万)'),
        ]
        self.special_needs_choices = [
            ('none', '无特殊需求'),
            ('esg', 'ESG投资(环保、社会责任)'),
            ('tax_efficient', '税务优惠产品'),
            ('liquid', '高流动性需求'),
            ('capital_preservation', '本金保障优先'),
        ]

    def display_welcome(self):
        print("=" * 60)
        print("            金融产品推荐系统 - 用户画像模式")
        print("=" * 60)
        print("操作流程：")
        print("  1. 先使用历史用户数据训练决策树模型；")
        print("  2. 输入年龄、职业、收入、风险偏好构建个人画像；")
        print("  3. 选择推荐策略获取个性化金融产品。")
        print("=" * 60)

    def perform_training(self):
        print("\n开始训练模型...")
        print("  1. 训练决策树模型...")
        summary = self.decision_tree.train_model()
        if summary is None:
            print("决策树模型训练失败：数据不足或连接异常。")
        else:
            print("决策树模型训练完成 ✅")
            print(f"  - 训练样本数: {summary['samples']}")
            print(f"  - 偏好类型数: {summary['preferred_type_count']}")
            print("  - 特征重要性:")
            for feature, importance in summary['feature_importances'].items():
                print(f"      · {feature}: {importance:.3f}")
        
        print("\n  2. 训练大模型推荐器...")
        try:
            large_model_summary = self.large_model.train_model()
            if large_model_summary:
                print("大模型推荐器训练完成 ✅")
            else:
                print("大模型推荐器训练未完成或失败")
        except Exception as e:
            print(f"大模型推荐器训练失败: {str(e)}")
        
        # 如果任一模型训练成功，我们就算模型已训练
        self.model_trained = summary is not None
        self.training_summary = summary

    def _prompt_int(self, prompt, min_value, max_value):
        while True:
            try:
                value = input(prompt)
                value = int(value)
                if min_value <= value <= max_value:
                    return value
                print(f"请输入 {min_value}-{max_value} 之间的数字。")
            except ValueError:
                print("请输入有效数字。")

    def _prompt_choice(self, title, choices):
        print(f"\n{title}")
        for idx, (_, label) in enumerate(choices, 1):
            print(f"  {idx}. {label}")
        while True:
            choice = input("请选择编号: ").strip()
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(choices):
                    return choices[idx - 1][0]
            print("输入无效，请重新选择。")

    def collect_user_profile(self):
        print("\n请填写您的基本画像信息：")
        age = self._prompt_int("  年龄 (18-80): ", 18, 80)
        occupation = self._prompt_choice("  职业：", self.occupation_choices)
        income = self._prompt_choice("  收入水平：", self.income_choices)
        risk = self._prompt_choice("  风险偏好：", self.risk_choices)
        
        print("\n请填写更详细的财务信息以获得个性化建议：")
        investment_goal = self._prompt_choice("  投资目标：", self.investment_goal_choices)
        investment_experience = self._prompt_choice("  投资经验：", self.investment_experience_choices)
        investment_amount = self._prompt_choice("  投资金额范围：", self.investment_amount_choices)
        special_needs = self._prompt_choice("  特殊需求：", self.special_needs_choices)
        
        return {
            'age': age,
            'occupation': occupation,
            'income_level': income,
            'risk_tolerance': risk,
            'investment_goal': investment_goal,
            'investment_experience': investment_experience,
            'investment_amount': investment_amount,
            'special_needs': special_needs
        }

    def choose_algorithm(self):
        print("\n请选择推荐策略：")
        print("  1. 决策树推荐（基于训练模型）")
        print("  2. 基于内容推荐（画像匹配）")
        print("  3. 大模型个性化推荐（含专业建议）")
        print("  4. 算法对比")
        while True:
            choice = input("请输入 1/2/3/4: ").strip()
            if choice in ['1', '2', '3', '4']:
                return choice
            print("输入无效，请重新选择。")

    def get_top_n(self):
        while True:
            raw = input("希望获得多少条推荐？(1-10, 默认5): ").strip()
            if not raw:
                return 5
            if raw.isdigit():
                top_n = int(raw)
                if 1 <= top_n <= 10:
                    return top_n
            print("请输入 1-10 之间的数字。")

    def show_recommendations(self, title, recommendations, advice=None):
        print(f"\n{title}")
        print("-" * 40)
        if not recommendations:
            print("  暂无推荐，请调整画像或检查数据。")
            return
        for idx, rec in enumerate(recommendations, 1):
            print(f"  {idx}. {rec['product_name']} ({rec['product_type']})")
            if 'expected_return' in rec:
                print(f"     预期收益: {rec['expected_return']}%")
            if 'similarity' in rec:
                print(f"     匹配度: {rec['similarity']:.3f}")
            if 'reason' in rec:
                print(f"     推荐理由: {rec['reason']}")
        
        # 如果有大模型建议，显示建议
        if advice:
            print(f"\n💡 个性化投资建议:")
            print("=" * 40)
            print(advice)

    def run_recommendations(self, choice, profile, top_n):
        if choice in ['1', '4']:  # 决策树推荐或对比
            if not self.model_trained:
                print("\n请先完成模型训练，再使用决策树推荐。")
            else:
                recs = self.decision_tree.recommend_for_profile(profile, top_n=top_n)
                self.show_recommendations("【决策树推荐】", recs)

        if choice in ['2', '4']:  # 基于内容推荐或对比
            recs = self.content_based.recommend_for_profile(profile, top_n=top_n)
            self.show_recommendations("【基于内容推荐】", recs)
        
        if choice in ['3', '4']:  # 大模型推荐或对比
            try:
                result = self.large_model.recommend_with_advice(profile, top_n=top_n)
                self.show_recommendations("【大模型个性化推荐】", result['recommendations'], result.get('advice', ''))
            except Exception as e:
                print(f"\n大模型推荐出错: {str(e)}")

    def run(self):
        self.display_welcome()
        while True:
            print("\n主菜单：")
            print("  1. 训练 / 更新模型")
            print("  2. 输入用户画像并获取推荐")
            print("  3. 退出系统")
            action = input("请选择 (1/2/3): ").strip()

            if action == '1':
                self.perform_training()
            elif action == '2':
                profile = self.collect_user_profile()
                algo_choice = self.choose_algorithm()
                top_n = self.get_top_n()
                self.run_recommendations(algo_choice, profile, top_n)
            elif action == '3':
                print("\n感谢使用金融产品推荐系统，再见！")
                break
            else:
                print("输入无效，请重新选择。")


if __name__ == "__main__":
    system = FinancialRecommendationSystem()
    system.run()