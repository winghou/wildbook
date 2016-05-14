$(document).ready(function () {
    // 跨域请求保护
     var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    // 得到模态窗口
    var modal_windows_feedback = $('#modal_windows_feedback');
    var modal_windows_feedback_input = $('#modal_windows_feedback_input');

    // 如果点击反馈
    var a_feedback = $('#a_feedback');
    a_feedback.click(function () {
        modal_windows_feedback.modal("show");
    });
    // 点击确定反馈
    var modal_windows_feedback_confirm = $('#modal_windows_feedback_confirm');
    modal_windows_feedback_confirm.click(function () {
        $.post('/feedback/', {
            "feedback": modal_windows_feedback_input.val()
        }, function (data) {
        }, 'json');
        modal_windows_feedback.modal("hide");
    });

});