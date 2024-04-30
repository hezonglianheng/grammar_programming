from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.db.models import Q # 用于组合查询条件
from django.template import loader # 加载模板
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # 用于分页

from functools import reduce

from .models import OriginalText, TextInfo, SpaceInfo
from homepage.views import QMODE
from config import RELATION_CHINESE

# 查询范围与关键字对应的字典
range_key = {
    'trajectory': ['trajectory1', 'trajectory2'],
    'landmark': ['landmark'],
    'event': ['event'],
    'preposition': ['preposition'],
    'location': ['location'],
}
# 语义范围列名
semantic_name = 'spatial_type'
# 语义范围与关键字对应的字典
semantic_key = {
    'place': ['isPlace'],
    'departure': ['isDeparture'],
    'destination': ['isDestination'],
    'orientation': ['isOrientation'],
    'direction': ['isDirection'],
    'path': ['isPath'],
    'part': ['isPart'],
}
SHOW_RANGE: int = 30
PAGE_SIZE: int = 30

# 修改：在原有的query函数中添加了对语义范围的处理
def res(request, text_input: str, queryrange: str, semanticrange: str, querymode: QMODE):
    def judge_in(text: str) -> bool:
        # 备用：模糊查询与精确查询
        if querymode == 'fuzzy':
            return text_input in text
        elif querymode == 'accurate':
            return text == text_input
        else:
            return False

    qkeys: list[str] = []
    # 若查询范围为all，则查询所有的关键字
    if queryrange == 'all':
        # 修改：使用reduce重构列表
        qkeys = reduce(lambda x, y: x + y, [i for i in range_key.values()])
    # 否则查询指定范围的关键字
    else:
        qkeys = range_key[queryrange]
    
    # 备用：模糊查询与精确查询
    if querymode == 'fuzzy':
        vague_qkeys = [i + "__text__contains" for i in qkeys]
    elif querymode == 'accurate':
        vague_qkeys = [i + "__text" for i in qkeys]
    else:
        return render(request, "spatialquery/noresults.html")
    
    # 合并全部查询条件
    qs = [Q(**{key: text_input}) for key in vague_qkeys]
    q = reduce(lambda x, y: x | y, qs)
    results = SpaceInfo.objects.filter(q)

    # 通过语义范围再次过滤查询结果
    if semanticrange == 'all':
        pass
    elif semanticrange in semantic_key:
        results = results.filter(spatial_type=semantic_key[semanticrange][0])
    else:
        return render(request, "spatialquery/noresults.html")

    print(len(results))
    if len(results) == 0:
        # 没有结果返回特定页面
        return render(request, "spatialquery/noresults.html")
    else:
        # 计算切片长度等信息构成条目
        # todo: 找出bug并优化速度
        aitems: list[list[SpaceInfo, str, str, str]] = []
        for i in results:
            for k in qkeys:
                # 判断是否存在该关键字，再判断查询内容是否在文本内
                if getattr(i, k) and judge_in(getattr(i, k).text):
                    a: str = str(max(getattr(i, k).start-SHOW_RANGE, 0))
                    b: str = str(getattr(i, k).start)
                    c: str = str(getattr(i, k).end)
                    d: str = str(min(getattr(i, k).end+SHOW_RANGE, len(i.source.context)))
                    aitems.append([i, f"{a}:{b}", f"{b}:{c}", f"{c}:{d}"])
                    break
        # 加入分页逻辑
        paginator = Paginator(aitems, PAGE_SIZE)

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
        return render(request, "spatialquery/getresults.html", {"items": items, "page_num": paginator.num_pages, "page_sum": len(aitems), "page_start": items.start_index(), "page_end": items.end_index()})

def detail(request, space_id):
    """显示某条空间信息的详细信息

    Args:
        request: 访问请求，由Django自动传入
        space_id: 语料的id

    Returns:
        返回请求具体信息的页面
    """    """"""
    space = get_object_or_404(SpaceInfo, pk=space_id)
    # 空间角色关键字
    spatial_keys = reduce(lambda x, y: x + y, [i for i in range_key.values()])
    # 空间角色值
    spatial_values: list[TextInfo|None] = [getattr(space, i) for i in spatial_keys]
    # 求取字符串
    spatial_string_dict = {k:s for k, s in zip(spatial_keys, [i.text if i else '' for i in spatial_values])}
    spatial_string_dict |= {"semantic": RELATION_CHINESE[space.spatial_type] if space.spatial_type else '未知'} # 添加语义关系
    # 求取非空索引值
    index_not_none = [(i.start, i.end) for i in [k for k in spatial_values if k]]
    index_not_none = list(set(index_not_none)) # 去重
    index_not_none.sort(key=lambda x: x[0]) # 排序
    # 求取索引值
    index = [(f"0:{index_not_none[0][0]}", False)]
    for i in range(len(index_not_none)):
        index.append((f"{index_not_none[i][0]}:{index_not_none[i][1]}", True))
        if i < len(index_not_none)-1:
            index.append((f"{index_not_none[i][1]}:{index_not_none[i+1][0]}", False))
    index.append((f"{index_not_none[-1][1]}:{len(space.source.context)}", False))
    # index = list(set(index)) # 去重
    return render(request, "spatialquery/detail.html", {"space": space, "spatial_string": spatial_string_dict, "index": index})