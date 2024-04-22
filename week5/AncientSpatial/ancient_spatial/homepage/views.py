from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from typing import Literal

# Create your views here.

def default(request):
    """默认的主页的页面"""
    return render(request, "homepage/default.html")

def query(request):
    """接收查询结果的页面"""
    if request.method == "POST":
        text_input = request.POST.get("text_input")
        queryrange = request.POST.get("queryrange")
        semanticrange = request.POST.get("semanticrange") # 添加属性语义范围
        useApplication: Literal['ancient', 'parallel', 'pattern'] = request.POST.get("useApplication")
        if useApplication == 'ancient':
            # 跳转到古代查询的页面
            return redirect(reverse("spatialquery:spatialqueryres", args=(text_input, queryrange, semanticrange)))
        elif useApplication == 'parallel':
            # 跳转到双语对齐语料查询的页面
            pass
        elif useApplication == 'pattern':
            # 跳转到模式查询的页面
            return redirect(reverse("patternquery:queryres", args=(text_input, semanticrange)))
        # return HttpResponse("text_input: %s, queryrange: %s, useApplication: %s" % (text_input, queryrange, useApplication))
    return HttpResponse("功能尚未开发，敬请期待……")