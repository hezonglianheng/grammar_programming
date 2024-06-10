# encoding: utf8
# 将空间信息标注结果合并到依存句法分析结果中

import json # read json.
import jsonlines # write jsonlines.
from itertools import accumulate
from bisect import bisect_left, bisect
from tqdm import tqdm
import config

PAIR2CONTEXT = {1: config.CONTEXT1, 2: config.CONTEXT2} # pair到context的映射

# 读取依存句法分析结果
with open(config.DEP_RESULT_PATH, 'r', encoding='utf-8') as f:
    data: list[dict] = json.load(f)

def merge_annotation(ann: dict):
    # print(ann)

    def find_seg_for_role(role: dict[str, str|int]) -> dict[str, str|list[int]]:
        """为role找到对应的分词结果项目"""
        # 从role中提取信息
        # role的空间角色标签
        role_label: str = role[config.LABEL]
        # role的文本
        role_word: str = text[role[config.START_OFFSET]:role[config.END_OFFSET]]
        # role的开始和结束位置
        start_hit: int = bisect(seg_indexes, role[config.START_OFFSET])
        end_hit: int = bisect(seg_indexes, role[config.END_OFFSET]-1)
        # role包含的分词结果项目
        role_contain_seg: list[int] = list(range(start_hit-1, end_hit))
        if not role_contain_seg:
            print(role[config.START_OFFSET], role[config.END_OFFSET]-1, seg_indexes, start_hit, end_hit, 'fail')
        # 返回结果
        return {config.LABEL: role_label, config.WORD: role_word, config.CONTAIN_SEG: role_contain_seg}

    # 通过qid和pair找到对应的依存句法分析结果
    pair: int = ann[config.PAIR]
    context: dict = [i for i in data if i[config.QID] == ann[config.QID]][0][PAIR2CONTEXT[pair]]
    text: str = ann[config.TEXT]
    # 计算每个词的索引值
    seg_indexes = list(accumulate([0] + [len(i) for i in context[config.SEG]], func=lambda x, y: x + y))
    # 为每个role找到对应的分词结果项目
    roles_seg = [find_seg_for_role(role) for role in ann[config.ENTITIES]]
    # 并入依存句法分析结果
    context[config.SPATIAL] = roles_seg

# 读取空间信息标注结果
with jsonlines.open(config.ANNOTATE_RES_PATH) as reader:
    for item in tqdm(reader, desc='标注结果合并中'):
        merge_annotation(item)

# 写入合并结果
with open(config.DEP_ANN_RES_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
