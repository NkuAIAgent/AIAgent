from fastapi import HTTPException, APIRouter
from models import RAGQueryPayload
from llm_services import call_llm
import vectordb_services
from typing import List, Dict, Any

router = APIRouter()
@router.post("/rag_answer_deepseek/")
async def rag_answer_deepseek(payload: RAGQueryPayload):
    print(
        f"DEBUG: Request received for RAG answer. User query: '{payload.user_query}', LLM model: '{payload.llm_model}'")
    ##如果向量数据库或者嵌入模型没有初始化，抛出异常
    if vectordb_services.vectorstore is None:
        raise HTTPException(status_code=500,
                            detail="ChromaDB vectorstore not initialized. Please check server logs for initialization errors.")
    if vectordb_services.lc_embedding_model is None:
        raise HTTPException(status_code=500,
                            detail="Embedding model not loaded. Please check server logs for initialization errors.")

    # 根据用户查询payload.user_query，检索top - k相关文档
    # 返回的docs是一个列表，每个元素是带有page_content和metadata的文档对象

    docs = vectordb_services.vectorstore.similarity_search(query=payload.user_query, k=payload.n_results)


    #构建检索到的文档内容初始化一个空字符串，用来拼接所有检索到的文档文本内容。
    # 这个字符串会被用来构造传给大语言模型（LLM）的上下文提示（prompt）。
    #例如把每个文档片段的文本用一定格式加进去，形成一个完整上下文。
    retrieved_documents_content = ""

    # 初始化一个空列表，存储每个检索到的文档的纯文本内容。
    #
    # 这个列表一般用于把文档内容原样返回给前端界面，方便前端展示。
    retrieved_docs_for_frontend = []

    # 初始化一个空列表，存储每个文档对应的元数据（metadata），比如文档来源、时间戳、标题等。
    #
    # 元数据通常用来辅助前端展示更丰富的信息，比如显示文档出处
    retrieved_metadatas_for_frontend = []

    if docs:
        ###遍历所有检索到的文档，i 是索引，doc 是每个文档对象
        for i, doc in enumerate(docs):
            # LangChain 的 Document 对象有 page_content 和 metadata 属性
            doc_content = doc.page_content

            # 提取文档的纯文本内容（page_content）
            #
            # 提取文档的元数据（metadata），通常是字典，含文档来源、时间、标题等信息
            metadata = doc.metadata
            # 打印调试信息，显示当前文档的前100字符内容和元数据信息，方便开发调试
            print(f"DEBUG: Retrieved Doc {i + 1}: '{doc_content[:100]}...' | Metadata: {metadata}")

            # 构建给 LLM 的上下文
            # 把文档内容拼接到字符串变量里，每个文档前面标明序号和换行，方便
            # LLM
            # 在提示里区分不同文档片段
            retrieved_documents_content += f"文档片段 {i + 1}:\n{doc_content}\n\n"

            # 构建给前端的数据

            # 将文档内容和对应的元数据分别追加到两个列表中，通常用于接口返回给前端
            retrieved_docs_for_frontend.append(doc_content)
            retrieved_metadatas_for_frontend.append(metadata)
    else:
        retrieved_documents_content = "没有找到相关的文档信息。\n"

    # 1. 构建对话历史字符串
    history_string = "" # 初始化一个空的字符串，用来存储最终格式化好的聊天历史
    # 如果有聊天历史，遍历每条记录，格式化成用户和AI助手的对话形式
    if payload.chat_history:
        history_string += "以下是之前的对话历史：\n"
        # 遍历聊天历史列表，格式化每条记录
        # 每条记录是一个字典，包含角色（user 或 AI）和内容
        for entry in payload.chat_history:
            role = "用户" if entry["role"] == "user" else "AI助手"
            history_string += f"{role}: {entry['content']}\n"
        history_string += "\n"  

    # 2. 构建 DeepSeek-Chat 的提示
    prompt = f"""{history_string}以下是相关的文档内容（如果存在，请优先参考）：
                    {retrieved_documents_content}
                    
                    用户问题：{payload.user_query}
                    
                    请根据上述文档内容回答用户的问题并再回答最后返回相关文章链接。如果文档中没有直接相关的信息，请尝试利用您的通用知识进行回答，但务必明确说明信息来源是文档还是通用知识。"""

    # 调用LLM
    # 模型（如DeepSeek、GPT
    # 等）生成对用户问题的回答。
    # payload.llm_model
    # 是前端传来的模型名，支持灵活切换模型。
    # await 表示该函数是异步函数，等待模型调用完成
    llm_answer = await call_llm(payload.llm_model, prompt)

    return {
        "status": "success",
        # "user_query": payload.user_query,
        "answer": llm_answer,
        # "retrieved_documents": retrieved_docs_for_frontend,
        # "retrieved_metadatas": retrieved_metadatas_for_frontend
    }
