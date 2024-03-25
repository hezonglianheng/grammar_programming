from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.db.models import Q # 用于组合查询条件
from django.template import loader # 加载模板
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # 用于分页

from functools import reduce

from .models import OriginalText, TextInfo, SpaceInfo

# 查询范围与关键字对应的字典
range_key = {
    'trajectory': ['trajectory1', 'trajectory2'],
    'landmark': ['landmark'],
    'event': ['event'],
    'preposition': ['preposition'],
    'location': ['location'],
}
SHOW_RANGE: int = 30
PAGE_SIZE: int = 30

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def res(request, text_input, queryrange):
    def judge_in(text: str) -> bool:
        # 备用：模糊查询与精确查询
        if True:
            return text in text_input
        else:
            return text == text_input

    qkeys: list[str] = []
    # 若查询范围为all，则查询所有的关键字
    if queryrange == 'all':
        for key in range_key:
            qkeys.extend(range_key[key])
    # 否则查询指定范围的关键字
    else:
        qkeys = range_key[queryrange]
    
    # 备用：模糊查询与精确查询
    if True:
        vague_qkeys = [i + "__text__contains" for i in qkeys]
    else:
        pass
    
    # 合并全部查询条件
    qs = [Q(**{key: text_input}) for key in vague_qkeys]
    q = reduce(lambda x, y: x | y, qs)
    results = SpaceInfo.objects.filter(q)
    # Do something with the results

    if len(results) == 0:
        # 没有结果返回特定页面
        return render(request, "spatialquery/noresults.html")
    else:
        # 计算切片长度等信息构成条目
        items: list[list[SpaceInfo, str, str, str]] = []
        for i in results:
            for k in qkeys:
                if judge_in(getattr(i, k).text):
                    a: str = str(max(getattr(i, k).start-SHOW_RANGE, 0))
                    b: str = str(getattr(i, k).start)
                    c: str = str(getattr(i, k).end)
                    d: str = str(min(getattr(i, k).end+SHOW_RANGE, len(i.source.context)))
                    items.append([i, f"{a}:{b}", f"{b}:{c}", f"{c}:{d}"])
                    # break
        # 加入分页逻辑
        paginator = Paginator(items, PAGE_SIZE)

        try:
            # 获取当前页码
            page = request.GET.get('page')
            # 获取当前页的数据
            items = paginator.page(page)
        except PageNotAnInteger:
            # 如果页码不是整数，则返回第一页
            items = paginator.page(1)
        except EmptyPage:
            # 如果页码超出范围，则返回最后一页
            items = paginator.page(paginator.num_pages)
        # 返回查询结果
        return render(request, "spatialquery/getresults.html", {"items": items, "page_num": paginator.num_pages})


def detail(request, space_id):
    pass