# encoding: utf8
# usage: 将不同编码的文本转换为utf8编码格式的text文件

import docx # 用于处理docx文件的第三方库
import pdfplumber # 用于处理pdf文件的第三方库
import chardet # 用于探测txt文件编码类型的第三方库
from pathlib import Path # 面向对象路径库

# 支持的文件后缀
TXT_SUFFIX = '.txt' # 文本文件后缀
DOCX_SUFFIX = '.docx' # docx文件后缀
PDF_SUFFIX = '.pdf' # pdf文件后缀
UTF8 = 'utf8'
FILE_SUFFIXES = [TXT_SUFFIX, DOCX_SUFFIX, PDF_SUFFIX]

def file_transfer(filepath: str|Path, dst: str|Path):
    # 将字符串形式的路径转换为Path形式
    if type(filepath) == str:
        filepath = Path(filepath)
    if type(dst) == str:
        dst = Path(dst)

    text = "" # 读取的文件内容
    if filepath.suffix == TXT_SUFFIX:
        # 侦测txt的编码格式
        with filepath.open(mode='br') as bfile:
            det_encode = chardet.detect(bfile.read())['encoding']
        # 读取文件
        with filepath.open(mode='r', encoding=det_encode) as ffile:
            text = ffile.read()
    elif filepath.suffix == DOCX_SUFFIX:
        document = docx.Document(str(filepath)) # 打开document
        # 提取每段中的文字
        for par in document.paragraphs:
            text += par.text
    elif filepath.suffix == PDF_SUFFIX:
        with pdfplumber.open(filepath) as pdf: # 打开pdf
            # 提取每页中的文字
            for page in pdf.pages:
                text += page.extract_text()
    else:
        raise ValueError(f'不支持转换文件:{filepath}')

    # todo: 文件写入
    # 新文件的路径
    new_file_path = dst / (filepath.stem + TXT_SUFFIX)
    # 将文本写入新路径
    with open(new_file_path, mode='w', encoding=UTF8) as wfile:
        wfile.write(text)

def dir_transfer(dirpath: str|Path, dst: str|Path):
    """将文件夹下的所有文件的编码转换为utf8编码格式的text文件

    Args:
        dirpath (str | Path): 需要转换的文件夹的路径
        dst (str | Path): 结果文件放置的文件夹路径

    Raises:
        OSError: 当需要转换的文件夹下存在非文件和文件夹的事物时抛出
    """    
    if type(dirpath) == str:
        dirpath = Path(dirpath)
    # 遍历文件夹下的所有文件
    for p in dirpath.iterdir():
        if p.is_dir():
            dir_transfer(p, dst) # 文件夹的场合递归调用
        elif p.is_file:
            file_transfer(p, dst) # 文件的场合调用具体文件处理函数
        else:
            raise OSError(f"{p}不是可以正常读取的文件或文件夹")

if __name__ == "__main__":
    # file_transfer(r"E:\大三下学期\学年论文\论文\方位词“前、后、左、右”的参照策略 郭锐 2004 comments by qyh.pdf", r'.')
    dir_transfer(r"D:\grammar_programming\grammar_programming\week2\file_encode\testdata\transfer_test", r'D:\grammar_programming\grammar_programming\week2\file_encode\testdata\transfer_res')