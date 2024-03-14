# encoding: utf8
# usage: 提取词语的函数

import threading # 多线程库
from string import printable # 所有可打印的ascii字符
from collections import Counter, deque, defaultdict # 计数器和线程安全队列类
import os # 系统调用库
import chardet # 探测文件编码类型库
import json # 读取json文件库
import csv # 将排序结果转换为csv文件
from tkinter import filedialog # 文件选择窗口
from tqdm import tqdm # 进度条库
from typing import Literal

PINYIN_DATA: str = r"pinyin_data.json" # 拼音数据文件
RES_DATA: str = r"word_extract.csv" # 词语提取结果文件
FILE_TYPE: list[str] = ['.txt'] # 可读取的文件类型
CONTEXTS_DEQUE = deque() # 文本序列，它是线程安全的
CHINESE_PUNC = "，。？！……——；：“”‘’《》【】（）、·" # 中文标点符号

def read_file(filename: str):
    """读取文本文件内容加入语料库

    Args:
        filename (str): 文本文件路径
    """
    with open(filename, mode='rb') as bfile:
        b_context = bfile.read()
    
    det_dict: dict = chardet.detect(b_context)
    file_encoding: str = 'gb18030' if 'GB' in det_dict['encoding'] else det_dict['encoding']
    # 根据对应的编码类型读文本内容
    with open(filename, mode='r', encoding=file_encoding) as tfile:
        t_context: str = tfile.read()

    # 文本加入队列
    CONTEXTS_DEQUE.append(t_context)

    print(f"{filename}处理完毕.")

def read_corpus(dirname: str):
    """读取文件夹下所有文本文件形成语料库

    Args:
        dirname (str): 文件夹路径名称
    """
    # 创建线程列表
    threads: list[threading.Thread] = []

    # 对于可以读取的文件添加线程
    for filename in tqdm(os.listdir(dirname), desc="添加读取文件线程"):
        if os.path.splitext(filename)[-1] in FILE_TYPE:
            arguments: tuple[str] = (os.path.join(dirname, filename),)
            thread = threading.Thread(target=read_file, args=arguments)
            thread.start()
            threads.append(thread)

    print(f"已选择文件夹{dirname}, 请等待文件处理...")
    # 结束线程
    for t in threads:
        t.join()

    print("文件夹处理完毕.")

def nagao(freq: int, maxlen: int, minlen: int) -> Counter[str, int]:
    """Nagao算法的实现，用于无监督提取词语

    Args:
        freq (int): 词语在语料中需要出现的频度
        maxlen (int): 词语的最大长度
        minlen (int, optional): 词语的最小长度. 为None时视为与maxlen相同.

    Returns:
        list[tuple[str, int]]: 词语及其频率
    """    
    def common_prefix_length(index1: int, index2: int) -> int:
        common_len: int = 0
        for c1, c2 in zip(corpus_str[index1:], corpus_str[index2:]):
            if c1 == c2:
                common_len += 1
            else:
                return common_len
            
    def have_punc(string: str):
        global CHINESE_PUNC
        for s in string:
            if s in printable + CHINESE_PUNC:
                return True
        return False

    # 语料库的语料列表
    global CONTEXTS_DEQUE # 检索全局变量
    corpus_str: str = "".join(CONTEXTS_DEQUE)
    del CONTEXTS_DEQUE # 删除队列
    print("语料库列表创建完毕.")
    # p_list，按照数字存储，数字代表字符串中的索引值
    print("开始创建P表, 请稍后...")
    p_list: list[int] = [i for i in range(len(corpus_str))]
    p_list.sort(key=lambda x: corpus_str[x]) # 按照对应字符对序列排序
    print("P表创建完毕.")
    # l_list，按照数字存储，数字代表p_list中对应的各字符串的最长前缀长度
    print("开始创建L表, 请稍后...")
    l_list: list[int] = [0] + [common_prefix_length(p_list[i-1], p_list[i]) for i in tqdm(range(1, len(p_list)), desc="L表共前缀长度计算")]
    print("L表创建完毕.")
    # 断言P表L表等长
    assert len(p_list) == len(l_list), "P表L表不等长, 程序出现错误."
    # 提取所有长度在(minlen, maxlen)的前缀子串
    print("开始提取子串, 请稍后...")
    # _minlen = maxlen if minlen is None else minlen # 最短长度确定
    prefix_list: list[str] = [corpus_str[index: index+length] for index, length in tqdm(zip(p_list, l_list), desc="子串提取") if type(length) == int and minlen <= length and length <= maxlen]
    # 移除带标点符号的子串
    prefix_list = [i for i in prefix_list if not have_punc(i)]
    # 生成计数器
    counter = Counter(prefix_list)
    # 从计数器中按照频率提取串
    word_list: list[tuple[str, int]] = [i for i in tqdm(counter.most_common(), desc="词语频率计算") if i[1] >= freq]
    # 将频率列表转换为计数器
    word_freq_dict = defaultdict(int)
    for word_freq in word_list:
        word_freq_dict[word_freq[0]] = word_freq[1]
    return Counter(word_freq_dict)

def substring_reduction(counter: Counter[str, int]) -> list[tuple[str, int]]:
    """子串归并算法，归并不成词的子串

    Args:
        counter (Counter[str, int]): 词语频率计数器

    Returns:
        list[tuple[str, int]]: 归并后的词语频率列表
    """
    def get_reduced(word_list: list[str], reversed: bool = False):
        for i in tqdm(range(len(ascending_word_list)-1), desc="词语归并"):
            word1 = word_list[i]
            word2 = word_list[i+1]
            if word1 in word2 and counter[word1] == counter[word2]:
                if reversed:
                    reduce_list.append(word1[::-1])
                else:
                    reduce_list.append(word1)

    print("进行词语归并，请稍后...")
    # 需要归并的子串集合
    reduce_list: list[str] = []
    # 升序子串归并
    ascending_word_list: list[str] = sorted([i for i in counter], key=lambda x:x)
    get_reduced(ascending_word_list)
    # 降序子串归并
    descending_word_list: list[str] = sorted([i[::-1] for i in counter], key=lambda x:x)
    get_reduced(descending_word_list, reversed=True)
    # 去除归并子串
    print("词语归并完成.")
    return [i for i in counter.most_common() if i[0] not in reduce_list]

def console_main():
    """以控制台运行程序时的主函数
    """
    def pinyin_sorted(word_list: list[tuple[str, int]]):
        def get_pinyin(word: tuple[str, int]) -> str:
            if word[0][0] in pinyin_data:
                return pinyin_data[word[0][0]][0]
            else:
                return "zzzzz"

        with open(PINYIN_DATA, mode='r', encoding='utf8') as jfile:
            pinyin_data: dict[str, list[str]] = json.load(jfile)

        word_list.sort(key=get_pinyin)
        return word_list
    
    corpus_dir: str = filedialog.askdirectory(title='选择语料所在文件')
    len_range: list[str] = input("词语长度下界和上界，以空格分隔：").split()
    len_range: list[int] = [int(i) for i in len_range]
    if len(len_range) != 2:
        print("词语长度下界和上界不正确")
        exit(0)
    word_freq: int = int(input("指定词语频率："))
    sort_kind_abb: Literal["f", "e", "p", ""] = input("请选择排序方式：频率f, 编码e, 拼音p, 不填默认按频率:")
    sort_kind: Literal["frequency", "encode", "pinyin"]
    
    read_corpus(corpus_dir)
    word_counter: Counter[str, int] = nagao(freq=word_freq, minlen=len_range[0], maxlen=len_range[1])
    word_list: list[tuple[str, int]] = substring_reduction(word_counter)

    sorted_list: list[tuple[str, int]]
    sort_kind: Literal["frequency", "encode", "pinyin"]
    if sort_kind_abb == 'f' or sort_kind_abb == '':
        sort_kind = "frequency"
        sorted_list = word_list
    elif sort_kind_abb == 'e':
        sort_kind = "encode"
        sorted_list = sorted(word_list, key=lambda x: x[0])
    elif sort_kind_abb == 'p':
        sort_kind = "pinyin"
        sorted_list = pinyin_sorted(word_list)
    else:
        print(f"排序方式简写不支持: {sort_kind_abb}")
        exit(0) # 不支持的排序方式时退出

    with open(f"{"_".join([sort_kind, RES_DATA])}", mode='w', encoding='utf8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(sorted_list)

    print(f"排序结果已写入{"_".join([sort_kind, RES_DATA])}.")

if __name__ == "__main__":
    # test_dir = r'D:\grammar_programming\grammar_programming\week3\word_extract\testdata'
    # read_corpus(test_dir)
    # print(nagao(freq=10, maxlen=4, minlen=2))
    console_main()
