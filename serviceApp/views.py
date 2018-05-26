import os
import json
import time
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.shortcuts import render, redirect
from datetime import datetime
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from serviceApp.models import *
from serviceApp.apps import *

# Create your views here.

#登录html返回
def login(request):
    return render(request, 'login.html')

#登录验证函数
@csrf_exempt
def verifyLogin(request):
    if request.method == "GET":
        userNo = request.GET.get("userNo","")
        passwd = request.GET.get("passwd","")
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        userNo = data['userNo']
        passwd = data['passwd']
    print('userNo',userNo)
    print('passwd',passwd)
    user = userInf.objects.filter(user_name=userNo, user_passwd=passwd)
    print('user is', user)
    if user:
        user_grant = 0
        request.session["login_user"] = userNo
        request.session["user_grant"] = user_grant
        sessionId=request.session.session_key 
        print('sessionId is ',sessionId)
        print('user_grant is',user_grant)
        response = {'result':True, 'sessionId':sessionId, 'user_grant':user_grant}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')
    else:
        response = {'result':False, 'error': "用户名或密码不正确!"}
        return HttpResponse(json.dumps(response), content_type='application/json;charset=utf-8')


#用户注销
@csrf_exempt
def userLoginOut(request):
    try:
        del request.session['login_user']
        del request.session['user_grant']
    except KeyError:
        pass
    return HttpResponse(json.dumps({'ret':True}), content_type='application/json;charset=utf-8')

#用户主页函数
def index(request):
    if is_logined(request) is False:
        #cusInfo = {'hello':'unknow', "user_grant":"custom"}
        return redirect('/index/home/')
        #return render(request, 'index.html',{'cusInfo':cusInfo})
    if is_logined(request) == 'user':
        #userInfo = {'hello':'user',"user_grant":'user'}
        return redirect('/userIndex/home/')

def home(request):
    user_grant = get_user_grant(request)
    if user_grant == "user":
        return render(request, 'home.html',{'extend': 'userIndex.html'})
    else:
        return redirect('/index/home/')

def index_home(request):
    return render(request, 'home.html',{'extend': 'index.html'})

#注册用户函数
@csrf_exempt
def registerUser(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    try:
        userNo = data['userNo']
        passwd = data['passwd']
        print(userNo, passwd)
        ret = userInf.objects.filter(user_name=userNo)
        if ret:
            return HttpResponse(json.dumps({'ret':'registered'}), content_type='application/json;charset=utf-8')
        else:
            ret = userInf.objects.create(user_name=userNo, user_nickname="小乐", user_passwd=passwd)
            if ret:
                return HttpResponse(json.dumps({'ret':True}), content_type='application/json;c:harset=utf-8')
            else:
                return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps({'ret':False}), content_type='application/json;charset=utf-8')


#关于页面返回
def about(request):
    user_grant = get_user_grant(request)
    if user_grant == "custom":
        return render(request, 'about.html',{'extend': 'index.html'})
    elif user_grant == "user":
        return render(request, 'about.html',{'extend': 'userIndex.html'})
    else:
        return redirect('/index/home/')  

#获取当前登录用户名
@csrf_exempt
def get_login_user(request):
    login_user = request.session.get('login_user',None)
    #login_user = userInf.objects.get(user_name=cur_user).user_nickname
    if login_user:
        return HttpResponse(json.dumps({"login_user": login_user}), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps({"login_user": None}), content_type='application/json;charset=utf-8')

#获取热曲排行列表信息
def songs_list(request):
    user_grant = get_user_grant(request)
    print(user_grant)
    items = []
    songs = songsInf.objects.all()
    for song in songs:
        items.append([song])
    if user_grant == "custom":
        return render(request, 'songs_list.html',{'extend': 'index.html','items':items,'list_type':'all','user_grant':user_grant})
    elif user_grant == "user":
        return render(request, 'songs_list.html',{'extend': 'userIndex.html','items':items,'list_type':'all', 'user_grant':user_grant})
    else:
        return redirect('/index/home/')

#获取收藏歌曲列表信息
def get_songs_liked(request):
    user_grant = get_user_grant(request)
    login_user=request.session.get('login_user',None)
    user = userInf.objects.get(user_name=login_user)
    items = []
    like_songs = songLikes.objects.filter(like_user=user)
    for like in like_songs:
        items.append([like.like_song,like])
    if user_grant == "user":
        return render(request, 'songs_list.html',{'extend': 'userIndex.html','items':items,'list_type':'liked', 'user_grant':user_grant})
    else:
        return redirect('/index/home/')


#歌曲收藏函数
@csrf_exempt
def song_liked(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        song_id = data['song_id']
        login_user=request.session.get('login_user',None)
        song = songsInf.objects.get(song_id=song_id)
        user = userInf.objects.get(user_name=login_user)
        ret = songLikes.objects.filter(like_user=user, like_song=song)
        if ret:
            return HttpResponse(json.dumps("liked"), content_type='application/json;charset=utf-8')
        else:
            ret = songLikes.objects.create(like_user=user, like_song=song)
            if ret:
                return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')
            else:
                return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')

#取消歌曲收藏函数
@csrf_exempt
def song_unliked(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        like_id = data['like_id']
        ret = songLikes.objects.filter(like_id=like_id).delete()
        if ret:
            return HttpResponse(json.dumps(True), content_type='application/json;c:harset=utf-8')
        else:
            return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')

#获取好友分享的歌曲列表信息
def get_songs_shared(request):
    user_grant = get_user_grant(request)
    login_user=request.session.get('login_user',None)
    user_to = userInf.objects.get(user_name=login_user)
    items = []
    share_songs = songShare.objects.filter(share_to=user_to)
    for song in share_songs:
        items.append([song,song.share_song])
    print(items)
    if user_grant == "user":
        return render(request, 'shared_html.html',{'extend': 'userIndex.html','items':items, 'user_grant':user_grant})
    else:
        return redirect('/index/home/')

#获取可分享的用户列表
def share_html(request):
    login_user=request.session.get('login_user',None)
    userlist = userInf.objects.filter(~Q(user_name=login_user))
    print(userlist)
    return render(request, 'share_form.html', {'userlist': userlist})

#分享歌曲给别人函数
@csrf_exempt
def share_song(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        song_id = data['song_id']
        share_users = data['share_to']
        share_details = data['share_details']
        login_user=request.session.get('login_user',None)
        share_from = userInf.objects.get(user_name=login_user)
        share_song = songsInf.objects.get(song_id=int(song_id))
        for user in share_users:
            try:
                share_to = userInf.objects.get(user_name=user)
                songShare.objects.create(share_from=share_from, share_to=share_to,share_song=share_song, share_commit= share_details)
            except Exception as err:
                return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')


#删除某条歌曲分享信息
@csrf_exempt
def del_shared(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        share_id = data['share_id']
        ret = songShare.objects.filter(share_id=share_id).delete()
        if ret:
            return HttpResponse(json.dumps(True), content_type='application/json;c:harset=utf-8')
        else:
            return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')


#获取某首歌曲的歌词信息
@csrf_exempt
def song_lyric(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        song_id = data['song_id']
        ret = songsInf.objects.filter(song_id=song_id)
        if ret:
            print(ret[0].song_lyric)
            return HttpResponse(json.dumps({'song_name':ret[0].song_name, 'song_lyric':ret[0].song_lyric}), content_type='application/json;c:harset=utf-8')
        else:
            return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    except Exception as err:
        print(str(err))
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')

#获取某首歌曲的评论信息
def get_songCommit(request):
    user_grant = get_user_grant(request)
    login_user=request.session.get('login_user',None)
    user_to = userInf.objects.get(user_name=login_user)
    if request.method == "GET":
        song_id = request.GET.get('song_id',"")
        print(song_id)
    if song_id:
        song = songsInf.objects.get(song_id=song_id)
        print(song)
        commits = songCommit.objects.filter(commit_song=song)
        print(commits)
    if user_grant == "user":
        return render(request, 'commit_html.html',{'extend': 'userIndex.html','commits':commits, 'user_grant':user_grant})
    else:
        return render(request, 'commit_html.html',{'extend': 'index.html','commits':commits, 'user_grant':user_grant})


#歌曲评论功能函数
@csrf_exempt
def commit_song(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
    else:
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    try:
        song_id = data['song_id']
        commit_details = data['commit_details']
        song = songsInf.objects.get(song_id=song_id)
        login_user=request.session.get('login_user',None)
        commit_from = userInf.objects.get(user_name=login_user)
        songCommit.objects.create(commit_song=song, commit_user = commit_from, commit_details=commit_details)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps(False), content_type='application/json;charset=utf-8')
    else:
        return HttpResponse(json.dumps(True), content_type='application/json;charset=utf-8')