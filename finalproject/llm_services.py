import httpx
import json
from fastapi.responses import StreamingResponse
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, OPENAI_APIKEY_FREE, OPENAI_BASE_URL_FREE, QWEN_API_KEY, \
    QWEN_BASE_URL

async def call_deepseek_chat(prompt: str):
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
        "stream": True  # 开启流式
    }

    async def stream_generator():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", DEEPSEEK_API_URL, headers=headers, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line.removeprefix("data: ").strip()
                        if data == "[DONE]":
                            break
                        obj = json.loads(data)
                        content = obj['choices'][0]['delta'].get("content", "")
                        if content:
                            yield content

    return stream_generator()

async def call_openai_chat(prompt: str):
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
        "stream": True  # 开启流式
    }

    async def stream_generator():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", OPENAI_BASE_URL_FREE, headers=headers, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line.removeprefix("data: ").strip()
                        if data == "[DONE]":
                            break
                        obj = json.loads(data)
                        content = obj['choices'][0]['delta'].get("content", "")
                        if content:
                            yield content

    return stream_generator()

async def call_qwen_chat(prompt: str):
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
        "stream": True  # 开启流式
    }

    async def stream_generator():
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", QWEN_BASE_URL, headers=headers, json=payload) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line.removeprefix("data: ").strip()
                        if data == "[DONE]":
                            break
                        obj = json.loads(data)
                        content = obj['choices'][0]['delta'].get("content", "")
                        if content:
                            yield content

    return stream_generator()


def call_llm(model_name: str):
    if model_name == "deepseek-chat":
        return call_deepseek_chat
    elif model_name == "chat-gpt-3.5-turbo":
        return call_openai_chat
    elif model_name == "qwen-chat":
        return call_qwen_chat
    else:
        print("Calling Error")

