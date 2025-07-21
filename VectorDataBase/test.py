# 加载已有的 Chroma 向量数据库
from langchain_chroma import Chroma

from VectorDataBase.VectorStorage import persist_path, embedding

vectordb = Chroma(persist_directory=persist_path, embedding_function=embedding)

# 执行向量相似度查询
query = "云南招聘时间？"
results = vectordb.similarity_search(query, k=3)

for i, doc in enumerate(results, 1):###编号从一开始
    print(f"{i}. {doc.page_content}\n")