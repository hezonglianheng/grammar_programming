# encoding: utf8
# 配置文件

from typing import Literal

# 模型名称
ModelNames = Literal['ernie', 'claude', 'llama3', 'gemma', 'gpt4o', 'moonshot']

# LLM返回类型
LLMResponse = Literal['error', 'message']

# api-keys
CLAUDE_API_FILE = r'api_keys\claude-api.txt'
ERNIE_API_FILE = r'api_keys\ernie-api.txt'
ERNIE_SECRET_API_FILE = r'api_keys\ernie-secret-api.txt'
GPT_API_FILE = r'api_keys\gpt-api.txt'

# 测试数据
TEST_DATA = r'dep_ann_result.json'
# 测试数据字段
CONTEXT1 = 'context1'
CONTEXT2 = 'context2'
SENTENCE = 'sentence'
JUDGE = 'judge'

# 整理结果
RESULT_DIR = r'llm_results'