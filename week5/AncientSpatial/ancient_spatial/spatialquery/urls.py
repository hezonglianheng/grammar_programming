# encoding: utf8
# usage: 设置路径信息

from django.urls import path

from . import views

app_name = "spatialquery" # 添加应用名称
urlpatterns = [
    # 查询结果页面
    path("res/<str:text_input>/<str:queryrange>/<str:semanticrange>/<str:querymode>", views.res, name="spatialqueryres"),
    # 查询详情页面
    path("resdetail/<int:space_id>/", views.detail, name="resdetail"),
]