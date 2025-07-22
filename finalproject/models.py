from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class RAGQueryPayload(BaseModel):
    user_query: str
    n_results: int = 5
    llm_model: Optional[str] = "deepseek-chat"
    chat_history: Optional[List[Dict[str, str]]] = None

