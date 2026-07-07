# # from dashscope import api_key
# from langchain.chat_models import init_chat_model
# from dotenv import load_dotenv
# import os
# from langchain.agents import create_agent
# import json
# from langchain_deepseek import ChatDeepSeek
# from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
# from langchain_tavily import TavilySearch
#
#
#
#
# def main():
#     load_dotenv()
#     api_key = os.getenv("QWEN_API_KEY")
#     web_key = os.getenv("TAVILY_API_KEY")
#     # web_search = TavilySearch(max_results = 2, api_key = web_key)
#     # model = ChatDeepSeek(api_key = api_key, model = "deepseek-v4-pro")
#     # agent = create_agent(model = model, tools = [web_search])
#     model = init_chat_model(model= "qwen-plus", api_key = api_key, model_provider="qwen")
#     messages = [
#         SystemMessage(content = "你是一个专业的新闻搜索助手，你可以根据用户的问题，搜索相关的新闻。你可以使用Tavily搜索相关的新闻。"),
#         HumanMessage(content= "我是Enfield， 请记住我的名字"),
#         AIMessage(content = "你好，Enfield，我已经记住了你的名字"),
#     ]
#     while True:
#         user_input = input("请提问：")
#         if user_input == "exit":
#             break
#         messages.append(HumanMessage(content = user_input))
#         res = model.invoke(messages)
#
#         messages.append(res)
#         print("回答：", res.content)


# from dashscope import api_key
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
import json
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_tavily import TavilySearch



def main():
    load_dotenv()
    api_key = os.getenv("QWEN_API_KEY")
    web_key = os.getenv("TAVILY_API_KEY")
    # web_search = TavilySearch(max_results = 2, api_key = web_key)
    # model = ChatDeepSeek(api_key = api_key, model = "deepseek-v4-pro")
    # agent = create_agent(model = model, tools = [web_search])
    model = ChatOpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        model="qwen-plus"
    )
    messages = [
        SystemMessage(content = "你是一个专业的新闻搜索助手，你可以根据用户的问题，搜索相关的新闻。你可以使用Tavily搜索相关的新闻。"),
        HumanMessage(content= "我是Enfield， 请记住我的名字"),
        AIMessage(content = "你好，Enfield，我已经记住了你的名字"),
    ]
    while True:
        user_input = input("请提问：")
        if user_input == "exit":
            break
        messages.append(HumanMessage(content = user_input))
        res = model.invoke(messages)

        messages.append(res)
        print("回答：", res.content)




if __name__ == "__main__":
    main()

