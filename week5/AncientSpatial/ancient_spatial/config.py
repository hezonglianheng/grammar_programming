# encoding: utf8
# 文件路径
ANNOTATED = r'corpus\jsonline_corpus\admin.jsonl' # 标注文件
ANNOTATED_DIR = r'corpus\jsonline_corpus' # 标注文件夹
JSONL_SUFFIX = '.jsonl' # jsonlines文件后缀
ANCIENT_RES = r"corpus\json_corpus\ancient.json" # 古代汉语提取结果

# jsonlines字段名称
TEXT = 'text' # 文本内容
ENTITIES = 'entities' # 实体
RELATIONS = 'relations' # 关系
SOURCE = 'source'

# entities字段名称
ID = 'id'
LABEL = 'label'
START_OFFSET = 'start_offset'
END_OFFSET = 'end_offset'
OFFSET_RANGE = [START_OFFSET, END_OFFSET]
# entity types
TRAJECTORY = "trajectory"
LANDMARK = "landmark"
EVENT = "event"
LOCATION = "location"
PREPOSITION = "preposition"

# relations字段名称
FROM_ID = 'from_id'
TO_ID = 'to_id'
TYPE = 'type'
# relation types
isPlace = "isPlace"
isPart = "isPart" # 新增：部件处所关系
isDeparture = "isDeparture"
isDestination = "isDestination"
isOrientation = "isOrientation"
isDirection = "isDirection"
isPath = "isPath"
isPreposition = "isPreposition"
isLocation = "isLocation"
isAction = "isAction"
isTranslation = "isTranslation"
spatial_relation = [
    isPlace, 
    isPart,
    isDeparture, 
    isDestination, 
    isOrientation, 
    isDirection, 
    isPath,
]

# 新建的字段名称
ANCIENT_TEXT = 'ancient_text'
TITLE = 'title'
SUBTITLE = 'subtitle'
SpaCE = 'space'
TR1 = "trajectory1"
TR2 = "trajectory2"
ROLES = [
    TR1, 
    TR2, 
    LANDMARK, 
    EVENT, 
    PREPOSITION, 
    LOCATION
]

# 表达模式各元素
PATTERN_DICT = {
    TR1: "tr",
    TR2: "tr",
    LANDMARK: "lm",
    EVENT: "ev",
    LOCATION: "lo",
    PREPOSITION: "pr",
}
PATTERN_JOIN = "+"
PATTERN2ROLE = {
    "tr": [TR1, TR2],
    "lm": [LANDMARK],
    "ev": [EVENT],
    "lo": [LOCATION],
    "pr": [PREPOSITION],
}
# relation to Chinese
RELATION_CHINESE = {
    isPlace: "处所",
    isPart: "部件处所",
    isDeparture: "起点",
    isDestination: "终点",
    isOrientation: "朝向",
    isDirection: "方向",
    isPath: "路径",
}
# 与统计表格中的关系对应
RELATION_EN = {
    isPlace: "place",
    isPart: "part",
    isDeparture: "departure",
    isDestination: "destination",
    isOrientation: "orientation",
    isDirection: "direction",
    isPath: "path",
}
MODE_CHINESE = {
    'accurate': '精确',
    'fuzzy': '模糊',
}