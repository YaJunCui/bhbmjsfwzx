from flask import Blueprint

auth = Blueprint('auth', __name__)    # 创建名为auth的蓝本

from . import views