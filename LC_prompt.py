from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model


def main():
    load_dotenv(dotenv_path= ".env")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    model = init_chat_model(api_key=api_key,
                            model_provider="deepseek",
                            language="zh-CN",
                            temperature=0,)
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你是{device_type}设备的客服助手，回答要简洁、准确。"
        ),
        (
            "human",
            "{question}"
        )
    ])

    chain = prompt | model
    res = chain.stream({"device_type": "Windows 11 PC", "question": "你好,我点开机键电脑没反应，为什么？ 如何解决"})
