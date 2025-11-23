# 系统架构说明

## 整体架构

金融产品推荐系统采用模块化设计，主要包含以下几个核心组件：

1. **Web界面层 (app.py)**: 使用Flask框架提供Web界面
2. **控制台界面层 (main.py)**: 提供命令行交互界面
3. **算法层 (algorithms/)**: 包含多种推荐算法实现
4. **数据层 (data/)**: SQLite数据库存储用户、产品和行为数据
5. **模板层 (templates/)**: Web页面模板

## 推荐算法架构

### 1. 决策树推荐 (decision_tree_recommender.py)
- 基于用户特征（年龄、职业、收入等）训练决策树模型
- 预测用户偏好产品类型
- 推荐该类型中高质量产品

### 2. 基于内容推荐 (content_based.py)
- 构建用户画像和产品特征向量
- 使用余弦相似度计算匹配度
- 推荐与用户画像匹配的产品

### 3. 协同过滤推荐 (collaborative_filtering.py)
- 基于用户行为相似性进行推荐
- 计算用户间相似度
- 预测用户对未评分产品的评分

### 4. Apriori关联规则推荐 (apriori_recommender.py)
- 挖掘用户购买行为中的关联规则
- 发现产品间的关系
- 推荐相关产品

## 数据库设计

### users表
- user_id: 用户ID
- age: 年龄
- occupation: 职业
- income_level: 收入水平
- risk_tolerance: 风险偏好

### products表
- product_id: 产品ID
- product_name: 产品名称
- product_type: 产品类型
- risk_level: 风险等级
- expected_return: 预期收益率
- min_investment: 最低投资额

### user_behavior表
- behavior_id: 行为ID
- user_id: 用户ID
- product_id: 产品ID
- behavior_type: 行为类型（view, purchase等）
- rating: 评分
- timestamp: 时间戳

## API接口设计

### Web API
- `GET /` - 首页
- `POST /train-model` - 训练模型
- `POST /recommend` - 获取推荐结果

### 推荐接口
- `recommend_for_profile(user_profile, top_n)` - 基于用户画像推荐
- `recommend_for_user(user_id, top_n)` - 基于用户ID推荐

## 项目特色

- **多算法融合**: 集成多种推荐算法，提高推荐准确性
- **用户画像**: 基于用户特征构建精准画像
- **实时推荐**: 支持基于用户实时行为的推荐
- **Web界面**: 提供友好的交互界面
- **模块化设计**: 算法模块化，便于扩展和维护