import os
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
import json
import time
from langchain.agents import create_agent
import base64


def audio_to_base64(audio_path: str) -> str:
    """将本地音频文件转换为 Base64 编码"""
    # 获取音频格式（用于设置 MIME 类型）
    ext = os.path.splitext(audio_path)[1].lower()
    mime_type = {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac"
    }.get(ext, "audio/mpeg")

    with open(audio_path, "rb") as f:
        base64_str = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime_type};base64,{base64_str}"


def main():
    load_dotenv()
    api_key = os.getenv("QWEN_API_KEY")
    model = init_chat_model(api_key= api_key,
                            model= "qwen3-asr-flash",
                            model_provider="openai",
                            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    audio_path = '/Users/zsh/Music/Music/Media.localized/Music/Unknown Artist/Unknown Album/莫文蔚 - 盛夏的果实.mp3'

    message= [
        HumanMessage(content_blocks= [
            {
                "type": "audio",
                "audio": audio_to_base64(audio_path)
            }])
    ]
    full_text= ""
    res = model.stream(message)
    for chunk in res:
        print(chunk.content, end= '', flush= True)
        full_text += chunk.content

    print("\n \n ✅✅✅ 完整的内容：\n", full_text, end= "\n")





if __name__ == "__main__":
    main()
