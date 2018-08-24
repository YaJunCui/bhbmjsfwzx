import json
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import message_board
from .. import db
from ..models import Role, User, ReserveInfo


@message_board.route('/message_board/add_message', methods=["GET", "POST"])
@login_required
def add_message():
    return render_template("message_board/add_message.html")


@message_board.route('/message_board/reserve_manage')
@login_required
def reserve_manage():
    reserveInfos = ReserveInfo.query.all()            # 获取所有预约信息
    rows = []
    for reserveInfo in reserveInfos:
        rows.append(reserveInfo.getDictObj())
    result = json.dumps(rows)
    return result



