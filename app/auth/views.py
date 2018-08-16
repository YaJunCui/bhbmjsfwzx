from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm

# 处理未确认的账户
@auth.before_app_request
def before_request():
    if current_user.is_authenticated  \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != "auth" \
            and request.endpoint != "static":
        return redirect(url_for("auth.unconfirmed"))

# 账户未被确认的视图
@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")

# 登录
@auth.route("/login", methods=["GET", "POST"])
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
@auth.route("/logout")
@login_required
def logout():
    logout_user()           # 调用flask-login的logout_user(),退出登录
    flash("您已经退出登录！")
    return redirect(url_for("main.index"))

# 注册新用户
@auth.route("/register", methods=["GET", "POST"])
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

# 新用户邮箱确认
@auth.route("/confirm/<token>")
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
@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, "确认账户",
               "auth/email/confirm", user=current_user, token=token)
    flash("新的账户确认信息已发送到您的邮箱！")
    return redirect(url_for("main.index"))