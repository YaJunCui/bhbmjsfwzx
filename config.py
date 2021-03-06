import os

# 配置基类
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Flasky'
   
    # 关于email的全局变量
    MAIL_SUBJECT_PREFIX = '[Flasky]'            # 邮件主题的前缀
    MAIL_SENDER = 'bhbmjsfwzx@163.com'          # 发件人的地址
    ADMIN = 'bhbmjsfwzx@163.com'                # 管理员邮箱账号

    SQLALCHEMY_POOL_RECYCLE = 5
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20
    FOLLOWERS_PER_PAGE = 50
    COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass

# 开发环境的配置类
class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True                         # 协议用SSL协议而不是TLS协议
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'bhbmjsfwzx@163.com'
    MAIL_PASSWORD = 'bhbmjsfwzx123'             # SMTP授权码，不是登录密码
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:root@127.0.0.1/myFlaskyDev'

# 测试环境的配置类
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://root:root@127.0.0.1/myFlaskyTest'
    WTF_CSRF_ENABLED = False

# 生产环境的配置类
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:root@127.0.0.1/myFlasky'

# 注册不同的配置环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
