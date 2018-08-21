from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

# 处理未确认的账户
@auth.before_app_request
def before_request():
    # 用户已登录
    if current_user.is_authenticated:
        current_user.ping()             # 更新已登录用户的访问时间
        # 登录用户没有确认
        if not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != "auth" \
            and request.endpoint != "static":
            return redirect(url_for("auth.unconfirmed"))

# 账户未被确认的视图
@auth.route("/auth/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")

# 登录
@auth.route("/auth/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)                   # 把用户标记为已登录；如果在页面选中“记住我”，则浏览器会写入一个cookie
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("无效的用户名或密码，请检查后重试登录！")
    return render_template("auth/login.html", form=form)

# 退出
@auth.route("/auth/logout")
@login_required
def logout():
    logout_user()           # 调用flask-login的logout_user(),退出登录
    flash("您已经退出登录！")
    return redirect(url_for("main.index"))

# 注册新用户
@auth.route("/auth/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, "Confirm Your Account",
                   "auth/email/confirm", user=user, token=token)
        flash("账户确认信息已发送到您的邮箱！")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

# 用户信息
@auth.route("/auth/user_info")
@login_required
def user_info():
    return render_template("auth/user_info.html")

# 新用户邮箱确认
@auth.route("/auth/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("您的信息已经被确认！")
    else:
        flash("您的信息确认链接无效或者已过期！")
    return redirect(url_for("main.index"))

# 重新发送账户确认邮件
@auth.route("/auth/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, "确认账户",
               "auth/email/confirm", user=current_user, token=token)
    flash("新的账户确认信息已发送到您的邮箱！")
    return redirect(url_for("main.index"))

# 修改密码
@auth.route("/auth/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("密码更新成功！")
            return redirect(url_for("main.index"))
        else:
            flash("无效的密码")
    return render_template("auth/change_password.html", form=form)

# 通过邮件发送重置密码的请求
@auth.route("/auth/reset", methods=["GET", "POST"])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, "重置密码",
                       "auth/email/reset_password",
                       user=user, token=token)
        flash("密码重置链接已通过邮件发送给您！")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)

# 重置密码
@auth.route("/auth/reset/<token>", methods=["GET", "POST"])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for("main.index"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash("密码重置成功！")
            return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("main.index"))
    return render_template("auth/reset_password.html", form=form)

# 重置邮箱的请求
@auth.route("/auth/change_email", methods=["GET", "POST"])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, "重置邮箱",
                       "auth/email/change_email",
                       user=current_user, token=token)
            flash("确认重置邮箱的链接已通过邮件发送给您！")
            return redirect(url_for("main.index"))
        else:
            flash("无效的邮箱或者密码")
    return render_template("auth/change_email.html", form=form)

# 重置邮箱
@auth.route("/auth/change_email/<token>")
@login_required
def change_email(token):
    if current_user.change_email(token):       # 调用User对象的change_email方法
        db.session.commit()
        flash("邮箱已重置成功！")
    else:
        flash("无效的邮箱重置请求！")
    return redirect(url_for("main.index"))
