import json
from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Role, User, ReserveInfo
from ..decorators import admin_required


@main.route('/')
@login_required
def index():
    return render_template('index.html')

# 获取预约数据
@main.route('/main/total_data', methods=["GET", "POST"])
@login_required
def total_data():
    rows = [{
        'date': '2018-08-30',
        '08:30--09:30':'<span id="9">北海市工业园区管委会</span>',
        '09:30--10:30':'市委组织部',
        '10:30--11:30':'市委办公室',
        '14:30--15:30':'涉密载体销毁中心',
        '15:30--16:30':'北海市国家保密局',
        '16:30--17:30':'市纪委',
    }]
    result = json.dumps(rows)
    return result

# 根据预约信息ID判断是否可以获取预约信息
@main.route('/main/get_reserve_info_flag_by_id', methods=["GET", "POST"])
@login_required
def get_reserve_info_flag_by_id():
    data_dict = request.get_json()      # 获取前台的数据(json格式)
    rows = {'flag': 'fail'}             # flag标记是否可以获取详细信息，默认fail(不可以)

    print('------------------------------------------')
    print(data_dict)
    print('------------------------------------------')

    if current_user.is_moderator() or current_user.is_administrator(): # 管理员和协管用户可以
        rows['flag'] = 'success'
    else:
        reserve_info = ReserveInfo.query.get_or_404(int(data_dict['reserve_id']))
        print('------------------------------------------')
        print(data_dict)
        print(reserve_info.user_id)
        print(current_user.id)
        print('------------------------------------------')
        if reserve_info.user_id == current_user.id:  # 如果当前用户与预约用户是同一用户
            rows['flag'] = 'success'
    
    result = json.dumps(rows)
    return result

# 根据预约信息ID判断是否可以获取预约信息
@main.route('/main/get_reserve_info_by_id/<int:reserve_id>')
@login_required
def get_reserve_info_by_id(reserve_id):
    reserve_info = ReserveInfo.query.get_or_404(reserve_id)
    return render_template("main/reserve_info.html", reserve_info=reserve_info)


# 资料页面路由
@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)

# 普通用户和协管员修改账号信息
@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.department = form.department.data
        current_user.location = form.location.data
        current_user.remarks = form.remarks.data
        db.session.add(current_user._get_current_object())  # 通过_get_current_object()获取User对象
        db.session.commit()
        flash('您的账号信息已经更新！')
        return redirect(url_for('.user', username=current_user.username))
    form.department.data = current_user.department
    form.location.data = current_user.location
    form.remarks.data = current_user.remarks
    return render_template('main/edit_profile.html', form=form)

# 管理员修改账号信息
@main.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.department = form.department.data
        user.location = form.location.data
        user.remarks = form.remarks.data
        db.session.add(user)
        db.session.commit()
        flash('您的账号信息已经更新！')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.department.data = user.department
    form.location.data = user.location
    form.remarks.data = user.remarks
    return render_template('main/edit_profile.html', form=form, user=user)