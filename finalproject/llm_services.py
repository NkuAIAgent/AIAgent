import httpx
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, OPENAI_APIKEY_FREE, OPENAI_BASE_URL_FREE, QWEN_API_KEY, \
    QWEN_BASE_URL

async def call_deepseek_chat(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        response_data = response.json()
        if 'choices' in response_data and response_data['choices']:
            llm_content = response_data['choices'][0]['message']['content']
            return llm_content
        else:
            return "DeepSeek API 返回了空内容。"

async def call_openai_chat(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_APIKEY_FREE}"
    }
    payload = {
        "model": "chat-gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(OPENAI_BASE_URL_FREE, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        response_data = response.json()
        if 'choices' in response_data and response_data['choices']:
            llm_content = response_data['choices'][0]['message']['content']
            return llm_content
        else:
            return "OPENAI API 返回了空内容。"

async def call_qwen_chat(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {QWEN_API_KEY}"
    }
    payload = {
        "model": "qwen-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }

    async with httpx.AsyncClient() as http_client:
        response = await http_client.post(QWEN_BASE_URL, headers=headers, json=payload, timeout=30.0)
        response.raise_for_status()
        response_data = response.json()
        if 'choices' in response_data and response_data['choices']:
            llm_content = response_data['choices'][0]['message']['content']
            return llm_content
        else:
            return "QWEN API 返回了空内容。"


async def call_llm(model_name: str, prompt: str) -> str:
    if model_name == "deepseek-chat":
        print("Calling DeepSeek Chat")
        return await call_deepseek_chat(prompt)
    elif model_name == "chat-gpt-3.5-turbo":
        return await call_openai_chat(prompt)
    elif model_name == "qwen-chat":
        return await call_qwen_chat(prompt)