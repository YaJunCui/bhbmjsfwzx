$(function(){
    $('#table_reserve').bootstrapTable({
        url:'/reserve/reserve_data',         // 获取表格数据的url
        toolbar: "#toolbar",
        cache: false,                        //是否使用缓存
        pagination: true,                    // 在表格底部显示分页组件，默认false
        pageList: [10, 20, 50, 100],         // 设置页面可以显示的数据条数
        pageSize: 10,                        // 页面数据条数
        pageNumber: 1,                       // 首页页码
        // sidePagination: 'server', // 设置为服务器端分页
        sortable: true,                      //是否启用排序
        sortName: 'reserve_date',            // 要排序的字段
        sortOrder: 'desc',                   // 排序规则
        search: true,                        // 是否启用搜索框
        // searchOnEnterKey: true,             // 设置为true时，按回车触发搜索方法，否则自动触发搜索方法
        showColumns: true,                   //是否显示内容列下拉框
        minimumCountColumns: 1,              //最少允许的列数
        showRefresh: true,                   // 是否显示刷新按钮
        clickToSelect: true,                 //是否启用点击选中行
        height: 527,                         //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
        showToggle:true,                     //是否显示详细视图和列表视图的切换按钮
        columns: [ {
            checkbox: true,                  // 显示一个复选框
        }, {
            field: 'department',
            title: '送销单位',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
            sortable: true,
        }, {
            field: 'approver',
            title: '审批人',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
        }, {
            field: 'sender',
            title: '送销人',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
        }, {
            field: 'telephone',
            title: '联系电话',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
        }, {
            field: 'reserve_date',
            title: '预约日期',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
            sortable: true,                  // 当前列进行排序
        }, {
            field: 'time_interval',
            title: '时段',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
        }, {
            field: 'remarks',
            title: '备注',
            align: 'center',                 // 水平居中显示
            valign: 'middle',                // 垂直居中显示
        }]
    });

    $('#btn_add').click(clickBtnAddFunc);        // 新增按钮的点击事件
    $('#btn_edit').click(clickBtnEditFunc);      // 修改按钮的点击事件
    $('#btn_delete').click(clickBtnDeleteFunc);  // 删除按钮的点击事件

    // $('#table_reserve').bootstrapTable()

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
    }

    window.location.href = "/reserve/reserve_edit?id="+lstData[0].id;   // 将选中数据的ID通过url传入后台
}