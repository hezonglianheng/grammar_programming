# encoding: utf8
# 用于统计结果，主要统计few-shot的结果

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, cohen_kappa_score
import json
import re
from pathlib import Path
from collections import defaultdict
import sys
import config

def extract_answer(output: str) -> bool:
    """从一条输出中获得答案"""
    pattern = r"(True|true|False|false)"
    match = re.findall(pattern, output)
    yes_no_pattern = r"(yes|no|Yes|No|YES|NO|unlikely)"
    yes_no_match = re.findall(yes_no_pattern, output)
    if match:
        if match[-1] == "True" or match[-1] == "true":
            return True
        else:
            return False
    elif yes_no_match:
        if yes_no_match[-1] == "yes" or yes_no_match[-1] == "Yes" or yes_no_match[-1] == "YES":
            return True
        else:
            return False
    else:
        raise ValueError(f"未能从输出'{output}'中提取答案！")

def statistics(judge: list[bool], answer: list[bool]) -> dict:
    """统计结果"""
    result = {
        'total': len(judge), # 总数
        'true_total': sum(judge), # 参考答案为True的总数
        'false_total': len(judge) - sum(judge), # 参考答案为False的总数
        'true_predict': sum(answer), # 模型预测为True的总数
        'false_predict': len(answer) - sum(answer), # 模型预测为False的总数
        'accuracy': accuracy_score(judge, answer),
        'true_accuracy': sum([j and a for j, a in zip(judge, answer)]) / sum(judge) if sum(judge) != 0 else 0, # 预测为True且正确的数量
        'false_accuracy': sum([not j and not a for j, a in zip(judge, answer)]) / (len(judge) - sum(judge)) if len(judge) - sum(judge) != 0 else 0, # 预测为False且正确的数量
        'precision': precision_score(judge, answer, zero_division=0),
        'recall': recall_score(judge, answer, zero_division=0),
        'f1': f1_score(judge, answer, zero_division=0),
        'kappa': cohen_kappa_score(judge, answer, labels=[True, False]),
    }
    return result

def main(model_names: config.ModelNames, shot_type: config.ShotType):
    """对模型需要的参数做统计"""
    json_path = Path(config.RESULT_DIR) / f"{model_names}_{shot_type}.json"

    with open(json_path, 'r', encoding='utf8') as f:
        data = json.load(f)

    # 从data中提取参考答案和模型的答案
    judge_lst: list[bool] = [i[config.JUDGE] for i in data]
    gpt_form = ['gpt4o', 'moonshot', 'claude']
    ernie_form = ['ernie', 'gemma', 'llama3']
    if model_names in gpt_form:
        answer_lst: list[bool] = [extract_answer(i['response']['choices'][0]['message']['content']) for i in data]
    elif model_names in ernie_form:
        answer_lst: list[bool] = [extract_answer(i['response']['result']) for i in data]
    else:
        raise ValueError(f"模型名称{model_names}不在gpt_form和ernie_form中，请检查！")

    # 统计结果
    result = statistics(judge_lst, answer_lst)

    # 读取测试数据
    with open(config.TEST_DATA, 'r', encoding='utf8') as f:
        test_data = json.load(f)

    # 获得schema_pairs
    schema_pairs = [f'{i[config.CONTEXT1][config.SCHEMA]}-{i[config.CONTEXT2][config.SCHEMA]}' for i in test_data]
    # 分类defaultdict
    grouped_dict = defaultdict(lambda: {'judge': [], 'answer': []})
    for p, j, a in zip(schema_pairs, judge_lst, answer_lst):
        grouped_dict[p]['judge'].append(j)
        grouped_dict[p]['answer'].append(a)

    # 分项统计结果
    statistics_dict = {k: statistics(v['judge'], v['answer']) for k, v in grouped_dict.items()}
    # 添加总统计结果
    statistics_dict |= {'total': result}
    # 保存统计结果
    statistics_df = pd.DataFrame(statistics_dict).T
    with pd.ExcelWriter(config.STATISTICS_FILE, mode='a', if_sheet_exists='replace') as writer:
        statistics_df.to_excel(writer, sheet_name=f"{model_names}_{shot_type}")

if __name__ == '__main__':
    model_names: config.ModelNames = sys.argv[1]
    shot_type: config.ShotType = sys.argv[2]
    main(model_names, shot_type)