from dashscope import api_key
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
import json
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_tavily import TavilySearch


load_dotenv()
web_search = TavilySearch(max_results = 2, api_key = os.getenv("TAVILY_API_KEY"))
model = ChatDeepSeek(api_key = os.getenv("DEEPSEEK_API_KEY"), model = "deepseek-v4-pro")
agent = create_agent(model = model, tools = [web_search],
                     system_prompt = "你是一个多才多艺的助手，你可以根据用户的问题，搜索相关的新闻。")

message = [
    SystemMessage(content = "你是是一个专业的新闻搜索助手"),
    HumanMessage(content = "你是谁？你能做什么？"),
    AIMessage(content = "我是你创建的助手，你可以根据用户的问题，搜索相关的新闻。"),
    HumanMessage(content = "请查询关于spaceX的新闻，要最近七天的，找出影响力大的新闻。")
]
res = agent.invoke({"messages": message})
for msg in res["messages"]:
    msg.pretty_print()





