# 异形同义语料精标注
秦宇航 hezonglianheng@stu.pku.edu.cn

## 工作相关情况说明
### 依存句法分析
本工作使用spacy工具进行依存句法分析。 
本工作使用的spacy模型为`zh_core_web_md`.  
出于知识产权考虑，本仓库不提供工具文件。请访问[spacy官网](http://spacy.io)获取详细信息。

### 空间信息标注
本工作使用[Doccano](https://github.com/doccano/doccano)工具进行空间信息标注。

## 语料标注相关内容
与本次语料标注相关的主要文件如下表所示。

| 文件路径                         | 文件功能                                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| [corpus\spatial_synonym_data.xlsx](corpus\spatial_synonym_data.xlsx) | 存放收集的初始语料、形义关系及图式标注结果。                                                                                    |
| [corpus\annotation_result.jsonl](corpus\annotation_result.jsonl)   | 空间角色标注结果文件。                                                                                                          |
| [corpus\dep_ann_result.json](corpus\dep_ann_result.json)       | 全部标注结果文件。                                                                                                              |
| pictures\without_spatial        | 存放标注结果可视化的，不含空间角色标注结果的html文件。                                                                          |
| pictures\with_spatial            | 存放标注结果可视化的，含有空间角色标注结果的html文件。                                                                          |
| [dependency_parsing.py](dependency_parsing.py)            | 执行自动分词和依存句法标注，标注结果存于corpus\dep_result.json和corpus\annotate_need.jsonl（用于[Doccano](https://github.com/doccano/doccano)标注工具标注空间角色）。 |
| [merge_annotations.py](merge_annotations.py)             | 用于合并自动分词和依存句法标注、空间角色标注结果，放入corpus\dep_ann_result.json。                                              |
| [visualization.py](visualization.py)                 | 将空间角色标注结果体现在依存句法标注的可视化文件中。                                                                            |

## 数据操作命令
目前，系统后台的数据更新主要通过程序move_corpus2app.py进行。该程序提供的命令及对应的功能如下表所示。

| 具体命令                                               | 命令参数                              | 命令功能                           |
|--------------------------------------------------------|---------------------------------------|------------------------------------|
| `python move_corpus2app.py add [rp_pair] [file_path]`    | `rp_pair`: 需要操作的替换对。           | 为指定的方位词替换对添加语料信息。 |
|                                                        | `file_path`: 包含句子对的json文件路径。 |                                    |
| `python move_corpus2app.py delete [rp_pair]`             | `rp_pair`: 需要操作的替换对。           | 删除指定的方位词替换对的语料信息   |
| `python move_corpus2app.py show`                         | 无                                    | 显示所有已有的替换对。             |
| `python move_corpus2app.py update [rp_pair] [file_path]` | `rp_pair`: 需要操作的替换对。           | 更新指定的方位词替换对的语料信息。 |
|                                                        | `file_path`: 包含句子对的json文件路径。 |                                    |
| `python move_corpus2app.py help [func_name]`             | `func_name`: 需要查看帮助的函数名。     | 查看指定函数的帮助信息。           |

## 数据查看
执行`python manage.py runserver`命令后，浏览器访问<http://127.0.0.1:8000/>查看。