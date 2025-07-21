import os
'''----------------------CORS配置---------------------'''
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

'''----------------------ChromaDB 配置----------------------'''
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "")
print(EMBEDDING_MODEL_NAME)
'''----------------------LLM API----------------------'''
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "")

OPENAI_APIKEY_FREE = os.getenv("OPENAI_APIKEY_FREE", "")
OPENAI_BASE_URL_FREE = os.getenv("OPENAI_BASE_URL_FREE", "")

QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "")