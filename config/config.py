import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///financial_data.db'
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL') or 'https://api.openai.com/v1'
    LLM_MODEL = os.environ.get('LLM_MODEL') or 'gpt-3.5-turbo'
    USE_OLLAMA = os.environ.get('USE_OLLAMA', 'false').lower() == 'true'
    
    # 推荐系统配置
    DEFAULT_TOP_N = 5
    MIN_TRAINING_SAMPLES = 10
    
    


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    DATABASE_URL = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///dev_financial_data.db'


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///financial_data.db'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}