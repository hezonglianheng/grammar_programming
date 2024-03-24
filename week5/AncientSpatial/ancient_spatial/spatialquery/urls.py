# encoding: utf8
# usage: 设置路径信息

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="spatialquery"),
]