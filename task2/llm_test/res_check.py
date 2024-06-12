# encoding: utf8
# 检查分词是否平行，统计空间关系的语序及其与正负例的相关系数

import config
import json
import sys
from collections import Counter
from scipy.stats import pearsonr
import numpy as np

WORD_PAIR: list[tuple[str]] = [('上', '下'), ('上面', '下面'), ('上边', '下边')]

def seg_check(seg1: list[str], seg2: list[str]) -> bool:
    """检查分词是否平行"""
    def pair_check(word1: str, word2: str) -> bool:
        """检查两个词是否平行"""
        if word1 != word2 and (word1, word2) not in WORD_PAIR:
            print(word1, word2)
            return False
        return True
    
    if seg1 == seg2:
        raise ValueError(f"分词\n{seg1}和\n{seg2}\n相同，无法判断是否平行")
    if len(seg1) != len(seg2):
        print(seg1, seg2)
        return False
    wordpairs = [(w1, w2) for w1, w2 in zip(seg1, seg2)]
    if any(not pair_check(w1, w2) for w1, w2 in wordpairs):
        return False
    return True

def seg():
    with open(config.TEST_DATA, 'r', encoding='utf8') as f:
        data = json.load(f)

    not_parallel = [item for item in data if not seg_check(item[config.CONTEXT1][config.SEG], item[config.CONTEXT2][config.SEG])]
    print(len(not_parallel))
    with open(config.CHECK_FILE, 'w', encoding='utf8') as f:
        json.dump(not_parallel, f, ensure_ascii=False, indent=4)

def order():
    def get_order(item: dict) -> tuple[str]:
        # 获得空间关系标注信息
        spatial: list[dict] = item['spatial']
        # 按照contain_seg[0]排序，获得空间关系的语序
        sorted_spatial = sorted(spatial, key=lambda x: x['contain_seg'][0])
        return tuple(i['label'] for i in sorted_spatial)

    with open(config.TEST_DATA, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    context1_order = [get_order(item[config.CONTEXT1]) for item in data]
    context2_order = [get_order(item[config.CONTEXT2]) for item in data]
    order_diff = [i for i, (o1, o2) in enumerate(zip(context1_order, context2_order)) if o1 != o2]
    assert not order_diff, f"存在不同的语序{order_diff}"
    
    counter = Counter(context1_order)
    counter_sorted = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    tr_lm_order = [True if i.index('trajectory') >= i.index('landmark') else False for i in context1_order]
    judge_order = [item[config.JUDGE] for item in data]

    correlation, _ = pearsonr(tr_lm_order, judge_order)

    with open(r'check_res/check_order.txt', 'w', encoding='utf8') as f:
        for k, v in counter_sorted:
            f.write(f"{k}: {v}\n")
        f.write(f"Correlation coefficient: {correlation}")

def seg_acc() -> float:
    def intersection(std: str, pred: str) -> float:
        check_index: list[int] = []
        find_len: int = 0
        for w in pred:
            if not check_index:
                if w in std:
                    find_len += 1
                    check_index = [i for i in range(len(std)) if std[i] == w]
            else:
                check_index = [i for i in check_index if i + 1 < len(std) and std[i + 1] == w]
                if check_index:
                    find_len += 1
                else:
                    break

        return find_len / len(std)

    def spatial_acc(item: dict) -> list[float]:
        spatial_elements: list[dict] = item['spatial']
        accs: list[float] = []
        for spatial in spatial_elements:
            contain_seg_list: list[int] = spatial['contain_seg']
            contain_word: list[str] = [item['seg'][i] for i in contain_seg_list]
            std_word: str = spatial['word']
            accs.append(max([intersection(std_word, i) for i in contain_word]))

        # print(accs)
        return accs

    with open(config.TEST_DATA, 'r', encoding='utf8') as f:
        data: list[dict] = json.load(f)

    acc_list: list[float] = []
    for item in data:
        acc_list.extend(spatial_acc(item[config.CONTEXT1]))
        acc_list.extend(spatial_acc(item[config.CONTEXT2]))

    print(np.mean(acc_list))
    return np.mean(acc_list)

def help():
    pass

if __name__ == '__main__':
    func: str = sys.argv[1]
    if func == 'seg':
        seg()
    elif func == 'order':
        order()
    elif func == 'acc':
        seg_acc()
    else:
        raise ValueError(f"无法识别的函数{func}")