from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from django.db.models import Q # 用于组合查询条件
from django.template import loader # 加载模板
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # 用于分页
from functools import reduce
# 引入单语查询模型
from spatialquery.models import OriginalText, TextInfo, SpaceInfo
from config import PATTERN_DICT, PATTERN_JOIN, PATTERN2ROLE, TR1, MODE_CHINESE
from typing import Optional
from spatialquery.views import SHOW_RANGE, PAGE_SIZE, semantic_key, semantic_name
from homepage.views import QMODE

def expression_parse(exp: str) -> Optional[list[tuple[str, Optional[str]]]]:
    """解析模式查询表达式\n
    模式查询表达式的ebnf范式如下：
    Exp ::= Unit "+" Unit {"+" Unit}
    Unit ::= Role ["(" Word ")"]
    Role ::= "tr" | "lm" | "ev" | "pr" | "lo" 
    Word ::= ... # 任意汉字字符串"""
    
    exp = exp.strip()
    # 检查表达式是否包含连接符号，若不包含则返回None
    if PATTERN_JOIN not in exp:
        return None
    # 按照表达式连接符号分割表达式
    units = exp.split(PATTERN_JOIN)
    res: list[tuple[str, Optional[str]]] = []
    # 解析Word信息
    for unit in units:
        # 检查是否包含括号，若包含则解析括号内的Word信息
        if "(" in unit and unit[-1] == ")":
            role, word = unit.split("(")
            word = word[:-1]
        else:
            role, word = unit, None
        if role not in PATTERN_DICT.values():
            return None
        res.append((role, word))
    return res

def queryres(request, pattern: str, semanticrange: str, querymode: QMODE):

    def check_list_order(short_lst: list[str], long_lst: list[str]) -> bool:
        """检查短列表是否为长列表的子序列\n
        若短列表为空，则返回True\n
        若长列表为空，则返回False\n
        若短列表的第一个元素不在长列表中，则返回False\n
        否则递归检查短列表的剩余部分是否为长列表剩余部分的子序列"""
        if not short_lst:
            return True
        if not long_lst:
            return False
        hit = long_lst.index(short_lst[0]) if short_lst[0] in long_lst else -1
        if hit == -1:
            return False
        return check_list_order(short_lst[1:], long_lst[hit+1:])

    # 解析pattern，若解析失败则返回无结果页面
    pattern_lst = expression_parse(pattern)
    if pattern_lst is None:
        return render(request, "patternquery/noresults.html")
    
    # 需要查询的语义信息
    word_info = []
    for role, word in pattern_lst:
        if word is not None:
            for n in PATTERN2ROLE[role]:
                word_info.append(Q(**{n + "__text__contains": word}))
    
    # 若有词语要求则根据词语信息筛选SpaceInfo，否则返回全部SpaceInfo
    if word_info:
        spaceinfos = SpaceInfo.objects.filter(reduce(lambda x, y: x & y, word_info))
    else:
        spaceinfos = SpaceInfo.objects.all()
    
    # 根据semanticrange筛选语料
    if semanticrange == 'all':
        pass
    elif semanticrange in semantic_key:
        spaceinfos = spaceinfos.filter(spatial_type=semantic_key[semanticrange][0])
    else:
        return render(request, "patternquery/noresults.html")

    '''
    # 遍历SpaceInfo，解析其pattern，然后比较pattern_lst是否为其子序列，返回命中的全部info
    results: list[SpaceInfo] = []
    for spaceinfo in spaceinfos:
        space_pattern_lst = expression_parse(spaceinfo.pattern)
        if space_pattern_lst is not None and check_list_order([p[0] for p in pattern_lst], [p[0] for p in space_pattern_lst]):
            results.append(spaceinfo)
    '''

    if querymode == 'accurate':
        # 精确查询pattern信息
        pure_pattern = PATTERN_JOIN.join([p[0] for p in pattern_lst])
        results = spaceinfos.filter(pattern=pure_pattern)
    elif querymode == 'fuzzy':
        results: list[SpaceInfo] = []
        for spaceinfo in spaceinfos:
            space_pattern_lst = expression_parse(spaceinfo.pattern)
            if space_pattern_lst is not None and check_list_order([p[0] for p in pattern_lst], [p[0] for p in space_pattern_lst]):
                results.append(spaceinfo)
    else:
        return render(request, "patternquery/noresults.html")

    results = [i for i in results if getattr(i, TR1)]
    if not results:
        return render(request, "patternquery/noresults.html")
    
    # 加入分页逻辑
    # 添加显示用的切片信息
    aitems: list[tuple[SpaceInfo, str, str, str]] = []
    for i in results:
        mid_st = getattr(i, TR1).start
        mid_end = getattr(i, TR1).end
        st = max(mid_st-SHOW_RANGE, 0)
        ed = min(mid_end+SHOW_RANGE, len(i.source.context))
        aitems.append((i, f"{st}:{mid_st}", f"{mid_st}:{mid_end}", f"{mid_end}:{ed}"))

    # 分页
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
    
    return render(request, "patternquery/getresults.html", {"items":items, "page_sum": len(aitems), "page_start": items.start_index(), "page_end": items.end_index(), "page_num": paginator.num_pages, "pattern":pattern, "querymode": MODE_CHINESE[querymode], "semanticrange": semantic_name[semanticrange]})
