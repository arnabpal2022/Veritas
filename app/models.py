from typing import Dict, List, Any, TypedDict, Optional
from pydantic import BaseModel

class Article(BaseModel):
    title: str
    url: str
    content: str

class Summary(TypedDict):
    title: str
    summary: str
    url: str

class GraphState(TypedDict):
    articles: Optional[List[Article]] 
    summaries: Optional[List[Summary]] 
    report: Optional[str] 