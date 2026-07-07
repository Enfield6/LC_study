import os
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv(dotenv_path=".env")

api_key = os.getenv("QWEN_API_KEY")

model = init_chat_model(api_key= api_key, model= "qwen3.5-omni-plus", model_provider="openai", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

message= [
    SystemMessage(content="你是我的图片识别助手，我传给你的图片，你要用文字形象的描述图片的内容，充分展示你的文采，词藻华丽"),
    HumanMessage(content_blocks=[
        {
            "type": "image",
            "url": "https://img2.baidu.com/it/u=452219227,549715250&fm=253&fmt=auto&app=138&f=JPEG?w=773&h=500"
        },
        {
            "type": "text",
            "text": "你知道你应该干什么的"
        }
    ])
]

res = model.stream(message)
full_text= ""
for chunk in res:
    print(chunk.content, end= '', flush= True)
    full_text += chunk.content

print("\n \n ✅✅✅ 完整的内容：\n", full_text, end= "\n")




