# encoding: utf8
# usage: 实现编码与汉字的相互转换

from typing import Literal # 限制函数参数的取值范围, 起提示作用
from typing import Optional # 表明类型为某类型或None

# 不同的汉字编码类型(增加一种日文编码格式shift_jis)
ENCODING_TYPES = ["gbk", "gb18030", "big5", "unicode", "utf8", "shift_jis"]
# 16进制
HEX = 16
# 单个字符长度
SINGLE_CHAR = 1

def char_to_encoding(char: str) -> dict[str, Optional[str]]:
    """输出给出汉字在不同码表下的码值
    char: 输入的汉字, 为单个字符"""
    # 确定为单个汉字
    assert len(char) == SINGLE_CHAR, f"输入{char}不是单个汉字!"
    global ENCODING_TYPES
    encoding_dir = {} # 存储编码值的字典
    # 遍历编码类型并输出码值
    for t in ENCODING_TYPES:
        if t == "unicode":
            try:
                e = str(hex(ord(char))) # 尝试返回Unicode值的字符串形式
            except:
                encoding_dir[t] = None # 出错说明码表中不存在该字符, 返回None
            else:
                encoding_dir[t] = e # 否则返回Unicode值
        else:
            try:
                e = char.encode(encoding=t).hex() # 尝试返回码表值的字符串形式
            except:
                encoding_dir[t] = None # 出错说明码表中不存在该字符, 返回None
            else:
                encoding_dir[t] = e # 否则返回码表中的码值
    return encoding_dir

def encoding_to_char(encode_set: Literal["gbk", "gb18030", "big5", "unicode", "utf8", "shift_jis"], code_value: str) -> Optional[str]:
    """将码值根据不同的码表转换为汉字

    Args:
        encode_set: 目前支持的码表类型
        code_value: 编码值, 应该是16进制数

    Raises:
        ValueError: 若输入不支持的编码集则抛出此错误

    Returns:
        Optional[str]: 若能够找到对应的字符, 返回汉字, 否则None
    """    """"""
    global HEX
    if encode_set == "unicode":
        try:
            code_value_int = int(code_value, base=HEX)
            char = chr(code_value_int) # 尝试输出Unicode码值对应的字符
        except:
            return None # 不能输出则返回None
        else:
            return char # 能够输出则返回字符
    elif encode_set in ENCODING_TYPES:
        try:
            char = bytes.fromhex(code_value).decode(encoding=encode_set) # 尝试输出码表对应的字符
        except:
            return None # 不能输出返回None
        else:
            return char # 能输出返回字符
    else:
        # 否则报错
        raise ValueError(f"不支持编码集{encode_set}")

if __name__ == "__main__":
    print(char_to_encoding("河"))
    print(encoding_to_char("gbk", 'bad3'))
    print(encoding_to_char("big5", 'aa65'))
    print(encoding_to_char('unicode', '6cb3'))
    print(encoding_to_char('utf8', 'e6b2b3'))
    print(encoding_to_char('shift_jis', '89cd'))