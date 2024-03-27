# encoding: utf8
# 文件路径
ANNOTATED = r'corpus\jsonline_corpus\admin.jsonl' # 标注文件
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
