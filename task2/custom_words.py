# encoding: utf8
# custom words for the dependency parsing.
# powered by spacy.
# 目前暂时不使用

import config

# Add new words to the vocabulary with specified part-of-speech tags
CUSTOM_WORDS = {
    # an example of the custom words.
    # "GitHub": {config.POS: config.PROPN},
    "金刚钻": {config.POS: config.NOUN},
}