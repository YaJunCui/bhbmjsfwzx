from flask import render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Role, User
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('index.html')

# 资料页面路由
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

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
    return render_template('edit_profile.html', form=form)

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
    return render_template('edit_profile.html', form=form, user=user)