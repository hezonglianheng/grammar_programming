# encoding: utf8
# usage: 设置路径信息

from django.urls import path

from . import views

app_name = "patternquery" # 添加应用名称
urlpatterns = [
    # 查询结果页面
    path("res/<str:pattern>/<str:semanticrange>/<str:querymode>", views.queryres, name="queryres"),
]