$(function(){
    $('#table_index').bootstrapTable({
        url:'/main/total_data',         // 获取表格数据的url
        toolbar: "#toolbar",
        cache: false,                        // 是否使用缓存
        pagination: true,                    // 在表格底部显示分页组件，默认false
        pageList: [10, 20, 50, 100],         // 设置页面可以显示的数据条数
        pageSize: 10,                        // 页面数据条数
        pageNumber: 1,                       // 首页页码
        search: true,                        // 是否启用搜索框
        showColumns: true,                   // 是否显示内容列下拉框
        minimumCountColumns: 1,              // 最少允许的列数
        showRefresh: true,                   // 是否显示刷新按钮
        clickToSelect: true,                 // 是否启用点击选中行
        height: 527,                         // 行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        showToggle:true,                     // 是否显示详细视图和列表视图的切换按钮
        onDblClickCell: dblClickCellFunc,
        columns: [{
            field: 'date',
            title: '日期',
        }, {
            field: '08:30--09:30',
            title: '08:30--09:30',
        }, {
            field: '09:30--10:30',
            title: '09:30--10:30',
        }, {
            field: '10:30--11:30',
            title: '10:30--11:30',
        }, {
            field: '14:30--15:30',
            title: '14:30--15:30',
        }, {
            field: '15:30--16:30',
            title: '15:30--16:30',
        }, {
            field: '15:30--16:30',
            title: '15:30--16:30',
        }, {
            field: '16:30--17:30',
            title: '16:30--17:30',
        }]
    });
});

function get_index_data() {
    var data = [{
        'date': '2018-08-30',
        '08:30--09:30':'北海市工业园区管委会',
        '09:30--10:30':'市委组织部',
        '10:30--11:30':'市委办公室',
        '14:30--15:30':'涉密载体销毁中心',
        '15:30--16:30':'北海市国家保密局',
        '16:30--17:30':'市纪委',
    }]
}

function dblClickCellFunc(field, value, row, $element) {
    var reserve_id = $element.children('span').first().attr('id')  // 预约信息的ID
    var data_dict = { 'reserve_id' : reserve_id};

    $.ajax({                                                // 查看预约信息的详情
        type: 'POST',
        url: '/main/get_reserve_info_flag_by_id',
        contentType: 'application/json',
        dataType: 'json',
        data: JSON.stringify(data_dict),                    // 获取页面数据
        success: function(resp, textStatus) {
            if(resp['flag'] == 'success') {                 // 可以获取预约信息
                window.location.href = '/main/get_reserve_info_by_id/'+reserve_id;
            } else {
                alert('由于权限限制，你无法查看别人的预约信息！')
            }
        },
        error: function(xmlHttpRequest, textStatus, errorTrown) {
            console.log('获取信息失败！');
        }
    });
}