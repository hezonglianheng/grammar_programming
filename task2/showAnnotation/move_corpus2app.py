# encoding: utf8

# 导入配置文件
import config
from pathlib import Path
from tqdm import tqdm
from typing import Literal
import sys
import json
import hashlib
import shutil
import time
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'showAnnotation.settings')
django.setup()

from show.models import SentencePair, ReplacePair

# 程序功能标识
ProgramFunc = Literal['add', 'update', 'delete', 'help', 'show']
# 随机碰撞循环次数
RANDOM_COLLISION = 100

def add(rp_pair: str, file_path: str):
    """
    Add sentence pairs to the database for a given replace pair.

    Args:
        rp_pair (str): The replace pair.
        file_path (str): The path to the file containing the sentence pairs.

    Returns:
        None

    Raises:
        ValueError: If a random collision occurs and a unique filename cannot be generated.
    """
    
    def file_copy(sentence: str, src: str) -> Path:
        """
        Copy a file to a destination directory with a unique filename based on the sentence.

        Args:
            sentence (str): The sentence used to generate the unique filename.
            src (str): The source file path.

        Returns:
            Path: The path of the copied file.

        Raises:
            ValueError: If a random collision occurs and a unique filename cannot be generated.
        """
        hash_value = hashlib.sha256(sentence.encode('utf-8')).hexdigest()
        dst = Path(config.STATIC_DIR) / (hash_value + '.html')
        if not dst.exists():
            shutil.copy(src, dst)
        else:
            # Random collision to prevent filename duplication
            for _ in range(RANDOM_COLLISION):
                hash_value = hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()
                dst = Path(config.STATIC_DIR) / (hash_value + '.html')
                if not dst.exists():
                    shutil.copy(src, dst)
                    break
            raise ValueError("Random collision occurred, unable to generate a unique filename")
        return dst.relative_to(config.STATIC_DIR)

    with open(file_path, 'r', encoding='utf8') as f:
        sentence_pairs = json.load(f)

    rp = ReplacePair.objects.create(rp_pair=rp_pair)
    sentence_lst = []
    for sentence_pair in tqdm(sentence_pairs, desc='添加句子对'):
        context1: str = sentence_pair[config.CONTEXT1][config.SENTENCE]
        context2: str = sentence_pair[config.CONTEXT2][config.SENTENCE]
        context1_filepath = file_copy(context1, sentence_pair[config.CONTEXT1][config.HTML])
        context2_filepath = file_copy(context2, sentence_pair[config.CONTEXT2][config.HTML])
        context1_schema = sentence_pair[config.CONTEXT1][config.SCHEMA]
        context2_schema = sentence_pair[config.CONTEXT2][config.SCHEMA]
        judge = sentence_pair[config.JUDGE]
        sentence_lst.append(SentencePair(rp_pair=rp, context1=context1, context1_filepath=str(context1_filepath), context2=context2, context2_filepath=str(context2_filepath), judge=judge, context1_schema=context1_schema, context2_schema=context2_schema))

    sentence_lst = SentencePair.objects.bulk_create(sentence_lst)
    print(f"添加了替换对为{rp_pair}的{len(sentence_lst)}个句子对")
    rp.save()
    for s in sentence_lst:
        s.save()

def delete(rp_pair: str):
    """
    Delete all sentence pairs and replace pairs associated with the given rp_pair.

    Args:
        rp_pair (str): The rp_pair to be deleted.

    Returns:
        None
    """
    if ReplacePair.objects.filter(rp_pair=rp_pair).exists():
        pass
    else:
        print(f"替换对{rp_pair}不存在")
        return

    sentence_count = SentencePair.objects.filter(rp_pair__rp_pair=rp_pair).count()
        
    sentence_pairs = SentencePair.objects.filter(rp_pair__rp_pair=rp_pair)
    for sentence_pair in sentence_pairs:
        context1_filepath = sentence_pair.context1_filepath
        context2_filepath = sentence_pair.context2_filepath
        path1 = Path(config.STATIC_DIR) / context1_filepath
        path2 = Path(config.STATIC_DIR) / context2_filepath
        if os.path.exists(path1):
            os.remove(path1)
        if os.path.exists(path2):
            os.remove(path2)
        
    sentence_pairs.delete()
    ReplacePair.objects.filter(rp_pair=rp_pair).delete()

    print(f"移除了替换对为{rp_pair}的{sentence_count}个句子对")

def update(rp_pair: str, file_path: str):
    """
    Updates the rp_pair by deleting the existing entry and adding a new entry with the provided file_path.
    
    Args:
        rp_pair (str): The rp_pair to be updated.
        file_path (str): The new file path to be associated with the rp_pair.
    """
    delete(rp_pair)
    add(rp_pair, file_path)

def help(func_name: ProgramFunc = None):
    if not func_name:
        print("""
        使用方法: python move_corpus2app.py [program_func] [rp_pair] [file_path]
            program_func: 使用的函数. 选项有'add', 'update', 'delete', 'help', 'show'.
            rp_pair: 需要操作的替换对.
            file_path: 包含句子对的json文件路径.
            """)
    elif func_name == 'add':
        print("""
        使用方法: python move_corpus2app.py add [rp_pair] [file_path]
            rp_pair: 需要操作的替换对.
            file_path: 包含句子对的json文件路径.
            """)
    elif func_name == 'update':
        print("""
        使用方法: python move_corpus2app.py update [rp_pair] [file_path]
            rp_pair: 需要操作的替换对.
            file_path: 包含句子对的json文件路径.
            """)
    elif func_name == 'delete':
        print("""
        使用方法: python move_corpus2app.py delete [rp_pair]
            rp_pair: 需要操作的替换对.
            """)
    elif func_name == 'show':
        print("""
        使用方法: python move_corpus2app.py show
            显示所有已有的替换对.
            """)
    elif func_name == 'help':
        print("""
        使用方法: python move_corpus2app.py help [func_name]
            func_name: 需要查看帮助的函数名.
            """)
    else:
        raise ValueError(f"没有操作'{func_name}'")

def show():
    replace_pairs = ReplacePair.objects.all()
    print('目前已有的替换对:')
    for replace_pair in replace_pairs:
        print(replace_pair.rp_pair)

if __name__ == '__main__':
    # 读取命令行参数
    program_func: ProgramFunc = sys.argv[1]
    if program_func == 'update':
        rp_pair: str = sys.argv[2] # 需要操作的替换对
        file_path: str = sys.argv[3] # 需要操作的文件路径
        update(rp_pair, file_path)
    elif program_func == 'delete':
        rp_pair: str = sys.argv[2] # 需要操作的替换对
        delete(rp_pair)
    elif program_func == 'help':
        if len(sys.argv) < 3:
            help()
        else:
            help(sys.argv[2])
    elif program_func == 'add':
        rp_pair: str = sys.argv[2] # 需要操作的替换对
        file_path: str = sys.argv[3]
        add()
    elif program_func == 'show':
        show()
    else:
        raise ValueError(f"没有操作'{program_func}'")