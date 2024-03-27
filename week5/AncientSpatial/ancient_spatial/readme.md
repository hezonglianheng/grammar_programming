# 古代汉语方所表达查询系统

秦宇航 hezonglianheng@stu.pku.edu.cn

本系统是古代汉语方所表达查询系统，希望实现如下功能：
1. 展示已有的古代汉语方位表达研究成果
2. 提供简单的查询接口
3. 展示对研究结果的统计分析

目前的主要操作如下：

## 单语查询

目前仅支持查询包含输入字符、空间信息角色为下拉选项中角色的文本。  
查询后，每页展示30个结果，查询词会高亮展示，页面左上会显示具体命中数量及当前查看的命中的编号。  
用户可以点击“上下文”按钮了解查询的详细信息。

## 古今对照（待完善）

## 语料统计（待完善）

## 使用说明（待完善）

## 使用方法
### 数据库添加方法
1. 根据本仓库中的`requirements.txt`配置环境（Python3.12）.
2. 将使用[doccano](https://github.com/doccano/doccano)工具标注的数据放入`corpus\jsonline_corpus\admin.jsonl`.
3. 启动`py extract_ancient.py`.
4. 启动`py update_data.py -a -r`.
5. 数据库更新完成.
### 服务器启动方法
1. 根据本仓库中的`requirements.txt`配置环境（Python3.12）.
2. 在命令行中`cd`到本文件所在目录下.
3. 在保证环境激活（特别是虚拟环境）的前提下，在命令行中输入命令`py manage.py runserver [port]`。端口port可以自行指定，默认为8000.
4. 在浏览器中输入`localhost:[port]`（端口port在3中已经指定好），启动程序.