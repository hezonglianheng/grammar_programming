# encoding: utf8
# config for scripts in the task2.

# 文件路径
ORIGIN_DATA_PATH = r'spatial_synonym_data.xlsx'
DEP_RESULT_PATH = r'dep_result.json'
ANNOTATE_NEED_PATH = r'annotate_need.jsonl'
ANNOTATE_RES_PATH = r'annotate_result.jsonl'
FINAL_RES_PATH = r'final_result.json'

ZH_MODEL = 'zh_core_web_md' # 中文模型名称

# excel列名，句对字段名称
QID = 'qid'
CONTEXT1 = 'context1'
CONTEXT2 = 'context2'
JUDGE = 'judge'

# json文件字段名称
# 单句字段名称
SENTENCE = 'sentence' # 句子
SEG = 'seg' # 分词结果
POS = 'pos' # 词性标注结果
DEP = 'dep' # 依存句法分析结果
# 依存句法分析结果中的字段名称
HEAD = 'head' # 依存句法分析结果中的头词
RELATION = 'relation' # 依存句法分析结果中的关系
WORD = 'word' # 依存句法分析结果中的词
# 空间信息的字段名称
SPATIAL = 'spatial' # 空间信息
TRAJECTORY = 'trajectory' # 射体
LANDMARK = 'landmark' # 地标
EVENT = 'event' # 事件

# jsonlines文件字段名称
PAIR = 'pair' # 句对中的编号
TEXT = 'text' # 句子
LABEL = 'label' # 标签

# 依存句法分析结果中的关系
# 特殊关系ROOT
ROOT = 'ROOT'

# 词类别
NOUN = 'NOUN' # 名词
PROPN = 'PROPN' # 专有名词
VERB = 'VERB' # 动词
ADJ = 'ADJ' # 形容词
ADV = 'ADV' # 副词
PRON = 'PRON' # 代词
DET = 'DET' # 限定词