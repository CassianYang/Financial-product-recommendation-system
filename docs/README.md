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
│   │   ├── apriori_flowchart_improved.png          # Apriori算法流程图
│   │   ├── collaborative_filtering_flowchart_improved.png # 协同过滤算法流程图
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