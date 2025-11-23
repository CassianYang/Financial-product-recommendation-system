# 金融产品推荐系统

## 项目概述

这是一个基于Python的金融产品推荐系统，采用多种推荐算法为用户提供个性化的金融产品推荐。系统主要包含多种推荐算法：

1. **决策树推荐**：基于用户历史行为和特征训练决策树模型，预测用户偏好类型
2. **基于内容的推荐**：通过用户画像与产品特征的相似度匹配进行推荐
3. **大模型推荐**：结合传统算法与大模型生成个性化投资建议

系统支持两种运行模式：
- Web界面模式（app.py）：通过Flask提供Web界面
- 控制台模式（main.py）：命令行交互界面

## 项目结构

```
Financial-product-recommendation-system/
├── app.py                    # Web界面主程序
├── main.py                   # 控制台模式主程序
├── generate_large_data.py    # 数据生成脚本
├── requirements.txt          # 项目依赖
├── readme.md                 # 项目说明文档
├── LICENSE                   # 许可证文件
├── .gitignore               # Git忽略文件配置
├── docs/                    # 文档目录
│   ├── README.md            # 文档说明
│   ├── CRM——上机报告2025.doc # 上机报告文档
│   ├── flowcharts/          # 流程图目录
│   │   ├── content_based_flowchart_improved.png         # 基于内容算法流程图
│   │   ├── decision_tree_flowchart_improved.png         # 决策树算法流程图
│   │   └── combined_flowchart_improved.png              # 组合算法流程图
│   └── architecture.md      # 系统架构说明
├── venv/                    # Python虚拟环境
├── data/                    # 数据存储目录
│   └── financial_data.db    # SQLite数据库文件
├── algorithms/              # 推荐算法模块目录
│   ├── __init__.py          # 模块初始化文件
│   ├── apriori_recommender.py          # Apriori关联规则推荐算法
│   ├── collaborative_filtering.py      # 协同过滤推荐算法
│   ├── content_based.py                # 基于内容推荐算法
│   ├── decision_tree_recommender.py    # 决策树推荐算法
│   ├── database_utils.py               # 数据库工具类
│   └── create_database.py              # 数据库创建脚本
└── templates/               # Web模板目录
    └── index.html           # 主页面模板
```

## 技术栈

- **后端**: Python, Flask
- **数据库**: SQLite
- **机器学习**: scikit-learn
- **数据处理**: pandas, numpy
- **相似度计算**: scikit-learn cosine_similarity
- **Web框架**: Flask
- **前端模板**: Jinja2

## 环境要求

- Python 3.8 或更高版本
- pip 包管理器

## 安装说明

1. 克隆项目到本地：
```bash
git clone https://github.com/CassianYang/Financial-product-recommendation-system.git
cd Financial-product-recommendation-system
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖包：
```bash
pip install -r requirements.txt
```

4. 初始化数据库：
```bash
python algorithms/create_database.py
```

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

### 大模型推荐
- 结合传统推荐算法和大模型生成个性化建议
- 基于用户画像提供专业投资指导
- 提供更人性化的推荐体验

## 使用方法

### Web界面模式
```bash
python app.py
```
访问 http://127.0.0.1:5000

### 控制台模式
```bash
python main.py
```

### 生成测试数据
```bash
python generate_large_data.py
```
生成模拟用户和产品数据用于测试

## API接口

### Web界面API
- `GET /` - 首页
- `POST /train-model` - 训练模型
- `POST /recommend` - 获取推荐结果
- `POST /add_behavior` - 添加用户行为数据

### 推荐接口
系统提供多种推荐算法供调用，支持根据用户画像获取个性化推荐，包括决策树推荐、基于内容推荐和大模型推荐。

## 项目特色

- **多算法融合**: 集成多种推荐算法，提高推荐准确性
- **用户画像**: 基于用户特征构建精准画像
- **实时推荐**: 支持基于用户实时行为的推荐
- **Web界面**: 提供友好的交互界面
- **模块化设计**: 算法模块化，便于扩展和维护

## 系统架构

详细架构说明请参见 [docs/architecture.md](docs/architecture.md)。

## 推荐算法流程图

算法流程图请参见 [docs/flowcharts/](docs/flowcharts/) 目录。

## 开发约定

- 推荐器类统一实现 `recommend_for_profile` 方法，支持基于用户画像的推荐
- 数据库操作封装在 `DatabaseManager` 类中
- 推荐结果统一包含产品ID、名称、类型、预期收益率等信息
- 使用LabelEncoder对分类特征进行编码处理
- 推荐结果按相关性或预期收益排序

## 项目优化

- 数据预处理优化，提高算法运行效率
- 推荐结果缓存机制，减少重复计算
- 用户行为实时更新，提供更精准推荐

## 贡献

如果您对本项目感兴趣，欢迎提交 Issue 或 Pull Request。

## 许可证

本项目采用 MIT 许可证。