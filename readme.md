# 金融产品推荐系统

## 项目概述

这是一个基于Python的金融产品推荐系统，采用多种推荐算法为用户提供个性化的金融产品推荐。系统主要包含多种推荐算法：

1. **决策树推荐**：基于用户历史行为和特征训练决策树模型，预测用户偏好类型
2. **基于内容的推荐**：通过用户画像与产品特征的相似度匹配进行推荐
3. **协同过滤推荐**：基于用户行为数据的协同过滤算法
4. **关联规则推荐**：使用Apriori算法挖掘产品间的关联关系
5. **大模型推荐**：结合传统算法与大模型生成个性化投资建议

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
├── .env.example             # 环境变量示例
├── .gitignore               # Git忽略文件配置
├── config/                  # 配置文件目录
│   └── config.py            # 应用配置类
├── docs/                    # 文档目录
│   ├── architecture.md      # 系统架构说明
│   ├── README.md            # 文档说明
│   ├── CRM——上机报告2025.doc # 上机报告文档
│   └── flowcharts/          # 流程图目录
│       ├── apriori_flowchart.png                    # Apriori关联规则算法流程图
│       ├── collaborative_filtering_flowchart.png    # 协同过滤算法流程图
│       ├── content_based_flowchart.png              # 基于内容算法流程图
│       ├── decision_tree_flowchart.png              # 决策树算法流程图
│       ├── large_model_flowchart.png                # 大模型算法流程图
│       ├── combined_flowchart.png                   # 系统整体推荐流程图
│       ├── combined_flowchart.txt                   # 组合算法详细流程
│       ├── apriori_visual_guide.txt                 # Apriori算法可视化流程图指南
│       ├── collaborative_filtering_visual_guide.txt # 协同过滤算法可视化流程图指南
│       ├── content_based_visual_guide.txt           # 基于内容算法可视化流程图指南
│       ├── decision_tree_visual_guide.txt           # 决策树算法可视化流程图指南
│       ├── large_model_visual_guide.txt             # 大模型算法可视化流程图指南
│       ├── combined_visual_guide.txt                # 组合算法可视化流程图指南
│       └── flowchart_creation_guide.txt             # 在draw.io中创建流程图指南
├── venv/                    # Python虚拟环境
├── data/                    # 数据存储目录
├── algorithms/              # 推荐算法模块目录
│   ├── __init__.py          # 模块初始化文件
│   ├── apriori_recommender.py          # Apriori关联规则推荐算法
│   ├── collaborative_filtering.py      # 协同过滤推荐算法
│   ├── content_based.py                # 基于内容推荐算法
│   ├── decision_tree_recommender.py    # 决策树推荐算法
│   ├── database_utils.py               # 数据库工具类
│   ├── large_model_recommender.py      # 大模型推荐算法
│   ├── large_model_service.py          # 大模型服务接口
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
- **配置管理**: python-dotenv
- **流程图生成**: graphviz

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

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件配置API密钥等
```

5. 初始化数据库：
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

### 协同过滤推荐
- 基于用户行为数据的协同过滤算法
- 找到具有相似偏好的用户群体
- 推荐相似用户喜欢但当前用户未接触的产品

### 关联规则推荐
- 使用Apriori算法挖掘产品间的关联关系
- 发现用户购买产品A后可能购买产品B的规律
- 推荐与用户已购买产品相关的其他产品

### 大模型推荐
- 结合传统推荐算法和大模型生成个性化建议
- 基于用户画像提供专业投资指导
- 提供更人性化的推荐体验

## 前端界面更新

### 新增算法选项
- 在前端界面中添加了"关联规则推荐（购买关联）"选项
- 在前端界面中添加了"协同过滤推荐（用户相似性）"选项
- 用户现在可以在这五种算法间自由选择

## 使用方法

### Web界面模式
```bash
python app.py
```
访问 http://127.0.0.1:5002

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
系统提供多种推荐算法供调用，支持根据用户画像获取个性化推荐，包括决策树推荐、基于内容推荐、协同过滤推荐、关联规则推荐和大模型推荐。

## 项目特色

- **多算法融合**: 集成多种推荐算法（决策树、基于内容、协同过滤、关联规则、大模型），提高推荐准确性
- **用户画像**: 基于用户特征构建精准画像
- **实时推荐**: 支持基于用户实时行为的推荐
- **Web界面**: 提供友好的交互界面，支持五种算法选择
- **模块化设计**: 算法模块化，便于扩展和维护
- **配置管理**: 使用配置文件管理应用设置
- **可视化流程**: 提供所有算法的详细流程图，便于理解和维护
- **简化设计**: 移除冗余的日志和测试模块，保持代码简洁

## 系统架构

详细架构说明请参见 [docs/architecture.md](docs/architecture.md)。

## 推荐算法流程图

所有推荐算法均有详细的可视化流程图和文本描述，位于 [docs/flowcharts/](docs/flowcharts/) 目录：

- **决策树算法**: `decision_tree_flowchart.png` - 展示决策树模型训练和推荐流程
- **基于内容算法**: `content_based_flowchart.png` - 展示用户画像构建和相似度匹配流程
- **协同过滤算法**: `collaborative_filtering_flowchart.png` - 展示用户相似度计算和推荐生成流程
- **关联规则算法**: `apriori_flowchart.png` - 展示频繁项集挖掘和关联规则发现流程
- **大模型算法**: `large_model_flowchart.png` - 展示大模型与传统算法融合流程
- **系统整体流程**: `combined_flowchart.png` - 展示整个推荐系统的工作流程

此外，目录中还包含创建流程图的指南和算法的详细文本描述。

## 配置大模型服务

### 使用 Ollama (本地部署，推荐用于演示)

1. **安装 Ollama**：
   - 访问 [Ollama 官网](https://ollama.ai/) 下载并安装
   - 启动 Ollama 服务：`ollama serve`

2. **下载小型模型**：
   ```bash
   ollama pull qwen2:0.5b  # 小型模型，适合演示
   # 或
   ollama pull llama3.2
   ```

3. **配置环境变量**：
   - 复制 `.env.example` 为 `.env`
   - 编辑 `.env` 文件，使用以下配置：
   ```env
   OPENAI_API_KEY=ollama
   OPENAI_BASE_URL=http://localhost:11434/v1
   USE_OLLAMA=true
   LLM_MODEL=qwen2:0.5b
   ```

### 使用云端大模型服务

如需使用 OpenAI 或其他云端服务，请参考 `.env.example` 文件中的配置说明。

## 开发约定

- 推荐器类统一实现 `recommend_for_profile` 方法，支持基于用户画像的推荐
- 数据库操作封装在 `DatabaseManager` 类中
- 推荐结果统一包含产品ID、名称、类型、预期收益率等信息
- 使用LabelEncoder对分类特征进行编码处理
- 推荐结果按相关性或预期收益排序
- 使用配置文件管理应用设置

## 项目优化

- 数据预处理优化，提高算法运行效率
- 推荐结果缓存机制，减少重复计算
- 用户行为实时更新，提供更精准推荐
- 配置管理优化，便于环境切换

## 贡献

如果您对本项目感兴趣，欢迎提交 Issue 或 Pull Request。

## 许可证

本项目采用 MIT 许可证。