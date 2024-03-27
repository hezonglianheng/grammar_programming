# encoding: utf8
# usage: 向数据集中添加数据

import os
import json # 处理json文件
import django
import sys # 接受命令行参数
from tqdm import tqdm # 进度条
from typing import Literal, Optional
from config import *

UTF8 = 'utf8'

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ancient_spatial.settings')

# 初始化Django
django.setup()

def update_ancient(mode: Literal['r', 'e']):
    """进行古代汉语部分数据的更新"""
    # 导入模型文件
    from spatialquery import models # 模型文件

    def make_text_info(space: dict, key: str) -> Optional[models.TextInfo]:
        """生成TextInfo数据"""
        if key in space and space[key]:
            return models.TextInfo(text=space[key][TEXT], start=space[key][START_OFFSET], end=space[key][END_OFFSET])
        else:
            return None

    # 读取json文件
    with open(ANCIENT_RES, encoding=UTF8) as jfile:
        data: list[dict] = json.load(jfile)

    # 若mode为r(replace), 则删除所有数据
    if mode == 'r':
        models.OriginalText.objects.all().delete()
        models.TextInfo.objects.all().delete()
        models.SpaceInfo.objects.all().delete()
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
            # 创建空间信息并保存
            roles_dict = {x:y for x, y in zip(ROLES, spatial_roles)}
            spatial_info = models.SpaceInfo(source=origin, **roles_dict, spatial_type=s[TYPE])
            spatial_info.save()

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