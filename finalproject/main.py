from contextlib import asynccontextmanager
from typing import List, Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import origins
from rag_answer import router
from vectordb_services import initialize_vector_db_and_embeddings
from dotenv import load_dotenv
load_dotenv()

# app = FastAPI()
# app.include_router(router, prefix="/api", tags=["RAG"])
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # 调用初始化函数，加载嵌入模型和 ChromaDB 向量存储
#     initialize_vector_db_and_embeddings()
#     yield
# app = FastAPI(lifespan=lifespan)
# # --- 运行FastAPI应用 ---
# # 要运行此应用，请保存为例如 `main.py`
# # 然后在终端中执行: uvicorn main:app --reload

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan 启动：开始初始化向量数据库和嵌入模型")
    initialize_vector_db_and_embeddings()
    print("lifespan 初始化完成，应用启动")
    yield
    print("lifespan 结束，应用关闭")

app = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(router, prefix="/api", tags=["RAG"])

# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8090, reload=True)