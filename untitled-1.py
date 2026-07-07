# from dashscope import api_key
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
import json
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_tavily import TavilySearch


def main():
    load_dotenv()
    api_key = os.getenv("DEEPSEEK_API_KEY")
    web_key = os.getenv("TAVILY_API_KEY")
    # web_search = TavilySearch(max_results = 2, api_key = web_key)
    # model = ChatDeepSeek(api_key = api_key, model = "deepseek-v4-pro")
    # agent = create_agent(model = model, tools = [web_search])
    model = init_chat_model(model= "deepseek-v4-pro", api_key = api_key, model_provider="deepseek")
    messages = [
        SystemMessage(content = "你是一个专业的新闻搜索助手，你可以根据用户的问题，搜索相关的新闻。你可以使用Tavily搜索相关的新闻。"),
        HumanMessage(content= "我是Enfield， 请记住我的名字"),
        AIMessage(content = "你好，Enfield，我已经记住了你的名字"),
    ]
    while True :
        user_input = input ("请提问：")
        if user_input == "exit":
            break
        messages.append(HumanMessage(content = user_input))
        res = model.stream(messages)
        # print("回答：", res.content)
        for msg in res:
            print(msg.content, end= '', flush= True)
        messages.append(res)



if __name__ == "__main__":
    main()
