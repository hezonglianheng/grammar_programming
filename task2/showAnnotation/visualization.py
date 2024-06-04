# encoding: utf8
# 将空间信息标注合并到依存句法分析可视化结果中
# 依存句法分析可视化结果生成参见dependency_parsing.py

import json # read json.
from bs4 import BeautifulSoup # parse html.
import config
from pathlib import Path # path operation.

UTF8 = 'utf-8'
CLASS = 'spatial-info'
FILL = 'currentColor'

def merge_ann2dep(data_item: dict):
    # 读取对应HTML文件
    with open(data_item[config.HTML], 'r', encoding=UTF8) as f:
        html_doc = f.read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    # 从HTML文件中读取分词结果
    tokens = soup.find('body').find_all('text')
    # 读取空间信息标注
    spatial: list[dict] = data_item[config.SPATIAL]
    # 向特定节点插入空间信息标注的标签
    for s in spatial:
        contain_seg: list[int] = s[config.CONTAIN_SEG]
        for seg in contain_seg:
            new_tag = soup.new_tag('tspan')
            new_tag['class'] = CLASS
            new_tag['fill'] = FILL
            new_tag['dy'] = '2em'
            new_tag['x'] = tokens[seg].find('tspan')['x']
            new_tag.string = f'{s[config.LABEL]}: {s[config.WORD]}' # 生成新的标签内容
            tokens[seg].append(new_tag)

    # 保存合并结果
    new_html_file = Path(config.PICTURE_WITH_SPATIAL) / Path(data_item[config.HTML]).name
    with open(new_html_file, 'w', encoding=UTF8) as f:
        f.write(str(soup))

# 读取合并结果json文件
with open(config.DEP_ANN_RES_PATH, 'r', encoding=UTF8) as f:
    data: list[dict] = json.load(f)

# 全部context1和context2分别形成列表
context1s = [i[config.CONTEXT1] for i in data]
context2s = [i[config.CONTEXT2] for i in data]
for i in context1s:
    merge_ann2dep(i)
for i in context2s:
    merge_ann2dep(i)