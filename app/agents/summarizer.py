from app.models import Article
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from app.llm import llm

class Summarizer:
    def __init__(self):
        self.system_prompt = """
        You are an AI expert who makes complex topics accessible 
        to general audiences. Summarize this article in 2-3 sentences, focusing on the key points 
        and explaining any technical terms simply.
        """
    
    def summarize(self, article: Article) -> str:
        response = llm.invoke([
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"Title: {article.title}\n\nContent: {article.content}")
        ])
        return response.content