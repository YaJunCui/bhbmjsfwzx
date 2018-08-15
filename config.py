import os
basedir = os.path.abspath(os.path.dirname(__file__))   # 获取文件的绝对路径

# 配置基类
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'bhbmjsfwzx'
   
    MAIL_SUBJECT_PREFIX = '[北海保密技术服务中心]'
    MAIL_SENDER = '北海保密技术服务中心 Admin <bhbmjsfwzx@163.com>'
    ADMIN = os.environ.get('ADMIN', 'bhbmjsfwzx@163.com')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 20
    FOLLOWERS_PER_PAGE = 50
    COMMENTS_PER_PAGE = 30

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bhbmjsfwzx@163.com'
    MAIL_PASSWORD = 'bhbmjsfwzx123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://root:root@45.40.192.224/bhbmjsfwzx_dev'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'mysql+pymysql://root:root@45.40.192.224/bhbmjsfwzx_test'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:root@45.40.192.224/bhbmjsfwzx'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
