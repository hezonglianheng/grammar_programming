# encoding: utf8
# 用于通过模型API获得答案

import config
import callapi
import getinput
import json
from tqdm import tqdm
import time
import sys
from typing import Literal
import random
from pathlib import Path

ShotType = Literal['zero', 'few']

def main(model_name: config.ModelNames, add_shot: bool = True):
    with open(config.TEST_DATA, 'r', encoding='utf8') as f:
        data: list[dict] = json.load(f)

    llm_inputs = [getinput.get_input(i[config.CONTEXT1][config.SENTENCE], i[config.CONTEXT2][config.SENTENCE]) for i in data]
    if add_shot:
        llm_inputs = [getinput.add_shot() + i for i in llm_inputs]

    responses = []
    for i in tqdm(llm_inputs, desc='调用API'):
        responses.append(callapi.call_api(i, model_name))
        time.sleep(random.uniform(.1, .9)) # 随机等待时间

    results = [
        {
            'context1': data[i][config.CONTEXT1][config.SENTENCE],
            'context2': data[i][config.CONTEXT2][config.SENTENCE],
            'judge': data[i][config.JUDGE],
            'response': responses[i],
        }
        for i in range(len(data))
    ]
    res_file = Path(config.RESULT_DIR) / (f"{model_name}" + ('_few' if add_shot else '_zero') + '.json')
    with open(res_file, 'w', encoding='utf8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    model_name = sys.argv[1]
    if len(sys.argv) == 3:
        add_shot: ShotType = sys.argv[2]
        if add_shot == 'zero':
            main(model_name, add_shot=False)
        else:
            main(model_name, add_shot=True)
    else:
        main(model_name, add_shot=True)
