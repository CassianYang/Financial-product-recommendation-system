#!/usr/bin/env python
# main.py
# 金融产品推荐系统 - 控制台模式（用户画像驱动）
import sys
import os

# 添加 algorithms 目录到 Python 路径，这样可以直接导入算法模块
sys.path.append(os.path.join(os.path.dirname(__file__), 'algorithms'))

from content_based import ContentBasedRecommender
from decision_tree_recommender import DecisionTreeRecommender


class FinancialRecommendationSystem:
    def __init__(self):
        self.decision_tree = DecisionTreeRecommender()
        self.content_based = ContentBasedRecommender()
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
        print("\n开始训练决策树模型...")
        summary = self.decision_tree.train_model()
        if summary is None:
            print("训练失败：数据不足或连接异常。")
            self.model_trained = False
            return

        self.model_trained = True
        self.training_summary = summary
        print("训练完成 ✅")
        print(f"  - 训练样本数: {summary['samples']}")
        print(f"  - 偏好类型数: {summary['preferred_type_count']}")
        print("  - 特征重要性:")
        for feature, importance in summary['feature_importances'].items():
            print(f"      · {feature}: {importance:.3f}")

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
        return {
            'age': age,
            'occupation': occupation,
            'income_level': income,
            'risk_tolerance': risk
        }

    def choose_algorithm(self):
        print("\n请选择推荐策略：")
        print("  1. 决策树推荐（基于训练模型）")
        print("  2. 基于内容推荐（画像匹配）")
        print("  3. 双算法对比")
        while True:
            choice = input("请输入 1/2/3: ").strip()
            if choice in ['1', '2', '3']:
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

    def show_recommendations(self, title, recommendations):
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

    def run_recommendations(self, choice, profile, top_n):
        if choice in ['1', '3']:
            if not self.model_trained:
                print("\n请先完成模型训练，再使用决策树推荐。")
            else:
                recs = self.decision_tree.recommend_for_profile(profile, top_n=top_n)
                self.show_recommendations("【决策树推荐】", recs)

        if choice in ['2', '3']:
            recs = self.content_based.recommend_for_profile(profile, top_n=top_n)
            self.show_recommendations("【基于内容推荐】", recs)

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