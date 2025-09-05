from typing import List, Dict
from langchain.schema import HumanMessage, SystemMessage
from app.llm import llm
from datetime import datetime
from app.prompts import broad_prompt

class Publisher:
    def create_report(self, summaries: List[Dict]) -> str:      
        prompt = broad_prompt
        
        # Format summaries for the LLM
        summaries_text = "\n\n".join([
            f"Title: {item['title']}\nSummary: {item['summary']}\nSource: {item['url']}"
            for item in summaries
        ])
        
        # Generate report
        response = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=summaries_text)
        ])
        
        # Add metadata and save
        current_date = datetime.now().strftime("%Y-%m-%d")
        markdown_content = f"""
        Generated on: {current_date}

        {response.content}
        """
        
        filename = f"ai_news_report_{current_date}.md"
        with open(filename, 'w') as f:
            f.write(markdown_content)
        
        return response.content