"""
系统配置管理 — 支持多环境配置
采用类继承实现配置切换，符合开闭原则
"""

import os


class BaseConfig:
    """基础配置 — 所有环境共享"""
    
    # 应用
    APP_NAME = "CarRentalPro"
    APP_VERSION = "1.0.0"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # 数据库
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///car_rental.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 分页
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
    
    # 租赁业务规则
    MIN_RENTAL_DAYS = 1
    MAX_RENTAL_DAYS = 90
    DEFAULT_DEPOSIT_DAYS = 3  # 押金 = 3天租金
    CANCELLATION_DEADLINE_HOURS = 24  # 免费取消截止时间
    
    # IoT 配置
    IOT_ENABLED = os.getenv("IOT_ENABLED", "false").lower() == "true"
    IOT_MQTT_BROKER = os.getenv("IOT_MQTT_BROKER", "localhost")
    IOT_MQTT_PORT = int(os.getenv("IOT_MQTT_PORT", "1883"))
    TELEMETRY_RETENTION_DAYS = 90
    
    # 特性开关
    FF_DYNAMIC_PRICING = os.getenv("FF_DYNAMIC_PRICING", "false").lower() == "true"
    FF_PREDICTIVE_MAINTENANCE = os.getenv("FF_PREDICTIVE_MAINTENANCE", "false").lower() == "true"
    FF_GEOFENCING = os.getenv("FF_GEOFENCING", "false").lower() == "true"


class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True  # 打印SQL语句便于调试
    
    # 开发环境启用所有特性开关以便测试
    IOT_ENABLED = True
    FF_DYNAMIC_PRICING = True
    FF_PREDICTIVE_MAINTENANCE = True
    FF_GEOFENCING = True


class TestingConfig(BaseConfig):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    
    # 测试用短时限
    MIN_RENTAL_DAYS = 1
    MAX_RENTAL_DAYS = 30


class ProductionConfig(BaseConfig):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    
    # 生产环境密钥必须从环境变量读取
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("Production environment requires SECRET_KEY environment variable")
    
    # 生产数据库
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/carrental")


# 配置映射表
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)()
