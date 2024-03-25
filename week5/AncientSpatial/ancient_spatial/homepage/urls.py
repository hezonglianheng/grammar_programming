# encoding: utf8
# usage: 设置路径信息

from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path("", views.default, name='default'), 
    # 查询界面
    path("query", views.query, name='query'),
]
