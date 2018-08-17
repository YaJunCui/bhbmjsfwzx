from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors   # 避免循环导入依赖，因为在views.py和errors.py中要导入蓝本main
from ..models import Permission

# 将Permission类加入模板上下文
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
