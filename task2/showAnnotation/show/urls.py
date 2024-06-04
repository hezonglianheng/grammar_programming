# encoding: utf8
from django.urls import path
from . import views

app_name = 'show'
urlpatterns = [
    # path("", views.default, name='default'),
    # 默认展示页面，展示所有替换对类型
    path("", views.show_rp_pairs, name='show_rp_pairs'),
    # 展示某一替换对下所有句子
    path("sentences/<str:rp_pair>/", views.show_sentences, name='show_sentences'),
]
