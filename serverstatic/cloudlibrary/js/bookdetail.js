/**
 * Created by bovenson on 5/3/16.
 */

var csrftoken = $.cookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
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
var modal_windows_close = $('#modal_windows_close');
var modal_windows_close_msg = $('#modal_windows_close_msg');
var modal_windows_go_login = $('#modal_windows_go_login');
var modal_windows_go_login_msg = $('#modal_windows_go_login_msg');

var text_leave_msg = $('#text_leave_msg');
var button_leave_msg = $('#button_leave_msg');
var label_user_id = $('#label_user_info');
$(document).ready(function () {
    button_leave_msg.click(function () {
        var reply_text = text_leave_msg.val();
        var book_id = button_leave_msg.val();
        var user_id = label_user_id.text();
        if (user_id == null || user_id == "" || user_id == "None") {
            modal_windows_go_login_msg.text("登录后才能留言");
            modal_windows_go_login.modal("show");
            return;
        }
        // 字数控制
        if (reply_text.length == 0) {
            modal_windows_close_msg.text("请输入留言内容");
            modal_windows_close.modal("show");
            return;
        } else if (reply_text.length > 120) {
            modal_windows_close_msg.text("您留言内容过长,请少于120字");
            modal_windows_close.modal("show");
            return;
        }
        // 向服务器POST回复
        var data_cont = {
            reply_text: reply_text,
            book_id: book_id
        };
        $.post("/book_reply", data_cont, function (data) {
            if (data["res"] != "success") {
                modal_windows_close_msg.text("留言时遇到问题:" + data["msg"]);
                modal_windows_close.modal("show");
            } else {
                // 添加回复
                location.reload();
            }
        }, 'json');
    });
});