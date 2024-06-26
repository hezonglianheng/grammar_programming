from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q # 用于组合查询条件
from typing import Literal
from collections import Counter # 用于计数
# 引入单语查询的模型
from spatialquery.models import OriginalText, SpaceInfo, TextInfo
# 引入将语义范畴翻译为数据库对应值的字典
from spatialquery.views import semantic_key, semantic_name
# 引入语料统计的模型
from .models import SpatialTypeStat, PatternStat, PrepStat, VerbStat, AbstractStat

# 参数类型标签
CategoryType = Literal['all', 'place', 'departure', 'destination', 'orientation', 'direction', 'path', 'part']
ActionType = Literal['semantic', 'preposition', 'verb', 'pattern']

# 语义类型标签
semantic_dict = {
    'isPlace': '处所',
    'isDeparture': '起点',
    'isDestination': '终点',
    'isOrientation': '朝向',
    'isDirection': '方向',
    'isPath': '路径',
    'isPart': '部件',
}
range_dict = {
    'place': '处所',
    'departure': '起点',
    'destination': '终点',
    'orientation': '朝向',
    'direction': '方向',
    'path': '路径',
    'part': '部件处所',
    'all': '全部',
    'all_cases': '全部'
}
# 其他常量
TOTAL = "总计"
EVENT = 'event'
PREP = 'preposition'
TITLE = "title"
RANGE = "range"
CATEGORY = "category"
ROLE = 'role'

# Create your views here.
def guide(request):
    """数据统计导航页"""
    return render(request, "corpus_stat/guidepage.html")
    
def query(request):
    """接受查询信息，跳转到相应的查询结果页面

    Args:
        request: 访问请求，由Django自动传入
    """
    # 语义范畴
    category: CategoryType = request.GET.get("category")
    # 查询动作
    action: ActionType = request.GET.get("action")
    # 重定向到相应的查询结果页面
    if action == "semantic":
        # return semantic(request, category)
        return semantic(request)
    elif action == "preposition":
        return prep(request, category)
    elif action == "verb":
        return verb(request, category)
    elif action == "pattern":
        return pattern(request, category)
    return HttpResponse("功能尚未开发，敬请期待……")

# deprecated function.
def semantic_ver1(request, category: CategoryType):
    """统计各语义的语料数量

    Args:
        request: 访问请求，由Django自动传入
        category (CategoryType): 语义范畴

    Returns:
        HttpResponse: 渲染后的HTML页面
    """
    # 统计各语义的语料数量
    count_by_type: list[int] = [SpaceInfo.objects.filter(**{semantic_name: i}).count() for i in semantic_dict]
    # 构筑结果列表
    result_list = list(zip(semantic_dict.values(), count_by_type))
    # 增加总计值
    result_list.append((TOTAL, sum(count_by_type)))
    return render(request, "corpus_stat/statres.html", {'res_list': result_list, TITLE: '语义类型', RANGE: '全部'})

# deprecated function.
def prep_ver1(request, category: CategoryType):
    # 根据语义范畴进行查询
    if category == 'all':
        qres = SpaceInfo.objects.all()
    else:
        qres = SpaceInfo.objects.filter(Q(**{semantic_name: semantic_key[category][0]}))
    # 统计介词出现次数
    preposition_counter = Counter([item.preposition.text if item.preposition else "无介词" for item in qres])
    # 按照出现次数从大到小排序
    sorted_prepositions = preposition_counter.most_common()
    return render(request, "corpus_stat/statres_withform.html", {'res_list': sorted_prepositions, TITLE: '介词', RANGE: range_dict[category], ROLE: "preposition", CATEGORY: category})

# deprecated function.
def verb_ver1(request, category: CategoryType):
    # 根据语义范畴进行查询
    if category == 'all':
        qres = SpaceInfo.objects.all()
    else:
        qres = SpaceInfo.objects.filter(Q(**{semantic_name: semantic_key[category][0]}))
    # 统计介词出现次数
    event_counter = Counter([item.event.text if item.event else "无事件" for item in qres])
    # 按照出现次数从大到小排序
    sorted_event = event_counter.most_common()
    return render(request, "corpus_stat/statres_withform.html", {'res_list': sorted_event, TITLE: '事件', RANGE: range_dict[category], ROLE: "event", CATEGORY: category})

# deprecated function.
def pattern_ver1(request, category: CategoryType):
    # 根据语义范畴进行查询
    if category == 'all':
        qres = SpaceInfo.objects.all()
    else:
        qres = SpaceInfo.objects.filter(Q(**{semantic_name: semantic_key[category][0]}))
    # 按照qres中的pattern键的值进行计数
    pattern_counter = Counter([item.pattern for item in qres])
    # 按照出现次数从大到小排序
    sorted_pattern = pattern_counter.most_common()
    return render(request, "corpus_stat/statres_withform.html", {'res_list': sorted_pattern, TITLE: '表达模式', RANGE: range_dict[category], ROLE: "pattern", CATEGORY: category})

# 更新：根据统计模型使用新的函数
def semantic(request):
    """统计各语义的语料数量"""
    # 获取SpatialTypeStat的全部结果并按照all_cases的值降序排序
    stat_results = SpatialTypeStat.objects.all().order_by('-all_cases')
    html_params = {TITLE: '语义类型', RANGE: '全部', 'results': stat_results}
    return render(request, "corpus_stat/statres.html", html_params)

ModelName = Literal['介词', '事件', '形式模式']
ModelDict: dict[ModelName, AbstractStat] = {'介词': PrepStat, '事件': VerbStat, '形式模式': PatternStat}

def query_abstat(request, category: CategoryType, model_name: ModelName):
    """统计介词、事件、形式模式的使用情况"""
    # 转换类别名称
    new_category = category if category != 'all' else 'all_cases'
    # 获取统计结果, 按照category的值降序排序, 取出stat_type、category两列
    stat_results = ModelDict[model_name].objects.all().order_by(f'-{new_category}').values_list('stat_type', new_category)
    # Filter out items with a value less than or equal to 0
    stat_results = stat_results.exclude(**{new_category + '__lte': 0})
    html_params = {TITLE: model_name, RANGE: range_dict[category], 'results': stat_results, 'stat_type': 'stat_type', 'new_category': new_category}
    return render(request, "corpus_stat/statres_withform.html", html_params)

def prep(request, category: CategoryType):
    """统计介词的使用情况"""
    return query_abstat(request, category, '介词')

def verb(request, category: CategoryType):
    """统计事件的使用情况"""
    return query_abstat(request, category, '事件')

def pattern(request, category: CategoryType):
    """统计形式模式的使用情况"""
    return query_abstat(request, category, '形式模式')
