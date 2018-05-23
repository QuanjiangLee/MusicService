function dialogAlert(title, content) {
    $(".Dialog").remove()
    var html = ''
    html += '<div class="Dialog"><div class="modal-backdrop fade in" style="z-index: 1040;"></div>';
    html += '<div class="modal bootstrap-dialog type-warning fade size-normal in" role="dialog" aria-hidden="true" tabindex="-1" style="z-index: 1050;display: block;text-align: center;">';
    html += '<div class="modal-dialog"><div class="modal-content">';
    html += '<div class="modal-header"><div class="bootstrap-dialog-header">';
    html += '<button type="button" class="close" data-dismiss="modal" aria-hidden="true" onclick="closeDialog(this)">&times;</button>'
    html += '<div class="bootstrap-dialog-title" style="text-align: center;">' + title + '</div></div></div><div class="modal-body"><div class="bootstrap-dialog-body">';
    html += '<div class="bootstrap-dialog-message">';
    html += content;
    html += '</div></div></div></div></div></div></div>';
    $("body").append(html);
}

function userLogin() {
    var html = ''
    html += '用户ID:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="text" placeholder="请输入用户ID" name="username"><br>'
    html += '密&emsp;码:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="password" placeholder="请输入密码" name="password"><br>'
    html += '<input style="margin: 10px;" type="button" onclick="checkLogin()" class="sign-in-button btn btn-info" name="submit" value="登录"><input style="margin: 10px;" type="button" onclick="userRegister()" class="sign-in-button btn btn-info" name="regsiter" value="注册">'
    html += '<div class="rightTips"><a href="javascript:void(0);">忘记密码？</a></div></div>'
    title = '登录';
    dialogAlert(title, html);
}

function userRegister() {
    var html = ''
    html += '&emsp;用户ID:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="text" placeholder="输入注册用户ID" name="username"><br>'
    html += '&emsp;&emsp;密码:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="password" box-shadow: none;border - radius: 2px;padding: 6px 10px;" placeholder="输入注册密码" name="password"><br>'
    html += '重复密码:<input style="height: 35px;margin: 10px;box-shadow: none;border: 1px solid #e5e5e5;border-radius: 2px;padding: 6px 10px;" type="password" box-shadow: none;border - radius: 2px;padding: 6px 10px;" placeholder="重复注册密码" name="repassword"><br>'
    html += '<input style="margin: 10px;" type="button" onclick="registerUser(this)" class="sign-in-button btn btn-info" name="submit" value="注册">'
    html += '<div class="rightTips" onclick="userLogin()"><a href="javascript:void(0);">返回登录？</a></div></div>'
    title = '注册';
    dialogAlert(title, html);
}

function closeDialog(elem) {
    $(elem).parents(".Dialog").remove();
}

function checkData_form() {  //检查form表单数据的合法性
    var index = true;
    var username = $("input[name='username']").val();
    var password = $("input[name='password']").val();
    var repassword = $("input[name='repassword']");
    $("input").css("border-color", "#ddd");
    if (username == "") {
        index = false;
        $("input[name='username']").css("border-color", "#f33");
    }
    if (password == "") {
        index = false;
        $("input[name='password']").css("border-color", "#f33");
    }
    if (repassword.length != 0) {
        if (repassword.val() == "") {
            index = false
            $("input[name='repassword']").css("border-color", "#f33");
        }
    }
    return index
}
function checkLogin() {
    var verifyInput = checkData_form();
    if (verifyInput == true) {
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        data = { 'userNo': username, 'passwd': password }
        postRequest("/verifyLogin/", data, true, verifyResult);
    } else {
        alert("要登录的用户名或密码不能为空!")
    }
}
function verifyResult(ret) {
    if (ret['result'] == true) {
        if (ret['user_grant'] == 0) {
            window.location.href = "/userIndex/home";
        } else {
            window.location.href = "/adminIndex/";
        }
    } else {
        alert(ret['error']);
    }

}

function registerUser(elem) {
    var verifyInput = checkData_form();
    if (verifyInput == true) {
        var username = $("input[name='username']").val();
        var password = $("input[name='password']").val();
        var repassword = $("input[name='repassword']").val();
        if (password != repassword) {
            alert("两次输入的密码不一样，请重新输入!")
        } else {
            data = { 'userNo': username, 'passwd': password }
            postRequest("/registerUser/", data, true, registerResult);
        }
    } else {
        alert("要注册的用户名或密码不能为空!")
    }
}

function registerResult(ret) {
    if (ret['ret'] == true) {
        alert("恭喜注册新用户成功！")
        userLogin();
    } else {
        alert("opps!注册新用户失败！")
    }
}


function orderReset() {
    $("textarea[name='order-details']").val('');
}
function orderSubmit() {
    var song_id = $('#song-id').text();
    var share_details = $("textarea[name='order-details']").val();
    var share_to = []
    var users = $(".selected").each(function () {
        if ($(this).children("a").attr("aria-selected") == "true") {
            share_to.push($(this).find("span").text())
        }
    });
    /*alert(song_id)
    alert(share_to)
    alert(share_details)*/
    if (share_to.length < 1) {
        alert("请至少选择一个分享人员！")
    } else {
        data = { 'song_id': song_id, 'share_to': share_to, 'share_details': share_details };
        postRequest("/share_song/", data, true, addOrderResult);
    }
}
function addOrderResult(ret) {
    if (ret == true) {
        $(".Dialog").remove();
        alert("恭喜您分享成功！");
    } else {
        alert("分享失败，请稍后重试！")
    }
}

function song_lyric(elem) {
    var song_id = $(elem).parent().attr("song-id")
    postRequest("/song_lyric/", { 'song_id': song_id }, true, lyricResult);
}

function lyricResult(ret) {
    if (ret) {
        var title = ret['song_name'] + " 的歌词"
        var html = "<p>"+ret['song_lyric']+"</p>"
        dialogAlert(title, html);
    } else {
        alert("歌词获取错误，请稍候重试！");
    }
}

function song_liked(elem) {
    var song_id = $(elem).parent().attr("song-id");
    data = { 'song_id': song_id };
    postRequest("/song_liked/", data, true, likedResult);
}
function likedResult(params) {
    if (params == true) {
        $(".Dialog").remove();
        alert("恭喜您收藏歌曲成功！");
    } else {
        alert("收藏失败，请稍后重试！")
    }
}

function song_share(elem) {
    var html = ""
    var song_id = $(elem).parents(".action").attr('song-id')
    var song_name = $(elem).parents(".entry").find(".artist").attr("title")
    html += "<h3>您想要分享的歌曲是：<span id='song-name'>" + song_name + "</span></h3>";
    html += "<h5>想要分享给：</h5>";
    var commitInfo = httpGet("/share_html/");
    html += commitInfo;
    html += "<span id='song-id' style='display:none;'>" + song_id + "</span>";
    var title = "分享歌曲给其他人"
    dialogAlert(title, html);
    $(".bootstrap-dialog-message").css("height", "500px");
    $(".bootstrap-dialog-message").css("overflow", "scroll");
    $(".bootstrap-dialog-message").css("text-align", "left");
}

function song_unliked(elem) {
    var like_id = $(elem).attr("like-id")
    postRequest("/song_unliked/", { 'like_id': like_id }, true, unlikedResult);
}
function unlikedResult(ret) {
    if (ret == true) {
        alert("取消收藏歌曲成功！");
        location.reload();
    } else {
        alert("取消收藏歌曲失败，请稍后重试！")
    }
}

function del_shared(elem) {
    var share_id = $(elem).attr("share-id")
    postRequest("/del_shared/", { 'share_id': share_id }, true, delSharedResult);
}
function delSharedResult(ret) {
    if (ret == true) {
        alert("删除被分享的歌曲成功！");
        location.reload();
    } else {
        alert("删除被分享的歌曲失败，请稍后重试！")
    }
}