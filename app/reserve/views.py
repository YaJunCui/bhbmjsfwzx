import json
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from . import reserve
from .forms import ReserveInfoForm
from .. import db
from ..models import Role, User, ReserveInfo
from ..message_board import message_board

# 新增预约数据
@reserve.route('/reserve/reserve_add', methods=["GET", "POST"])
@login_required
def reserve_add():
    if request.method == 'GET':                       # GET请求         
        user = User.query.get_or_404(current_user.id)
        form = ReserveInfoForm()
        form.department.data = current_user.department
        return render_template("reserve/reserve_add.html", form=form)
    elif request.method == 'POST':                       # POST请求              
        data_dict = request.get_json()                   # 获取前台的数据(json格式)
        reserveInfo = ReserveInfo(
            department = data_dict.get('department',''),
            approver = data_dict.get('approver',''),
            sender = data_dict.get('sender',''),
            telephone = data_dict.get('telephone',''),
            date_year = data_dict.get('date_year',''),
            date_month = data_dict.get('date_month',''),
            date_day = data_dict.get('date_day',''),
            time_interval = data_dict.get('time_interval',''),
            remarks = data_dict.get('remarks',''),
        )
        db.session.add(reserveInfo)                       # 向数据库增加预约数据
        db.session.commit()

        res = {                                           # 返回的数据 
            'url': url_for('reserve.reserve_manage'),
            'code': 'success'
        }     
        return json.dumps(res)  

# 修改预约数据
@reserve.route('/reserve/reserve_edit', methods=["GET", "POST"])
@login_required
def reserve_edit():
    if request.method == "GET":                        # get请求
        reserve_info_id = int(request.args.get('id'))  # 获取预约数据的id
        reserveInfo = ReserveInfo.query.get_or_404(reserve_info_id)

        form = ReserveInfoForm()
        # 获取选中行的预约数据
        form.id.data = reserveInfo.id   
        form.department.data = reserveInfo.department                 
        form.approver.data = reserveInfo.approver
        form.sender.data = reserveInfo.sender
        form.telephone.data = reserveInfo.telephone
        form.date_year.data = reserveInfo.date_year
        form.date_month.data = reserveInfo.date_month
        form.date_day.data = reserveInfo.date_day
        form.time_interval.data = reserveInfo.time_interval
        form.remarks.data = reserveInfo.remarks

        return render_template("reserve/reserve_edit.html", form=form)

    elif request.method == 'POST':                       # POST请求              
        data_dict = request.get_json()                   # 获取前台的数据(json格式)
        reserveInfo = ReserveInfo.query.get_or_404(int(data_dict['id']))

        reserveInfo.department = data_dict.get('department','--')         
        reserveInfo.approver = data_dict.get('approver','--')
        reserveInfo.sender = data_dict.get('sender','--')
        reserveInfo.telephone = data_dict.get('telephone','--')
        reserveInfo.date_year = data_dict.get('date_year','--')
        reserveInfo.date_month = data_dict.get('date_month','--')
        reserveInfo.date_day = data_dict.get('date_day','--')
        reserveInfo.time_interval = data_dict.get('time_interval','--')
        reserveInfo.remarks = data_dict.get('remarks','--')

        db.session.add(reserveInfo)           
        db.session.commit()

        res = {'url': url_for('reserve.reserve_manage')}     # 返回的数据
        return json.dumps(res)  

# 预约管理页面
@reserve.route('/reserve/reserve_manage', methods=["GET", "POST"])
@login_required
def reserve_manage():
    return render_template("reserve/reserve_manage.html")

# 获取预约数据
@reserve.route('/reserve/reserve_data', methods=["GET", "POST"])
@login_required
def reserve_data():
    reserveInfos = ReserveInfo.query.all()            # 获取所有预约信息
    rows = []
    for reserveInfo in reserveInfos:
        rows.append(reserveInfo.getDictObj())
    result = json.dumps(rows)
    return result

# 删除选中的预约数据
@reserve.route('/reserve/reserve_delete', methods=["GET", "POST"])
@login_required
def reserve_delete():
    print(request.get_json())       
    data_dict = request.get_json()                   # 获取前台的数据(json格式)
    for id in data_dict['ids']:                      # 删除选中的数据
        ReserveInfo.query.filter_by(id=int(id)).delete()
    db.session.commit()

    resp = {
        'code': 'success',
    }

    result = json.dumps(resp)
    return result