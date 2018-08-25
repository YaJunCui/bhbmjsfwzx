from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError


# 预约信息表单
class ReserveInfoForm(FlaskForm):
    id = StringField("ID")
    department = StringField("<font color='red'>*</font>送销单位:", validators=[DataRequired(), Length(1, 64)])
    approver = StringField("<font color='red'>*</font>审批人:", validators=[DataRequired(), Length(1, 64)], render_kw={"placeholder":"送销单位审批人"})
    sender = StringField("<font color='red'>*</font>送销人:", validators=[DataRequired(), Length(1, 64)], render_kw={"placeholder":"须在职在编人员"})
    telephone = StringField("联系电话:", validators=[Length(0, 64)])
    date_year = StringField("年")
    date_month = StringField("月")
    date_day = StringField("日")
    time_interval = SelectField("时段")
    remarks = TextAreaField("备注：")
    submit = SubmitField("提交")

    def __init__(self, *args, **kwargs):
        super(ReserveInfoForm, self).__init__(*args, **kwargs)
        self.time_interval.choices = [(time_interval, time_interval) for time_interval in self._get_time_interval()]

    # 时段
    def _get_time_interval(self):
        summer_time_interval = ["08:30--09:30", "09:30--10:30", "10:30--11:30",    # 夏季办公时间
                                "15:00--16:00", "16:00--17:00", "17:00--18:00"]  
        winter_time_interval = ["08:30--09:30", "09:30--10:30", "10:30--11:30",    # 冬季办公时间
                                "14:30--15:30", "15:30--16:30", "16:30--17:30"]

        if datetime.now().month in [5,6,7,8,9,10]:        # 使用夏季办公时间
            return summer_time_interval
        else:                                             # 使用冬季办公时间
            return winter_time_interval
