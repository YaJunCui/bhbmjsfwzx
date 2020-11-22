from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from ..models import Role, User

# 创建 NameForm 表单类
class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])  # 名为name的文本字段
    submit = SubmitField("Submit")                                         # 名为submit的提交按钮

# 普通用户和协管员编辑账号信息表单
class EditProfileForm(FlaskForm):
    department = StringField("单位名称：", validators=[Length(0, 64)])
    location = StringField("地址：", validators=[Length(0, 64)])
    remarks = TextAreaField("备注：")
    submit = SubmitField("提交")

# 管理员编辑账号信息
class EditProfileAdminForm(FlaskForm):
    email = StringField("邮箱：", validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField("用户名：", validators=[
        DataRequired(), Length(1, 64),
        Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 0,
               "用户名只能包含字母、数字、.和_")])
    confirmed = BooleanField("确认账号信息：")
    role = SelectField("角色：", coerce=int)
    department = StringField("单位名称：", validators=[Length(0, 64)])
    location = StringField("地址：", validators=[Length(0, 64)])
    remarks = TextAreaField("备注：")
    submit = SubmitField("提交")

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    # 校验邮箱
    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError("该邮箱已被注册！")

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError("该用户名已经存在！")

