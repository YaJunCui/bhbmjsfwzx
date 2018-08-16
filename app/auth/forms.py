from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

# 登录表单类
class LoginForm(FlaskForm):
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码：', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

# 注册表单类
class RegistrationForm(FlaskForm):
    email = StringField('邮箱：', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('用户名：', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               '用户名只能包含字母、数字、.和_')])
    password = PasswordField('密码：', validators=[
        DataRequired(), EqualTo('password2', message='两次填写的密码不一致')])
    password2 = PasswordField('确认密码：', validators=[DataRequired()])
    submit = SubmitField('立即注册')

    # 校验邮箱是否已被注册
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮香已被注册')

    # 校验用户名是否已存在
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已经存在')
