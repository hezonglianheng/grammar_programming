# encoding: utf8
# 将原有句子对改造为带有提示语的试题

HINT = '阅读context1及context2，回答question。'
QUESTION = '上述两个句子是否有可能表达相同的空间场景？'

def get_input(context1: str, context2: str) -> str:
    return f'{HINT}\ncontext1: {context1}\ncontext2: {context2}\nquestion: {QUESTION}'

def add_shot():
    return """阅读context1及context2，回答question。
    context1: 蒋一轮倚在柳树下，用的是让桑桑最着迷的姿势：两腿微微交叉着。
    context2: 蒋一轮倚在柳树旁，用的是让桑桑最着迷的姿势：两腿微微交叉着。
    question: 上述两个句子是否有可能表达相同的空间场景？
    answer: True\n
    阅读context1及context2，回答question。
    context1: 家里两只淘气的小猫钻到婴儿床里，翻滚嬉闹了好半天。
    context2: 家里两只淘气的小猫钻到婴儿床下，翻滚嬉闹了好半天。
    question: 上述两个句子是否有可能表达相同的空间场景？
    answer: False\n"""