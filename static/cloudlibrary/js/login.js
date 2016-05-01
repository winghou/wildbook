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
    var login_model = $('#login_model');
    var login_model_msg = $('#login_model_msg');
    // 得到模态窗口 end

    // 处理登陆
    $('#button_login_confirm').click(function () {
        var username = $("#input_login_username").val();
        var password = $("#input_login_password").val();
        if (username.trim() == "") {
            login_model_msg.text("请输入账号");
            login_model.modal("show");
            return false;
        }
        if (password.trim() == "") {
            login_model_msg.text("请输入密码");
            login_model.modal("show");
            return false;
        }

        $.post("/deal_login_register",{
            username: username,
            password: password,
            action: "login"
        }, function(data) {
            if (data['res']=='success') {
            // login_model_msg.text("认证成功");
            // login_model.modal("show");
                location.href = "/index";
            }
            else {
            login_model_msg.text(data["msg"]);
            login_model.modal("show");
            }
        }).error(function() {
            login_model_msg.text("网络超时,稍等重试,您可以尝试刷新页面");
            login_model.modal("show");
        });
    });
    // 处理登陆 end

    // 处理注册
    $('#button_register_confirm').click(function () {
        var username = $("#input_register_username").val();
        var password = $("#input_register_password").val();
        var password_repeat = $("#input_register_password_repeat").val();
        if (username.trim() == "") {
            login_model_msg.text("请输入账号");
            login_model.modal("show");
            return false;
        }
        if (password == "") {
            login_model_msg.text("请输入密码");
            login_model.modal("show");
            return false;
        }
        if (password_repeat == "") {
            login_model_msg.text("请再次输入密码");
            login_model.modal("show");
            return false;
        }
        if (password != password_repeat) {
            login_model_msg.text("两次输入密码不同, 请确认您的密码");
            login_model.modal("show");
            return false;
        }

        $.post("/deal_login_register",{
            username: username,
            password: password,
            action: "register"
        }, function(data) {
            if (data["res"]=='success') {
            // login_model_msg.text("注册成功");
            // login_model.modal("show");
                location.href = "/index"
            } else {
                login_model_msg.text(data["msg"]);
                login_model.modal("show");
            }
        }).error(function() {
                login_model_msg.text("网络超时,稍等重试,您可以尝试刷新页面");
                login_model.modal("show");
        });
    });
    // 处理注册 end

    // 设置登录注册字体颜色
    var color_activate = "#4B4641";
    var color_deactivate = "#ADADAD";
    var a_login = $('#a_login');
    var a_register = $('#a_register');
    a_login.css("color", color_activate);
    a_register.css("color", color_deactivate);

    a_login.click(function () {
        $('#div_register').hide();
        $('#div_login').show();
        $('#a_login').css("color", color_activate);
        $('#a_register').css("color", color_deactivate);
    });
    a_register.click(function () {
        $('#div_login').hide();
        $('#div_register').show();
        $('#a_login').css("color", color_deactivate);
        $('#a_register').css("color", color_activate);
    });
    // end
});
