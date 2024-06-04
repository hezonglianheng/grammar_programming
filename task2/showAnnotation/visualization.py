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

    # 修改: 在head中添加meta标签，以支持中文显示
    head = soup.find('head')
    meta = soup.new_tag('meta')
    meta['charset'] = 'utf-8'
    head.append(meta)
    # 修改: 将head中的title标签内容改为“句法空间标注结果”
    title = soup.find('title')
    title.string = '句法空间标注结果'
    # 保存合并结果
    new_html_file = Path(config.PICTURE_WITH_SPATIAL) / Path(data_item[config.HTML]).name
    with open(new_html_file, 'w', encoding=UTF8) as f:
        f.write(str(soup))
    return str(new_html_file) # 返回合并结果文件路径

# 读取合并结果json文件
with open(config.DEP_ANN_RES_PATH, 'r', encoding=UTF8) as f:
    data: list[dict] = json.load(f)

# 全部context1和context2分别形成列表
context1s = [i[config.CONTEXT1] for i in data]
context2s = [i[config.CONTEXT2] for i in data]
context1s_new_paths = []
context2s_new_paths = []
for i in context1s:
    context1s_new_paths.append(merge_ann2dep(i))
for i in context2s:
    context2s_new_paths.append(merge_ann2dep(i))

# 修改数据的html路径
for i, item in enumerate(data):
    item[config.CONTEXT1][config.HTML] = context1s_new_paths[i]
    item[config.CONTEXT2][config.HTML] = context2s_new_paths[i]

# 存回原文件中
with open(config.DEP_ANN_RES_PATH, 'w', encoding=UTF8) as f:
    json.dump(data, f, ensure_ascii=False, indent=4)