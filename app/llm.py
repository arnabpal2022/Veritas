import os
import getpass
from tavily import TavilyClient
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm =  ChatGroq(
    model_name="openai/gpt-oss-120b",
    temperature=0.7
)