# encoding: utf8
# usage: 操作文件大小与文件名称

from pathlib import Path # python新的面向对象路径库
from functools import lru_cache # 用于缓存已经计算的结果, 减小计算开销
from typing import Literal # python类型库, 用于限定取值范围

# 默认结果文件路径
SIZES_FILE = r"get_sizes.txt"

def size_file():
    """输出统计结果文件路径"""
    global SIZES_FILE
    return SIZES_FILE

@lru_cache
def get_size(path: Path) -> int:
    """获得文件或文件夹的size信息
    path: 文件或文件夹的路径"""
    # 分别处理path作为文件或文件夹的情况
    # path作为文件
    if path.is_file():
        # 返回文件大小信息
        return path.stat().st_size
    # path作为文件夹
    elif path.is_dir():
        # 文件夹内容大小的加和
        dir_size = sum([get_size(p) for p in path.iterdir()])
        # 返回文件夹大小信息
        return dir_size
    else:
        raise ValueError(f"路径{path}不是合法的文件或文件夹")

def get_root_size(root_path: str):
    """获得某个路径下所有文件的size信息
    root_path: 被探测的路径
    """
    # 转换文件路径类型
    path_path = Path(root_path)
    # 打开结果文件
    global SIZES_FILE
    with open(SIZES_FILE, "w", encoding='utf8') as f:
        for root, _, files in path_path.walk():
            # 文件夹大小获得并写入特定文件
            f.write(f"dir:{root}, size:{get_size(root)} bytes\n")
            # 文件大小获得并写入文件
            for file in files:
                f.write(f"dir:{root/file}, size:{get_size(root/file)} bytes\n")


def modify_path(path: Path, string: str, pos: Literal["prefix", "suffix"]):
    """为某个文件名添加前缀或后缀的函数
    path: 父目录路径
    string: 需要添加的文本
    pos: 添加位置, 分为前缀prefix和后缀suffix"""
    # 获取新的路径
    if pos == 'prefix':
        # 路径变为父目录 + 前缀 + 文件名
        newpath = path.parent / (string + path.name)
    elif pos == 'suffix':
        # 路径变为去除扩展名的路径 + 后缀 + 扩展名
        newpath = Path(path.stem + string + path.suffix)
    else:
        raise ValueError(f"输入的添加字段位置不正确")
    # 更名
    path.rename(newpath)

def modify_paths(path: str, string: str, pos: Literal["prefix", "suffix"]):
    """为某个目录下文件名批量添加前缀或后缀的函数
    path: 父目录路径
    string: 需要添加的文本
    pos: 添加位置, 分为前缀prefix和后缀suffix"""
    # 将字符串路径转换为路径对象
    ppath = Path(path)
    # 取绝对路径
    abs_ppath = ppath.absolute()
    # 遍历路径更名
    for root, _, files in abs_ppath.walk():
        for file in files:
            # 对每个文件调用更名函数
            modify_path(Path(root/file), string, pos)

if __name__ == "__main__":
    test_file = r"D:\grammar_programming\grammar_programming\week1"
    get_root_size(test_file)