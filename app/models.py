from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager


# 角色权限常量
class Permission:
    """
    匿名（0x00）：未登录的用户。
    注册用户（0x01）：用户已经注册，但信息未确认。具有读权限。
    普通用户（0x03）：信息已确认，具有读写权限。
    协管员（0x07）：可以驳回用户的申请
    管理员（0x87）：具有所有权限
    """
    RAED = 0x01        # 读权限
    WRITE = 0x02       # 写权限
    MODERATE = 0x04    # 修改权限
    ADMIN = 0x80       # 管理员权限


# 角色类
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=True, index=True)  # 是否为默认角色
    permissions = db.Column(db.Integer)                        # 角色权限
    users = db.relationship('User', backref='role', lazy='dynamic')

    # 更新角色权限
    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.RAED, Permission.WRITE],
            'Moderator': [Permission.RAED, Permission.WRITE, 
                          Permission.MODERATE],
            'Administrator': [Permission.RAED, Permission.WRITE, 
                              Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()   # 获取角色为r的角色
            if role is None:
                role = Role(name=r)
            role.reset_permissions()                      # 将权限置空
            for perm in roles[r]:                         # 为角色添加权限
                role.add_permission(perm)
            role.default = (role.name == default_role)    # 标识是否为默认缺陷
            db.session.add(role)
        db.session.commit()

    # 添加某项角色权限
    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    # 移除某项角色选项
    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    # 重置角色权限
    def reset_permissions(self):
        self.permissions = 0

    # 判断角色是否有某项权限
    def has_permission(self, perm):
        return self.permissions & perm == perm       # 位与运算

    def __repr__(self):
        return '<Role %r>' % self.name


# 用户类
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))     # 外键
    confirmed = db.Column(db.Boolean, default=False)               # 标志新用户是否已确认
    department = db.Column(db.String(64))                          # 部门名称
    location = db.Column(db.String(128))                           # 位置
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    remarks = db.Column(db.Text())

    # 定义默认的用户角色
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN']:           # 如果邮箱为配置文件ADMIN对应邮箱，则为管理员
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:                                   # 默认角色设为普通用户
                self.role = Role.query.filter_by(default=True).first()
    
    # 不允许读取
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # 将password设定为写属性
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码是否正确
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成邮箱确认令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    # 确认账户
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # 生成重置密码的令牌
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    # 重置密码
    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    # 生成重置邮箱的令牌
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    # 修改邮箱
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    # 检查用户是否有指定权限
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    # 检查用户是否为管理员
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    # 刷新最后访问时间
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
    
    def __repr__(self):
        return '<User %r>' % self.username

# 匿名用户类（角色验证时，出于一致性的考虑）
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 预约信息
class ReserveInfo(db.Model):
    __tablename__ = "reserve_infos"
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(64), index=True)             # 送销部门
    approver = db.Column(db.String(64))                           # 送销单位审批人
    sender = db.Column(db.String(64))                             # 送销人
    telephone = db.Column(db.String(64))                          # 联系电话
    date_year = db.Column(db.String(64))                          # 日期
    date_month = db.Column(db.String(64))                         # 日期
    date_day = db.Column(db.String(64))                           # 日期
    time_interval = db.Column(db.String(64))                      # 时段
    remarks = db.Column(db.Text())                                # 备注

    def getDictObj(self):                                             # 格式化为python字典对象
        return {
            'id': self.id,
            'department': self.department,
            'approver': self.approver,
            'sender': self.sender,
            'telephone': self.telephone,
            'date_year': self.date_year,
            'date_month': self.date_month,
            'date_day': self.date_day,
            'reserve_date': self.date_year+'-'+self.date_month+'-'+self.date_day,
            'time_interval': self.time_interval,
            'remarks': self.remarks
        }

    def __repr__(self):
        return '<ReserveInfo %r>' % self.department