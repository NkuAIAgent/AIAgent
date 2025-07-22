# import os
# from langchain_community.document_loaders import TextLoader
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
#
#
# # 设置路径
# folder_path = r"../resources/txt_out_dir"
# embedding_model_path = r"../embedding_models/moka/m3e-base"
# persist_path = r"../resources/persist_path/chroma_db"
#
#
# # 1. 加载 embedding 模型
# embedding = HuggingFaceEmbeddings(model_name=embedding_model_path)
#
#
# # 2. 加载文本数据
# all_docs = []
# i=1
# for filename in os.listdir(folder_path):
#     if filename.endswith(".txt"):###只加载以txt结尾文件
#         loader = TextLoader(os.path.join(folder_path, filename), encoding="utf-8")
#         docs = loader.load()
#         all_docs.extend(docs)
#         print(f"已加载第 {i}条")
#         i+=1
#         break###只加载第一条
#
# # 3. 文本分块（可调节 chunk_size）               500字一块         可重叠50字
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
# print("文本分块")
# split_docs = text_splitter.split_documents(all_docs)####切块
# print("文本分块完毕")
# print(split_docs)
# ####可以按照字符标点
# # 4. 构建向量数据库并持久化
# # vectordb = Chroma.from_documents(split_docs, embedding=embedding, persist_directory=persist_path)
# # print("Chroma 向量库构建完毕")
# # vectordb.persist()  # 持久化存储
# # print("Chroma 向量库构建完毕并已保存")
#

import os
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from VectorDataBase.Clear import clear


def storage():
# 路径配置（相对路径）
     embedding_model_path = r"../embedding_models/moka/m3e-base"
     txt_dir =  r"../resources/txt_out_dir"
     persist_dir =  r"../resources/persist_path/chroma_db"

     # 初始化embedding模型
     embedding = HuggingFaceEmbeddings(model_name=str(embedding_model_path))

     # 初始化Chroma向量数据库
     vectordb = Chroma(
         embedding_function=embedding,
         persist_directory=str(persist_dir)
     )

     # 定义函数用于去除字段前缀
     def clean_prefix(text: str, prefix: str) -> str:
         if text.startswith(prefix):        # 判断 text 是否以 prefix 开头
             return text[len(prefix):].strip()  # 去掉 prefix 后剩余部分，并去除首尾空白
         return text.strip()                # 如果没有 prefix，直接去除空白返回

     # 逐个处理txt文件

     # txt_dir 是一个 Path 对象，表示某个文件夹路径；
     #
     # .glob("*.txt") 是 Path 提供的方法，功能是查找匹配特定模式（这里是所有以 .txt 结尾的文件）；
     #
     # 这个语句返回一个生成器（iterator），你用 for 循环依次取出每个符合条件的文件。
     txt_dir = Path(txt_dir)
     i=1
     for file in txt_dir.glob("*.txt"):
         with open(file, "r", encoding="utf-8") as f:
             print(f"正在处理第{i}个文件")
             i+=1
             lines = [line.strip() for line in f.readlines() if line.strip()]
             if "标题:未知标题" in lines[0]:
                 print(f"文件 {file.name} 标题未知，跳过。")
                 continue
             if len(lines) < 4:
                 print(f"文件 {file.name} 格式错误，跳过。")
                 continue

             # 去除字段前缀
             title = clean_prefix(lines[0], "标题:")
             content = lines[1]
             source = clean_prefix(lines[2], "原文链接:")
             pub_time = clean_prefix(lines[3], "发布时间:")

             metadata = {
                 "title": title,
                ## "source": source,
                 "pub_time": pub_time,
                 "file_name": file.name
             }
             content=content+title+pub_time+file.name
             doc = Document(page_content=content, metadata=metadata)
             vectordb.add_documents([doc])
             print(f"已添加文档：{file.name}")

     # 持久化保存
     vectordb.persist()
     print(" 全部文档处理完成并保存。")
     clear()
     open("../resources/json_input_path.json", "w", encoding="utf-8").close()


