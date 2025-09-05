from app.models import Article
from typing import List
from app.llm import tavily

class NewsSearcher:
    def search(self) -> List[Article]:
        response = tavily.search(
            query="artificial intelligence and machine learning news", 
            topic="news",
            time_range="day",
            search_depth="basic",
            max_results=5
        )
        
        print("Search response:", response['results'])  # Debugging line
        
        articles = []
        for result in response['results']:
            articles.append(Article(
                title=result['title'],
                url=result['url'],
                content=result['content']
            ))
        
        return articles