"""MusicService URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from serviceApp import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^registerUser/', views.registerUser),
	url(r'^verifyLogin/', views.verifyLogin),
	url(r'^userLoginOut/', views.userLoginOut),
	url(r'^index/$', views.index),
    url(r'^userIndex/$', views.index),
    url(r'^index/home/$', views.index_home),
    url(r'^userIndex/home/$', views.home),
    url(r'^index/songs_list/$', views.songs_list),
    url(r'^userIndex/songs_list/$', views.songs_list),
    url(r'^userIndex/get_songs_liked/$', views.get_songs_liked),
    url(r'^userIndex/get_songs_shared/$', views.get_songs_shared),
    url(r'^get_songCommit/$', views.get_songCommit),
    url(r'^song_unliked/$', views.song_unliked),
    url(r'^song_liked/$', views.song_liked),
    url(r'^share_song/$', views.share_song),
    url(r'^del_shared/$', views.del_shared),
    url(r'^song_lyric/$', views.song_lyric),
    url(r'^commit_song/', views.commit_song),
    url(r'^share_html/$', views.share_html),
    url(r'^get_login_user/$', views.get_login_user),
    url(r'^index/about/$', views.about),
    url(r'^userIndex/about/$', views.about),
]
