# encoding: utf8
# 用于调用模型的API

from typing_extensions import deprecated
import requests
import json
import config

TEMPERATURE = 0.1 # 固定温度；降低温度，提高生成文本的准确性

def call_gpt(text: str, api: str) -> dict:
    url = 'https://api.zhizengzeng.com/v1/chat/completions'
    header = {
        'Content-Type': 'application/json', 
        'Authorization': f'Bearer {api}', 
    }
    body = {
        'model': 'gpt-4o', 
        'messages': [
            {
                'role': 'system',
                'content': '你是一位了解空间表达的人。请只用True或False回答问题。'
            },
            {
                'role': 'user', 
                'content': text
            }
        ], 
        'temperature': TEMPERATURE, # 降低温度，提高生成文本的准确性
    }
    response = requests.post(url, headers=header, json=body)
    return response.json()

def call_gemma(text: str, api: str, secret_api: str) -> dict:
    def get_access():
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": api, "client_secret": secret_api}
        return str(requests.post(url, params=params).json().get("access_token"))

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/gemma_7b_it"
    header = {'Content-Type': 'application/json'}
    query = {'access_token': get_access()}
    body = {
        'messages': [
            {
                'role': 'user',
                'content': text
            }
        ],
        'temperature': TEMPERATURE, # 降低温度，提高生成文本的准确性
        'system': '你是一位了解空间表达的人。请只用True或False回答问题。',
    }
    response = requests.post(url, headers=header, params=query, data=json.dumps(body))
    return response.json()

def call_llama3(text: str, api: str, secret_api: str) -> dict:
    def get_access():
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": api, "client_secret": secret_api}
        return str(requests.post(url, params=params).json().get("access_token"))

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/llama_3_70b"
    header = {'Content-Type': 'application/json'}
    query = {'access_token': get_access()}
    body = {
        'messages': [
            {
                'role': 'user',
                'content': text
            }
        ],
        'temperature': TEMPERATURE, # 降低温度，提高生成文本的准确性
        'system': '你是一位了解空间表达的人。请只用True或False回答问题。',
    }
    response = requests.post(url, headers=header, params=query, data=json.dumps(body))
    return response.json()

def call_ernie(text: str, api: str, secret_api: str) -> dict:
    def get_access():
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": api, "client_secret": secret_api}
        return str(requests.post(url, params=params).json().get("access_token"))

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro_preemptible"
    header = {'Content-Type': 'application/json'}
    query = {'access_token': get_access()}
    body = {
        'messages': [
            {
                'role': 'user',
                'content': text
            }
        ],
        'temperature': TEMPERATURE, # 降低温度，提高生成文本的准确性
        'system': '你是一位了解空间表达的人。请只用True或False回答问题。',
    }
    response = requests.post(url, headers=header, params=query, data=json.dumps(body))
    return response.json()

def call_claude(text: str, api: str) -> dict:
    headers = {
        'Anthropic-Version': '2023-06-01',
        'Authorization': f'Bearer {api}',
    }
    data = {
        "model": "claude-3-opus-20240229",
        "temperature": TEMPERATURE, # 降低温度，提高生成文本的准确性
        "messages": [
            {"role": "system", "content": "你是一位了解空间表达的人。请只用True或False回答问题。"}, 
            {"role": "user", "content": text}, 
        ]
    }
    url = 'https://api.zhizengzeng.com/v1/chat/completions'
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def call_api(text: str, model_name: config.ModelNames) -> dict:
    def get_api(api_file: str) -> str:
        with open(api_file, 'r') as f:
            return f.read().strip()
        
    if model_name == 'ernie':
        api = get_api(config.ERNIE_API_FILE)
        secret_api = get_api(config.ERNIE_SECRET_API_FILE)
        return call_ernie(text, api, secret_api)
    elif model_name == 'claude':
        api = get_api(config.GPT_API_FILE)
        return call_claude(text, api)
    elif model_name == 'llama3':
        api = get_api(config.ERNIE_API_FILE)
        secret_api = get_api(config.ERNIE_SECRET_API_FILE)
        return call_llama3(text, api, secret_api)
    elif model_name == 'gemma':
        api = get_api(config.ERNIE_API_FILE)
        secret_api = get_api(config.ERNIE_SECRET_API_FILE)
        return call_gemma(text, api, secret_api)
    elif model_name == 'gpt4o':
        api = get_api(config.GPT_API_FILE)
        return call_gpt(text, api)
    else:
        raise ValueError(f"Unknown model name: {model_name}")