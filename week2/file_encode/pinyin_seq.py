# encoding: utf8
# usage: 给出汉字的拼音顺序

from pathlib import Path # 面向对象路径库
import json # 数据表使用json格式存储读取
from collections import defaultdict # 可以设计默认值的字典

PINYIN_DATA_TXT = r'.\汉字字音数据库.txt' # txt汉字字音数据库
PINYIN_DATA_JSON = r'.\pinyin_data.json' # json汉字字音数据库
UTF8 = 'utf8' # utf8编码格式
CHAR = 1 # 汉字在列表中index=1
PINYIN = 2 # 拼音在列表中index=2
FIRST = 0 # 列表的首个索引值

def create_json_data():
    """从文本形式数据库生成备用json文件
    """
    # 读取文本文件
    assert Path(PINYIN_DATA_TXT).exists(), "汉字字音数据库不存在, 请检查文件配置"
    with open(PINYIN_DATA_TXT, mode='r', encoding=UTF8) as tfile:
        pinyin_list = tfile.readlines()

    pinyin_list = [i.split() for i in pinyin_list]

    # 将列表转换为字典, 并排序
    pinyin_dict = defaultdict(list) # 以列表作为值的字典
    for p in pinyin_list:
        if len(p) <= PINYIN: # 跳过数据集中不完整的数据
            # print(p)
            continue
        pinyin_dict[p[CHAR]].append(p[PINYIN]) # 拼音数据加到字典中
    
    for c in pinyin_dict:
        sorted(pinyin_dict[c]) # 对字典的值做排序
    
    # 写入json文件
    with open(PINYIN_DATA_JSON, mode='w', encoding=UTF8) as jfile:
        json.dump(pinyin_dict, jfile, indent=4, ensure_ascii=False)

def _load_json_data() -> dict[str, list[str]]:
    """加载json数据库

    Returns:
        dict[str, list[str]]: json文件中记录的数据库
    """
    # 检查json文件数据库是否存在
    if not Path(PINYIN_DATA_JSON).exists():
        create_json_data()
    assert Path(PINYIN_DATA_JSON).exists(), '数据集缺失, 请检查文件配置'

    # 读取数据
    with open(PINYIN_DATA_JSON, mode="r", encoding=UTF8) as jfile:
        pinyin_dict = json.load(jfile)

    return pinyin_dict

def _pinyin_query(char: str, dic: dict, onlyfirst: bool = False) -> str | list[str] | None:
    """在拼音数据库中查询一个汉字的拼音

    Args:
        char (str): 需要查询的汉字
        dic (dict): 查询用的字典
        onlyfirst: 是否只查询第一个拼音

    Returns:
        str | list[str] | None: 若汉字在字典中, 则返回其拼音形式, 否则返回None
    """
    assert len(char) == 1, f"“{char}”不是一个字符" # 断言查询的是单个字符
    try:
        pinyin = dic[char] # 查字典
    except:
        return None # 查不出返回None
    else:
        # 否则返回拼音
        return pinyin[FIRST] if onlyfirst else pinyin

def pinyin_query(char: str) -> list[str] | None:
    """在拼音数据库中查询一个汉字的拼音

    Args:
        char (str): 需要查询的汉字

    Returns:
        list[str] | None: 若汉字在字典中, 则返回其拼音形式, 否则返回None
    """
    pinyin_dict = _load_json_data()
    return _pinyin_query(char, pinyin_dict)

def pinyin_sort(chars: list[str]) -> list[str] | None:
    """为一个汉字列表排序

    Args:
        chars (list[str]): 需要排序的汉字列表

    Returns:
        list[str] | None: 若能够排序则返回拼音序的汉字列表, 否则返回None
    """
    pinyin_dict = _load_json_data()

    # 查询
    pinyin_qres = [(c, _pinyin_query(c, pinyin_dict, onlyfirst=True)) for c in chars]
    # 若出现None, 则无法排序, 返回None, 否则返回排序结果
    if None in [r[PINYIN-1] for r in pinyin_qres]:
        return None
    else:
        pinyin_qres.sort(key=lambda x: x[PINYIN-1])
        return [p[CHAR-1] for p in pinyin_qres]

if __name__ == "__main__":
    # create_json_data()
    print(pinyin_query('朝'))