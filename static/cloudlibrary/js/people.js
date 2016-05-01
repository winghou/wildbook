/**
 * Created by bovenson on 4/30/16.
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
var modal_windows = $('#modal_windows');
var modal_windows_msg = $('#modal_windows_msg');
var button_modal_confirm = $('#button_modal_confirm');
var modal_windows_alert = $('#modal_windows_alert');
var modal_windows_alert_msg = $('#modal_windows_alert_msg');
// 得到模态窗口 end

// 删除书籍
function delete_book(obj) {
    var book_name = obj.getAttribute("name");
    modal_windows_msg.text("确定要下架 " + book_name + " 吗?");
    modal_windows_msg.val(obj.id);
    modal_windows.modal("show");
}
button_modal_confirm.click(function () {
    modal_windows.modal("hide");
    var book_id = modal_windows_msg.val();
    $.post("/delete_book", {
        id: book_id
    }, function(data){
        if (data["res"] == "error") {
            alert(data["msg"]);
        } else {
            $("div[id=" + book_id + "]").hide();
            $("div[id=clearfix" + book_id + "]").hide();
        }
    }, 'json');
});

$(document).ready(function () {

    // 得到几个输入框
    var input_nickname = $('#input_nickname');
    var input_qq = $('#input_qq');
    var input_tel = $('#input_tel');
    var input_weixin = $('#input_weixin');

    // nickname
    var a_edit_nickname = $('#a_edit_nickname');
    var button_confirm_nickname = $('#button_confirm_nickname');
    var div_show_nickname = $('#div_show_nickname');
    var div_edit_nickname = $('#div_edit_nickname');
    // 如果没有昵称, 文字改为 编辑昵称
    if (a_edit_nickname.text().trim() == "") {
        a_edit_nickname.text("编辑昵称");
    } else {
        input_nickname.val(a_edit_nickname.text());
    }
    a_edit_nickname.click(function () {
        div_show_nickname.hide();
        div_edit_nickname.show();
    });
    button_confirm_nickname.click(function () {
        div_show_nickname.show();
        div_edit_nickname.hide();
        a_edit_nickname.text(input_nickname.val());
        update_people_info();
    });

    // 微信
    // 显示/隐藏
    var a_edit_weixin = $('#a_edit_weixin');
    var button_confirm_weixin = $('#button_confirm_weixin');
    var div_show_weixin = $('#div_show_weixin');
    var div_edit_weixin = $('#div_edit_weixin');
    if (a_edit_weixin.text().trim() == "") {
        a_edit_weixin.text("编辑微信");
    } else {
        input_weixin.val(a_edit_weixin.text());
    }
    a_edit_weixin.click(function () {
        div_show_weixin.hide();
        div_edit_weixin.show();
    });
    button_confirm_weixin.click(function () {
        div_show_weixin.show();
        div_edit_weixin.hide();
        a_edit_weixin.text(input_weixin.val());
        update_people_info();
    });


    // qq
    var a_edit_qq = $('#a_edit_qq');
    var button_confirm_qq = $('#button_confirm_qq');
    var div_show_qq = $('#div_show_qq');
    var div_edit_qq = $('#div_edit_qq');
    if (a_edit_qq.text().trim() == "") {
        a_edit_qq.text("编辑QQ");
    } else {
        input_qq.val(a_edit_qq.text());
    }
    a_edit_qq.click(function () {
        div_show_qq.hide();
        div_edit_qq.show();
    });
    button_confirm_qq.click(function () {
        div_show_qq.show();
        div_edit_qq.hide();
        a_edit_qq.text(input_qq.val());
        update_people_info();
    });

    // tel
    var a_edit_tel = $('#a_edit_tel');
    var button_confirm_tel = $('#button_confirm_tel');
    var div_show_tel = $('#div_show_tel');
    var div_edit_tel = $('#div_edit_tel');
    if (a_edit_tel.text().trim() == "") {
        a_edit_tel.text("编辑电话");
    } else {
        input_tel.val(a_edit_tel.text());
    }
    a_edit_tel.click(function () {
        div_show_tel.hide();
        div_edit_tel.show();
    });
    button_confirm_tel.click(function () {
        div_show_tel.show();
        div_edit_tel.hide();
        a_edit_tel.text(input_tel.val());
        update_people_info();
    });

    function update_people_info() {
        var new_nickname = a_edit_nickname.text();
        var new_weixin = a_edit_weixin.text();
        var new_qq = a_edit_qq.text();
        var new_tel = a_edit_tel.text();

        if (new_weixin == "编辑微信") {
            new_weixin = ""
        }
        if (new_qq == "编辑QQ") {
            new_qq = ""
        }
        if (new_tel == "编辑电话") {
            new_tel = ""
        }
        if (new_nickname == "编辑昵称") {
            new_nickname = ""
        }

        var cont_data = {
            weixin: new_weixin,
            qq: new_qq,
            nickname: new_nickname,
            tel: new_tel
        };
        $.post("/edit_person", cont_data, function(data) {
            if (data["res"] == "error") {
                modal_windows_alert_msg.text(data["msg"]);
                modal_windows_alert.modal("show");
            }

            // 更新用户信息
            if (data["nickname"]==null || data["nickname"].trim()=="") {
                a_edit_nickname.text("编辑昵称");
            } else {
                a_edit_nickname.text(data["nickname"]);
            }
            input_nickname.val(data["nickname"]);

            if (data["weixin"]==null || data["weixin"].trim()=="") {
                a_edit_weixin.text("编辑微信");
            } else {
                a_edit_weixin.text(data["weixin"]);
            }
            input_weixin.val(data["weixin"]);

            if (data["qq"]==null || data["qq"].trim()=="") {
                a_edit_qq.text("编辑QQ");
            } else {
                a_edit_qq.text(data["qq"]);
            }
            input_qq.val(data["qq"]);

            if (data["tel"]==null || data["tel"].trim()=="") {
                a_edit_tel.text("编辑电话");
            } else {
                a_edit_tel.text(data["tel"]);
            }
            input_tel.val(data["tel"]);
        }, 'json');
    }
});
