# encoding: utf8
# usage: 从标注好的jsonlines文件中抽取与古代汉语空间表达相关的信息

import jsonlines # 处理jsonlines文件
import json # 处理json文件
import os # 处理文件路径
from tqdm import tqdm # 进度条
from typing import Literal
from config import *

# 提取语料中的古代部分

ancient_list: list[dict] = []

def data_extract(annotated: dict, need: Literal['ancient', 'modern'] = 'ancient'):
    """从标注数据中提取古代/现代汉语数据"""
    # 切割古今语料
    need_idx: int = 0 if need == 'ancient' else 1
    _text = annotated[TEXT].split('\n')[need_idx]
    text_len = len(_text)
    # 筛选entities
    ancient_entities = [i for i in annotated[ENTITIES] if i[START_OFFSET] <= text_len and i[END_OFFSET] <= text_len]
    # 筛选relations
    entities_ids = [i[ID] for i in ancient_entities] # entities的id
    ancient_relations = [i for i in annotated[RELATIONS]] # 通过entities的id筛选relations
    return {
        ANCIENT_TEXT: _text, # 文本
        SOURCE: annotated[SOURCE], # 来源
        ENTITIES: ancient_entities, # 实体
        RELATIONS: ancient_relations, # 关系
    }

def ancient_concat(newitem: dict):
    """将年份相同的材料进行合并"""
    if ancient_list:
        olditem: dict = ancient_list[-1]
        if newitem[SOURCE] != olditem[SOURCE]:
            # 若年份不同直接加入
            ancient_list.append(newitem)
        else:
            # 拼接文本
            ancient_text: str = olditem[ANCIENT_TEXT] + newitem[ANCIENT_TEXT]
            # 调整索引值
            last_len: int = len(olditem[ANCIENT_TEXT])
            for i in newitem[ENTITIES]:
                # 索引值的更新
                i.update({START_OFFSET: i[START_OFFSET]+last_len, END_OFFSET: i[END_OFFSET]+last_len})

            # 删除旧有材料
            olditem = ancient_list.pop()
            # 添加新材料
            ancient_list.append(
                {
                    ANCIENT_TEXT: ancient_text, 
                    SOURCE: newitem[SOURCE], 
                    ENTITIES: olditem[ENTITIES] + newitem[ENTITIES],
                    RELATIONS: olditem[RELATIONS] + newitem[RELATIONS]
                }
            )
    else:
        ancient_list.append(newitem)

def read_annotated(need: Literal["ancient", "modern"]) -> list[dict]:
    # 从文件夹逐个读取
    extracted = []
    for i in os.listdir(ANNOTATED_DIR):
        if JSONL_SUFFIX in i:
            with jsonlines.open(os.path.join(ANNOTATED_DIR, i)) as reader:
                extracted.extend([data_extract(j, need) for j in reader])
    
    return extracted

def annotation2space(annotated: dict) -> dict:
    """按照SpaCE规范整理标注材料"""
    
    def relation2entities(relations: list[dict], id_key: Literal['from_id', 'to_id'] = 'from_id'):
        keys: list[int] = [i[id_key] for i in relations]
        res: list[dict] = []
        for k in keys:
            res.extend([i for i in entities if i[ID] == k])
        return res

    # 实体列表
    entities: list[dict] = annotated[ENTITIES]
    # 关系列表
    relations: list[dict] = annotated[RELATIONS]
    # 界标列表
    landmarks: list[dict] = [i for i in entities if i[LABEL] == LANDMARK]
    # space信息列表
    space_infos: list[dict] = []
    # 根据界标找到其他因素
    for m in landmarks:
        # 射体，可能有1个或多个
        trajectory = relation2entities([i for i in relations if i[FROM_ID] == m[ID] and i[TYPE] in spatial_relation], TO_ID)
        _types = [i for i in relations if i[FROM_ID] == m[ID] and i[TYPE] in spatial_relation]
        # assert len(_types) >= 1, f"{annotated[SOURCE]}, {annotated[ANCIENT_TEXT][m[START_OFFSET]-5:m[END_OFFSET]+5]}" # 界标只能有1个类型
        if len(_types) < 1:
            print(f"{annotated[SOURCE]}, {annotated[ANCIENT_TEXT][m[START_OFFSET]-5:m[END_OFFSET]+5]}")
            break
        _type = _types[0][TYPE]
        # 界标，可能有1个
        preposition = relation2entities([i for i in relations if i[TO_ID] == m[ID] and i[TYPE] == isPreposition])
        # 方位词，可能有1个
        location = relation2entities([i for i in relations if i[TO_ID] == m[ID] and i[TYPE] == isLocation])
        # 事件，与射体相对应
        # 修改语料标注合法性检查行为
        # 实体只能有1~2个 界标只能有0~1个 方位词只能有0~1个
        if not 1 <= len(trajectory) <= 2 or not 0 <= len(preposition) <= 1 or not 0 <= len(location) <= 1:
            print(f"{annotated[SOURCE]}, {annotated[ANCIENT_TEXT][m[START_OFFSET]-5:m[END_OFFSET]+5]}")
        # assert 0 <= len(preposition) <= 1 # 界标只能有0~1个
        # assert 0 <= len(location) <= 1 # 方位词只能有0~1个
        event: list[list[dict]] = []
        for t in trajectory:
            curr_event = relation2entities([i for i in relations if i[TO_ID] == t[ID] and i[TYPE] == isAction])
            # 事件只能有0~1个
            if 0 <= len(curr_event) <= 1:
                event.append(curr_event)
            else:
                print(f"{annotated[SOURCE]}, {annotated[ANCIENT_TEXT][t[START_OFFSET]-5:t[END_OFFSET]+5]}")
        assert len(event) == len(trajectory) # 实体事件一一对应
        # 产生1条完整SpaCE信息
        space_info = {
            TR1: {x: trajectory[0][x] for x in OFFSET_RANGE} | {TEXT: annotated[ANCIENT_TEXT][trajectory[0][START_OFFSET]:trajectory[0][END_OFFSET]]}, 
            TR2: {x: trajectory[1][x] for x in OFFSET_RANGE} | {TEXT: annotated[ANCIENT_TEXT][trajectory[1][START_OFFSET]:trajectory[1][END_OFFSET]]} if len(trajectory) == 2 else None, 
            EVENT: {x: event[0][0][x] for x in OFFSET_RANGE} | {TEXT: annotated[ANCIENT_TEXT][event[0][0][START_OFFSET]:event[0][0][END_OFFSET]]} if len(event[0]) else None,
            LANDMARK: {x: m[x] for x in OFFSET_RANGE} | {TEXT: annotated[ANCIENT_TEXT][m[START_OFFSET]:m[END_OFFSET]]}, 
            PREPOSITION: {x: preposition[0][x] for x in OFFSET_RANGE} | {TEXT: annotated[ANCIENT_TEXT][preposition[0][START_OFFSET]:preposition[0][END_OFFSET]]} if len(preposition) else None,
            LOCATION: {x: location[0][x] for x in OFFSET_RANGE} | {TEXT: annotated[ANCIENT_TEXT][location[0][START_OFFSET]:location[0][END_OFFSET]]} if len(location) else None,
            TYPE: _type, 
        }
        space_infos.append(space_info)

    return {
        TITLE: annotated[SOURCE].split('-')[0],
        SUBTITLE: annotated[SOURCE].split('-')[1], 
        ANCIENT_TEXT: annotated[ANCIENT_TEXT], 
        SpaCE: space_infos
    }

if __name__ == "__main__":
    print('开始从标注文件中抽取语料.')
    '''
    with jsonlines.open(ANNOTATED) as reader:
        extracted = [data_extract(i) for i in reader]
    '''

    # 从文件夹逐个读取
    extracted = []
    for i in os.listdir(ANNOTATED_DIR):
        if JSONL_SUFFIX in i:
            with jsonlines.open(os.path.join(ANNOTATED_DIR, i)) as reader:
                extracted.extend([data_extract(j) for j in reader])
    
    organized = []    
    for i in tqdm(extracted, desc='语料合并'):
        ancient_concat(i)
    for i in tqdm(ancient_list, desc='语料整理'):
        organized.append(annotation2space(i))

    with open(ANCIENT_RES, mode='w', encoding='utf8') as jfile:
        json.dump(organized, jfile, indent=4, ensure_ascii=False)

    print('古汉语料抽取完毕.')