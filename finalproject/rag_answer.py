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
    if vectordb_services.vectorstore is None:
        raise HTTPException(status_code=500,
                            detail="ChromaDB vectorstore not initialized. Please check server logs for initialization errors.")
    if vectordb_services.lc_embedding_model is None:
        raise HTTPException(status_code=500,
                            detail="Embedding model not loaded. Please check server logs for initialization errors.")

    docs = vectordb_services.vectorstore.similarity_search(query=payload.user_query, k=payload.n_results)

    retrieved_documents_content = ""
    retrieved_docs_for_frontend = []
    retrieved_metadatas_for_frontend = []

    if docs:
        for i, doc in enumerate(docs):
            # LangChain 的 Document 对象有 page_content 和 metadata 属性
            doc_content = doc.page_content
            metadata = doc.metadata

            print(f"DEBUG: Retrieved Doc {i + 1}: '{doc_content[:100]}...' | Metadata: {metadata}")

            # 构建给 LLM 的上下文
            retrieved_documents_content += f"文档片段 {i + 1}:\n{doc_content}\n\n"

            # 构建给前端的数据
            retrieved_docs_for_frontend.append(doc_content)
            retrieved_metadatas_for_frontend.append(metadata)
    else:
        retrieved_documents_content = "没有找到相关的文档信息。\n"

    # 2. 构建 DeepSeek-Chat 的提示
    prompt = f"""以下是相关的文档内容（如果存在，请优先参考）：
{retrieved_documents_content}

用户问题：{payload.user_query}

请根据上述文档内容回答用户的问题并再回答最后返回相关文章链接。如果文档中没有直接相关的信息，请尝试利用您的通用知识进行回答，但务必明确说明信息来源是文档还是通用知识。"""

    llm_answer = await call_llm(payload.llm_model, prompt)

    return {
        "status": "success",
        "user_query": payload.user_query,
        "answer": llm_answer,
        "retrieved_documents": retrieved_docs_for_frontend,
        "retrieved_metadatas": retrieved_metadatas_for_frontend
    }
