import json
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import message_board
from .. import db
from ..models import Role, User


@message_board.route('/message_board/add_message', methods=["GET", "POST"])
@login_required
def add_message():
    # user = User.query.get_or_404(current_user.id)
    # form = ReserveInfoForm()
    # if form.validate_on_submit():
    #     reserve_info = ReserveInfo(
    #         department = form.department.data,
    #         approver = form.approver.data,
    #         sender = form.sender.data,
    #         telephone = form.telephone.data,
    #         date_year = form.date_year.data,
    #         date_month = form.date_month.data,
    #         date_day = form.date_day.data,
    #         time_interval = form.time_interval.data,
    #         remarks = form.remarks.data
    #     )
    #     db.session.add(reserve_info)  # 通过_get_current_object()获取User对象
    #     db.session.commit()
    #     flash('您的预约信息已经增加！')
    #     return redirect(url_for('reserve.add_reserve'))
    # form.department.data = current_user.department
    return render_template("message_board/add_message.html")


@message_board.route('/message_board/reserve_manage')
@login_required
def reserve_manage():
    rows =  [{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"测试2",
        'approver':"小军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"测试1",
        'approver':"小兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
       'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
       'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
       'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
        'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
        'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
        'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
        'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
        'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
        'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
        'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
        'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
        'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
        'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
        'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
        'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
        'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
        'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
        'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    },{
        'department':"市涉密载体销毁管理中心",
        'approver':"崔亚军",
        'sender':"李四",
        'telephone':"18977950202",
        'reserve_date':"2017-08-19",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据"
    }, {
        'department':"市涉密载体销毁管理中心1",
        'approver':"户尊兰",
        'sender':"李四1",
        'telephone':"18977950203",
        'reserve_date':"2017-08-18",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }, {
        'department':"市涉密载体销毁管理中心2",
        'approver':"崔亚军",
        'sender':"李四2",
        'telephone':"18977950203",
        'reserve_date':"2017-08-28",
        'time_interval':"08:00--09:00",
        'remarks':"测试数据2"
    }]

    result = json.dumps(rows)
    return result



