from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import reserve
from .forms import ReserveInfoForm
from .. import db
from ..models import Role, User, ReserveInfo


@reserve.route('/add_reserve', methods=["GET", "POST"])
@login_required
def add_reserve():
    user = User.query.get_or_404(current_user.id)
    form = ReserveInfoForm()
    if form.validate_on_submit():
        reserve_info = ReserveInfo(
            department = form.department.data,
            approver = form.approver.data,
            sender = form.sender.data,
            telephone = form.telephone.data,
            date_year = form.date_year.data,
            date_month = form.date_month.data,
            date_day = form.date_day.data,
            time_interval = form.time_interval.data,
            remarks = form.remarks.data
        )
        db.session.add(reserve_info)  # 通过_get_current_object()获取User对象
        db.session.commit()
        flash('您的预约信息已经增加！')
        return redirect(url_for('reserve.add_reserve'))
    form.department.data = current_user.department
    return render_template("reserve/add_reserve.html", form=form)