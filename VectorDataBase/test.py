# 加载已有的 Chroma 向量数据库
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# from VectorDataBase.VectorStorage import persist_path, embedding
embedding_model_path = r"../embedding_models/moka/m3e-base"
persist_path = r"../resources/persist_path/chroma_db"
# 1. 加载 embedding 模型
embedding = HuggingFaceEmbeddings(model_name=embedding_model_path)
vectordb = Chroma(persist_directory=persist_path, embedding_function=embedding)

# 执行向量相似度查询
query = ("请列举软件学院招聘信息？")
results = vectordb.similarity_search(query, k=3)

for i, doc in enumerate(results, 1):###编号从一开始
    print(f"{i}. {doc.page_content}\n")
