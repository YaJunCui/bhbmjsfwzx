from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()                                  # 初始化flask_mail邮箱
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()                  
login_manager.session_protection = "strong"     # 防止用户会话被篡改
login_manager.login_view = "auth.login"         

# 工厂函数
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 导入config_name对应名称的配置对象的配置信息
    config[config_name].init_app(app)            # config[config_name]返回的是配置类

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)                  # 初始化flask-login

    from .main import main as main_blueprint                  # 导入蓝本main
    app.register_blueprint(main_blueprint)                    # 注册蓝本main

    from .auth import auth as auth_blueprint                  # 认证，导入蓝本auth
    app.register_blueprint(auth_blueprint)                    # 注册蓝本auth

    from .reserve import reserve as reserve_blueprint         # 预约系统，导入蓝本reserve
    app.register_blueprint(reserve_blueprint)                 # 注册蓝本reserve

    from .message_board import message_board as message_board_blueprint    # 留言板，导入蓝本message_board
    app.register_blueprint(message_board_blueprint)                        # 注册蓝本message_board

    return app

