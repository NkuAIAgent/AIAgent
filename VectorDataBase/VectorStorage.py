import os
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# 设置路径
folder_path = r"../resources/txt_out_dir"
embedding_model_path = r"../embedding_models/moka/m3e-base"
persist_path = r"../resources/persist_path/chroma_db"


# 1. 加载 embedding 模型
embedding = HuggingFaceEmbeddings(model_name=embedding_model_path)


# 2. 加载文本数据
all_docs = []
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):###只加载以txt结尾文件
        loader = TextLoader(os.path.join(folder_path, filename), encoding="utf-8")
        docs = loader.load()
        all_docs.extend(docs)

# 3. 文本分块（可调节 chunk_size）               500字一块         可重叠50字
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
split_docs = text_splitter.split_documents(all_docs)####切块
####可以按照字符标点
# 4. 构建向量数据库并持久化
vectordb = Chroma.from_documents(split_docs, embedding=embedding, persist_directory=persist_path)
vectordb.persist()  # 持久化存储
print("Chroma 向量库构建完毕并已保存")

