# encoding: utf8
# usage: 向数据集中添加数据

import os
import json # 处理json文件
import django
import sys # 接受命令行参数
from tqdm import tqdm # 进度条
import pandas as pd # 统计数据用二维表格形式存储
from typing import Literal, Optional
from config import *

UTF8 = 'utf8'
EMPTY_PREP = '无介词'
EMPTY_VERB = '无动词'

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ancient_spatial.settings')

# 初始化Django
django.setup()

def update_ancient(mode: Literal['r', 'e']):
    """进行古代汉语部分数据的更新"""
    # 导入模型文件
    from spatialquery import models # 查询模型文件
    from corpus_stat import models as stat_models # 统计模型文件

    def make_text_info(space: dict, key: str) -> Optional[models.TextInfo]:
        """生成TextInfo数据"""
        if key in space and space[key]:
            return models.TextInfo(text=space[key][TEXT], start=space[key][START_OFFSET], end=space[key][END_OFFSET])
        else:
            return None

    def make_pattern(space: dict) -> str:
        """生成形式模式"""
        space_keys = [TR1, TR2, LANDMARK, EVENT, PREPOSITION, LOCATION]
        space_idxes:list[tuple[str, int, int]] = [(PATTERN_DICT[key], space[key][START_OFFSET], space[key][END_OFFSET]) for key in space_keys if space[key]]
        space_idxes.sort(key=lambda x: (x[1], x[2]))
        return PATTERN_JOIN.join([x[0] for x in space_idxes])

    def update_stat(qkey: str, stat_model: stat_models.AbstractStat, spatial_type: str):
        """更新统计数据表的结果
        qkey: 查询的关键字
        stat_model: 统计数据表
        spatial_type: 空间语义类型"""
        stat_row: Optional[stat_models.AbstractStat] = stat_model.objects.filter(stat_type=qkey).first()

        # 增加整体统计值
        if stat_row:
            stat_row.all_cases += 1
        else:
            stat_row = stat_model(stat_type=qkey, all_cases=1)
        
        # 增加空间语义类型统计值
        setattr(stat_row, RELATION_EN[spatial_type], getattr(stat_row, RELATION_EN[spatial_type]) + 1)
        # 保存更新结果
        stat_row.save()
    
    # 读取json文件
    with open(ANCIENT_RES, encoding=UTF8) as jfile:
        data: list[dict] = json.load(jfile)

    # 若mode为r(replace), 则删除所有数据
    if mode == 'r':
        # 删除查询模型所有数据
        models.OriginalText.objects.all().delete()
        models.TextInfo.objects.all().delete()
        models.SpaceInfo.objects.all().delete()
        # 删除统计模型所有数据
        stat_models.SpatialTypeStat.objects.all().delete()
        stat_models.PrepStat.objects.all().delete()
        stat_models.VerbStat.objects.all().delete()
        stat_models.PatternStat.objects.all().delete()
    else:
        pass

    # 写入数据集
    for item in tqdm(data, desc="写入数据集"):
        # 先写入原文基本信息
        origin = models.OriginalText(title=item[TITLE], subtitle=item[SUBTITLE], context=item[ANCIENT_TEXT])
        origin.save() # 记得存入
        # 遍历所有方位表达, 写入方位表达信息
        for s in item[SpaCE]:
            spatial_roles: list[models.TextInfo|None] = [make_text_info(s, r) for r in ROLES]
            for n in spatial_roles:
                if n:
                    n.save() # 记得写入
            # 创建空间信息
            roles_dict = {x: y for x, y in zip(ROLES, spatial_roles)}
            # 求出模式
            pattern = make_pattern(s)
            spatial_info = models.SpaceInfo(source=origin, **roles_dict, spatial_type=s[TYPE], pattern=pattern)
            # 保存SpaceInfo
            spatial_info.save()
            # 方位表达情形统计
            # 语义统计
            # 查询SpatialTypeStat中是否有这种方位表达语义类型
            spatial_type_stat = stat_models.SpatialTypeStat.objects.filter(spatial_type=RELATION_CHINESE[s[TYPE]]).first()

            if spatial_type_stat:
                # 如果存在，则将all_cases属性+1
                spatial_type_stat.all_cases += 1
                spatial_type_stat.save()
            else:
                # 如果不存在，则创建数据表行并将all_case属性设置为1
                spatial_type_stat = stat_models.SpatialTypeStat(spatial_type=RELATION_CHINESE[s[TYPE]], all_cases=1)
                spatial_type_stat.save()
            # 介词统计
            if s[PREPOSITION]:
                # 如果存在介词，则更新介词统计，需要传入介词的文本内容
                update_stat(s[PREPOSITION][TEXT], stat_models.PrepStat, s[TYPE])
            else:
                update_stat(EMPTY_PREP, stat_models.PrepStat, s[TYPE])
            # 动词统计
            if s[EVENT]:
                # 如果存在动词，则更新动词统计，需要传入动词的文本内容
                update_stat(s[EVENT][TEXT], stat_models.VerbStat, s[TYPE])
            else:
                update_stat(EMPTY_VERB, stat_models.VerbStat, s[TYPE])
            # 形式模式统计
            if pattern:
                update_stat(pattern, stat_models.PatternStat, s[TYPE])

def update_data(datatype: Literal['a', 'p'], mode: Literal['r', 'e']):
    """进行数据的更新"""
    assert mode == 'r' or mode == 'e', f"no mode '{mode}'"
    if datatype == 'a':
        update_ancient(mode) # 更新古代汉语数据
    elif datatype == 'p':
        pass
    else:
        raise ValueError(f"no datatype '{datatype}'")

if __name__ == "__main__":
    update_data(sys.argv[1][1], sys.argv[2][1])