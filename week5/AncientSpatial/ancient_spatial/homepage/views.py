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
        useApplication: Literal['ancient', 'parallel'] = request.POST.get("useApplication")
        if useApplication == 'ancient':
            return redirect(reverse("spatialquery:spatialqueryres", args=(text_input, queryrange)))
        elif useApplication == 'parallel':
            pass
        # return HttpResponse("text_input: %s, queryrange: %s, useApplication: %s" % (text_input, queryrange, useApplication))
    return HttpResponse("功能尚未开发，敬请期待……")