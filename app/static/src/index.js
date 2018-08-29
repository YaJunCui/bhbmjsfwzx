$(function(){
    $('#table_index').bootstrapTable({
        url:'/index/total_data',         // 获取表格数据的url
        data: get_index_data(),
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