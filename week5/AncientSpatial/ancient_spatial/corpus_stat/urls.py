from django.urls import path
from . import views

app_name = 'corpus_stat'
urlpatterns = [
    # 数据统计导航页
    path('', views.guide, name='guide'),
    # 数据统计页，用于接受查询信息，重定向到相应的查询结果页面
    path('query/', views.query, name='query'),
    # 空间语义数据统计页
    path('stat_semantic/', views.semantic, name='semantic'),
    # 介词数据统计页
    path('stat_prep/', views.prep, name='prep'),
    # 动词数据统计页
    path('stat_verb/', views.verb, name='verb'),
]