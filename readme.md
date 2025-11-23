# 金融产品推荐系统

## 项目概述

这是一个基于Python的金融产品推荐系统，采用多种推荐算法为用户提供个性化的金融产品推荐。系统主要包含两种推荐算法：

1. **决策树推荐**：基于用户历史行为和特征训练决策树模型，预测用户偏好类型
2. **基于内容的推荐**：通过用户画像与产品特征的相似度匹配进行推荐

系统支持两种运行模式：
- Web界面模式（app.py）：通过Flask提供Web界面
- 控制台模式（main.py）：命令行交互界面

## 项目结构

```
Financial-product-recommendation-system/
├── app.py              # Web界面主程序
├── main.py             # 控制台模式主程序
├── generate_large_data.py  # 数据生成脚本
├── algorithms/         # 推荐算法模块
│   ├── decision_tree_recommender.py  # 决策树推荐器
│   ├── content_based.py              # 基于内容推荐器
│   ├── database_utils.py             # 数据库工具
│   └── create_database.py            # 数据库创建脚本
├── data/               # 数据存储目录
│   └── financial_data.db             # SQLite数据库
├── templates/          # Web模板
│   └── index.html      # 主页面模板
```

## 技术栈

- **后端**: Python , Flask
- **数据库**: SQLite
- **机器学习**: scikit-learn
- **数据处理**: pandas, numpy
- **相似度计算**: scikit-learn cosine_similarity

## 数据库设计

系统使用SQLite数据库，包含三个主要表：

1. **users表**: 存储用户信息（年龄、职业、收入水平、风险偏好）
2. **products表**: 存储金融产品信息（产品名称、类型、风险等级、预期收益率、最低投资额）
3. **user_behavior表**: 存储用户行为（浏览、购买记录，评分，时间戳）

## 推荐算法说明

### 决策树推荐
- 利用用户历史购买数据训练决策树模型
- 预测用户最可能偏好的产品类型
- 基于预测类型推荐该类型中预期收益较高的产品

### 基于内容的推荐
- 使用余弦相似度计算用户画像与金融产品特征的匹配度
- 用户画像基于年龄、职业、收入、风险偏好等特征构建
- 推荐与用户画像最匹配的产品

## 运行说明

### Web界面模式
```bash
python app.py
```
访问 http://127.0.0.1:5000

### 控制台模式
```bash
python main.py
```

### 数据生成
```bash
python generate_large_data.py
```
生成模拟用户和产品数据用于测试

## 开发约定

- 推荐器类统一实现 `recommend_for_profile` 方法，支持基于用户画像的推荐
- 数据库操作封装在 `DatabaseManager` 类中
- 推荐结果统一包含产品ID、名称、类型、预期收益率等信息
- 使用LabelEncoder对分类特征进行编码处理
- 推荐结果按相关性或预期收益排序