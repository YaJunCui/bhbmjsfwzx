$(function(){           // 动态修改预约信息时段的值
    var flag = $('#time_interval').attr('flag');
    if(flag) {
        $('#time_interval').find('option[value="'+flag+'"]').attr('selected', 'selected');   
    }
});