from langchain_core.messages import MessagesPlaceholder, HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent
import json
import os
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from langchain.tools import tool

def main():
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    web_key = os.getenv("TAVILY_API_KEY")
    web_search = TavilySearch(max_results = 2, api_key = web_key)
    model = init_chat_model(api_key = api_key, model = "deepseek-v4-pro", model_provider= "deepseek")
    engine = create_agent(model = model, tools = [web_search],)

 


if __name__ == "__main__":
    main()
