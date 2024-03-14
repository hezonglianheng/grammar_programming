# encoding: utf8
# usage: 实现各功能的函数

import threading # 尝试使用多线程处理这一问题
from string import printable # 所有可打印的ascii字符
from collections import Counter, deque # 计数器和线程安全队列类
import os # 系统调用库
import chardet # 探测文件编码类型库
import json # 读取json文件库
import csv # 将排序结果转换为csv文件
from tkinter import filedialog # 文件选择窗口
from tqdm import tqdm # 进度条库
from typing import Literal

CHAR_DEQUE: deque = deque() # 字符队列
FILE_TYPE: list[str] = ['.txt'] # 可读取的文件类型
CHINESE_PUNC = "，。？！……——；：“”‘’《》【】（）、" # 中文标点符号
PINYIN_DATA = r"pinyin_data.json" # 拼音数据文件
RES_FILE = r"sort_res.csv" # 排序结果存储文件

def get_file_chars(file_name: str) -> None:
    """将文件中的字符加入队列中备用

    Args:
        file_name (str): 读取的文件名
    """
    # 读文件，确定编码类型
    with open(file_name, mode='rb') as bfile:
        b_context = bfile.read()
    
    det_dict: dict = chardet.detect(b_context)
    file_encoding = 'gb18030' if 'GB' in det_dict['encoding'] else det_dict['encoding']
    # 根据对应的编码类型读文本内容
    with open(file_name, mode='r', encoding=file_encoding) as tfile:
        t_context: str = tfile.read()

    # 若字符不是ascii可打印字符则加入队列中
    for c in tqdm(t_context, desc=os.path.split(file_name)[-1]):
        if c not in printable and c not in CHINESE_PUNC:
            CHAR_DEQUE.append(c)

    print(f"{file_name}处理完毕.")

def get_dir_chars(dir_name: str) -> Counter:
    """统计文件夹下文本文件的字符情况

    Args:
        dir_name (str): 文件夹路径

    Returns:
        Counter: 统计计数器(dict的子类)
    """
    # 创建线程列表
    count_threads: list[threading.Thread] = []

    # 对于可以读取的文件添加线程
    for filename in tqdm(os.listdir(dir_name), desc="添加读取文件线程"):
        if os.path.splitext(filename)[-1] in FILE_TYPE:
            arguments: tuple[str] = (os.path.join(dir_name, filename),)
            thread = threading.Thread(target=get_file_chars, args=arguments)
            thread.start()
            count_threads.append(thread)

    print(f"已选择文件夹{dir_name}, 请等待文件处理...")
    # 结束线程
    for t in count_threads:
        t.join()

    # 队列转换为计数器
    char_counter = Counter(CHAR_DEQUE)

    return char_counter

def sort_by_pinyin(char_list: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """将字符频率列表按照音序排列

    Args:
        char_list (list[tuple[str, int]]): 需要排列的字符频率列表

    Returns:
        list[tuple[str, int]]: 已经排序的字符频率列表
    """
    def pinyin(char_freq: tuple[str, int]):
        if char_freq[0] in pinyin_dict:
            return pinyin_dict[char_freq[0]][0]
        else:
            return "zzzzz" # 查不出来的放在最后
    # 读取拼音数据
    with open(PINYIN_DATA, encoding='utf8') as jfile:
        pinyin_dict: dict[str, list[str]] = json.load(jfile)

    # char_list = [c for c in counter]
    char_list.sort(key=pinyin)
    return char_list
    
def chars_sort(counter: Counter, kind: Literal['frequency', 'encode', 'pinyin'] = 'frequency'):
    """对统计的字符串做排序

    Args:
        counter (Counter): 字符串统计结果
        kind (Literal[&#39;frequency&#39;, &#39;encode&#39;, &#39;pinyin&#39;], optional): 排序依据(频率,编码,拼音). 默认按照频率排序.

    Raises:
        ValueError: 排序种类不支持时抛出
    """    """"""   
    char_list: list[tuple[str, int]] = counter.most_common()
    sorted_chars: list[tuple[str, int]]
    if kind == 'frequency':
        sorted_chars = char_list
    elif kind == 'pinyin':
        sorted_chars = sort_by_pinyin(char_list)
    elif kind == 'encode':
        char_list.sort(key=lambda x: x[0])
        sorted_chars = char_list
    else:
        raise ValueError(f'不支持按照{kind}排序！')
    
    with open("_".join([kind, RES_FILE]), mode='w', encoding='utf8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sorted_chars)

    print(f"排序结果已写入{"_".join([kind, RES_FILE])}.")

def console_main():
    """以控制台启动程序的主函数

    Raises:
        ValueError: 输入不支持的排序方式时抛出
    """
    corpus_dir: str = filedialog.askdirectory(title='选择语料所在文件')
    sort_kind_abb: Literal["f", "e", "p"] = input("请选择排序方式：频率f, 编码e, 拼音p, 不填默认按频率:")
    sort_kind: Literal["frequency", "encode", "pinyin"]
    if sort_kind_abb == 'f':
        sort_kind = "frequency"
    elif sort_kind_abb == 'e':
        sort_kind = "encode"
    elif sort_kind_abb == 'p':
        sort_kind = "pinyin"
    else:
        print(f"排序方式简写不支持: {sort_kind_abb}")
        exit(0) # 不支持的排序方式时退出
    counter = get_dir_chars(corpus_dir)
    chars_sort(counter=counter, kind=sort_kind)

if __name__ == "__main__":
    # test_dir = r'E:\CCL语料整理1210\corpus\xiandai\\1990s\\1999\报刊\人民日报'
    # print(get_dir_chars(test_dir))
    console_main()