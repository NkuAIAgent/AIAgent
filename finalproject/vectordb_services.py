import os
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_DB_PATH, EMBEDDING_MODEL_NAME

'''
--------- 嵌入模型和 ChromaDB 配置初始化 ---------
'''
lc_embedding_model = None
vectorstore = None
persist_path = r"../resources/persist_path/chroma_db"
def initialize_vector_db_and_embeddings():
    global lc_embedding_model, vectorstore
    # 1. 初始化 LangChain 的嵌入模型
    lc_embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    # print("22")
    # print(lc_embedding_model.model_name)
    # 2. 初始化 LangChain 的 Chroma 向量存储
    # 获取 ChromaDB 存储的绝对路径


    # 使用 persist_directory 和 embedding_function 参数初始化 Chroma
    # Chroma 会自动处理底层客户端的创建和集合的加载
    vectorstore = Chroma(
        persist_directory=persist_path,
        embedding_function=lc_embedding_model,
    )
    print("11")