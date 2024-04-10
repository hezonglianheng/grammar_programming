# encoding: utf8
# usage: 从标注材料中抽取古今平行语料

import jsonlines # 处理jsonlines文件
import json # 处理json文件
import os # 处理文件路径
from tqdm import tqdm # 进度条
from typing import Literal
from config import *
from extract_ancient import read_annotated, annotation2space


if __name__ == '__main__':
    print(read_annotated('modern'))