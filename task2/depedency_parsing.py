# encoding: utf8
# dependency parsing for the sentence in the task2.
# powered by spacy.

import json # read json.
import jsonlines # write jsonlines.
import pandas as pd # read excel.
import spacy # dependency parsing.
from spacy.tokens import Doc # add the custom words to the vocabulary.
import config
import custom_words

# load the spacy model.
nlp = spacy.load(config.ZH_MODEL)
# Add new words to the vocabulary with specified part-of-speech tags
custom_words = custom_words.CUSTOM_WORDS

# Add the custom words to the spacy vocabulary
for word, attrs in custom_words.items():
    doc = Doc(nlp.vocab, words=[word])
    doc[0].tag_ = attrs[config.POS]

def dependency_parsing(sentence: str) -> dict[str, list[str]| list[dict] | str]:
    """对句子执行依存句法分析
    Args:
        sentence (str): 句子
    Returns:
        dict: 依存句法分析结果"""
    # do the word segmentation and dependency parsing.
    doc = nlp(sentence)
    token_index = {token: i for i, token in enumerate(doc)}
    # 整理分词、词性标注和依存句法分析结果
    result: dict[str, list[str]| list[dict] | str] = {
        # 句子
        config.SENTENCE: sentence,
        # 分词结果
        config.SEG: [token.text for token in doc],
        # 词性标注结果
        config.POS: [token.pos_ for token in doc],
        # 依存句法分析结果
        config.DEP: [{config.HEAD:token_index[token.head], config.WORD:i, config.RELATION:token.dep_} for i, token in enumerate(doc)]
    }
    return result

result: list[dict] = [] # the result of the dependency parsing.
jl_res: list[dict] = [] # the result for the jsonlines.
df = pd.read_excel(config.ORIGIN_DATA_PATH) # read the data from the excel.
# do the dependency parsing for the context1.
context1_res = map(dependency_parsing, df[config.CONTEXT1])
# do the dependency parsing for the context2.
context2_res = map(dependency_parsing, df[config.CONTEXT2])
# merge the result.
for i, (res1, res2, j) in enumerate(zip(context1_res, context2_res, df[config.JUDGE])):
    # 结果中添加qid和判断结果后添加到result中
    result.append({config.QID:i, config.CONTEXT1: res1, config.CONTEXT2: res2, config.JUDGE: j})
    # 将结果转换为jsonlines格式
    jl_res.append({config.QID:i, config.PAIR:1, config.TEXT:res1[config.SENTENCE], config.SEG:res1[config.SEG], config.POS:res1[config.POS], config.LABEL:[]})
    jl_res.append({config.QID:i, config.PAIR:2, config.TEXT:res2[config.SENTENCE], config.SEG:res2[config.SEG], config.POS:res2[config.POS], config.LABEL:[]})

# save the result to the json file.
with open(config.DEP_RESULT_PATH, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
    print(f"the dependency parsing result has been saved to {config.DEP_RESULT_PATH}")

# save the result to the jsonlines file.
with jsonlines.open(config.ANNOTATE_NEED_PATH, 'w') as writer:
    writer.write_all(jl_res)
    print(f"the jsonlines file has been saved to {config.ANNOTATE_NEED_PATH}")