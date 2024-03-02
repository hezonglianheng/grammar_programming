# 文件格式及字符编码处理程序说明

2024年3月2日

本项目是一个文件格式及字符编码处理程序, 主要实现了以下功能：
1. 由汉字查码值：
    - 输入：汉字
    - 输出：该汉字的GBK码、Big5码、Unicode码、UTF8码、shift_jis码值
2. 由码值查汉字：
    - 输入：用户指定编码集（GBK码、Big5码、Unicode码、UTF8码、shift_jis码），码值
    - 输出：汉字
3. 文件格式及编码转换：
    - 输入：用户指定文件夹（文件夹下可以是word、pdf、txt格式文件，编码可以是gbk、unicode、utf8、big5等）
    - 输出：txt文件，utf8编码
4. 汉字拼音查询：
    - 输入：汉字
    - 输出：拼音
5. 按照拼音对汉字进行排序

该项目包含如下文件：
- encoding_functions.py：实现功能1、2
- file_encoding_transfer.py：实现功能3
- pinyin_seq.py：实现功能4、5
- FileEncoding.py：UI实现
- FileEncoding.exe：可执行文件
- pinyin_data.json, 汉字字音数据库.txt：程序功能的依赖文件，请勿删除