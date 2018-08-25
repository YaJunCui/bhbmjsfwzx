$(function(){           // 动态修改预约信息时段的值
    var flag = $('#time_interval').attr('flag');
    if(flag) {
        $('#time_interval').find('option[value="'+flag+'"]').attr('selected', 'selected');   
    };

    $("#submit").click(clickSubmitBtnFuc);
});

function clickSubmitBtnFuc() {
    $.ajax({
        type: 'POST',
        url: '/reserve/reserve_edit',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(getData()),             // 获取页面数据
        success: function(data, textStatus) {
            console.log('成功！'+data);
            window.location.href = data['url'];
        },
        error: function(xmlHttpRequest, textStatus, errorTrown) {
            console.log('失败！');
        }
    });
}

function getData() {
    var reserve_id = $('#reserve_id').val();      // id
    var department = $('#department').val();      // 送销单位
    var approver = $('#approver').val();          // 审批人
    var sender = $('#sender').val();              // 送销人
    var telephone = $('#telephone').val() | '--'; // 联系方式
    var date_year = $('#date_year').val();        // 年
    var date_month = $('#date_month').val();      // 月
    var date_day = $('#date_day').val();          // 日
    var time_interval = $('#time_interval :selected').text();// 时段
    var remarks = $('#remarks').val();            // 备注

    return {
        'id': reserve_id,
        'department': department,
        'approver': approver,
        'sender': sender,
        'telephone': telephone,
        'date_year': date_year,
        'date_month': date_month,
        'date_day': date_day,
        'time_interval': time_interval,
        'remarks': remarks,
    };
}