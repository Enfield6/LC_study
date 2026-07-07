import dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import dotenv as dt
from langchain.chat_models import init_chat_model
import os

dt.load_dotenv(dt.find_dotenv())
api_key = os.getenv("QWEN_API_KEY")
model = init_chat_model(
    model="qwen3.5-omni-plus",
    model_provider="openai",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=api_key
)

messages = [
    HumanMessage(content= [
        {
            "type": "video_url",
            "video_url": {
                "url": "https://aweme.snssdk.com/aweme/v1/play/?video_id=v0200fg10000cuhogevog65hkurqon00&ratio=720p&line=0"
            },
        },
        {
            "type": "text",
            "text": "请只提取这段视频中的语音内容，转写成文字。如果有多个人呢说话，请你写成剧本的形式, 要符合人类的习惯。"
        }
    ])
]

res = model.stream(messages)
full_text = ""
for chunk in res:
    print(chunk.content, end= "", flush= True)
    full_text += chunk.content

print("\n \n ✅✅✅ 完整的内容：\n", full_text, end= "\n")
