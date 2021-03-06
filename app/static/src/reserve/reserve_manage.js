$(function(){
    $('#table_reserve').bootstrapTable({
        url:'/reserve/reserve_data',         // 获取表格数据的url
        toolbar: "#toolbar",
        cache: false,                        // 是否使用缓存
        pagination: true,                    // 在表格底部显示分页组件，默认false
        pageList: [10, 20, 50, 100],         // 设置页面可以显示的数据条数
        pageSize: 10,                        // 页面数据条数
        pageNumber: 1,                       // 首页页码
        sortable: true,                      // 是否启用排序
        sortName: 'reserve_date',            // 要排序的字段
        sortOrder: 'desc',                   // 排序规则
        search: true,                        // 是否启用搜索框
        showColumns: true,                   // 是否显示内容列下拉框
        minimumCountColumns: 1,              // 最少允许的列数
        showRefresh: true,                   // 是否显示刷新按钮
        clickToSelect: true,                 // 是否启用点击选中行
        height: 527,                         // 行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        showToggle:true,                     // 是否显示详细视图和列表视图的切换按钮
        columns: [ {
            checkbox: true,                  // 显示一个复选框
        }, {
            field: 'id',
            title: 'ID',
        }, {
            field: 'department',
            title: '送销单位',
            sortable: true,
        }, {
            field: 'approver',
            title: '审批人',
        }, {
            field: 'sender',
            title: '送销人',
        }, {
            field: 'telephone',
            title: '联系电话',
        }, {
            field: 'reserve_date',
            title: '预约日期',
            sortable: true,                  // 当前列进行排序
        }, {
            field: 'time_interval',
            title: '时段',
        }, {
            field: 'remarks',
            title: '备注',
        }]
    });

    $('#btn_add').click(clickBtnAddFunc);        // 新增按钮的点击事件
    $('#btn_edit').click(clickBtnEditFunc);      // 修改按钮的点击事件
    $('#btn_delete').click(clickBtnDeleteFunc);  // 删除按钮的点击事件
});

// 新增按钮的点击事件函数
function clickBtnAddFunc(params) {
    window.location.href = "/reserve/reserve_add";
}

// 修改按钮的点击事件
function clickBtnEditFunc(params) {
    var lstData = $('#table_reserve').bootstrapTable('getSelections');
    var lstDataLen = lstData.length;

    if(lstDataLen < 1) {
        alert("请选中1行需要修改的数据！");
    } else if(lstDataLen > 1) {
        alert("您已经选中"+lstDataLen+"行数据，您只能选中1行数据进行修改！")
    } else {
        window.location.href = "/reserve/reserve_edit?id="+lstData[0].id;   // 将选中数据的ID通过url传入后台
    }    
}

function clickBtnDeleteFunc(params) {
    $table = $('#table_reserve')
    var lstData = $table.bootstrapTable('getSelections');
    var lstDataLen = lstData.length;

    if(lstDataLen < 1) {
        alert("请选择需要删除的数据！");
    }

    var r = confirm("您确认要删除"+lstDataLen+"条数据吗？");      // 删除预约信息的确认框
    if (r == true) {
        var ids = $.map($table.bootstrapTable('getSelections'), // 获取选中数据行的ID
                        function (row) {  
                            return row.id;
                        });
        var data_dict = { 'ids' : ids};
        $.ajax({                                                // 删除数据
            type: 'POST',
            url: '/reserve/reserve_delete',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify(data_dict),                    // 获取页面数据
            success: function(resp, textStatus) {
                $table.bootstrapTable('remove', {               // 删除数据
                    field: 'id',
                    values: ids
                });
            },
            error: function(xmlHttpRequest, textStatus, errorTrown) {
                console.log('删除失败！');
            }
        });
    } 
}