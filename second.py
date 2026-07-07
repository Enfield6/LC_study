from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    model = init_chat_model(api_key = os.getenv("DEEPSEEK_API_KEY"),
                            base_url = "https://api.deepseek.com",
                            model = "deepseek-v4-pro"

                            )

    """统一返回"""
    # res = model.invoke("你是谁，你能干什么？")
    # print(res.content)


    # """流式返回"""
    # res = model.stream("你是谁，你能干什么？")
    # for msg in res:
    #     print(msg.content, end= '', flush= True)

    """一次多问"""
    res = model.batch(["你是谁，你能干什么？", "你有哪些功能，能帮助我什么？", "你和langchain结合，能开发出怎么样的程序？"])
    for item in res:
        print(item.content, end= "\n")

    """ """




if __name__ == "__main__":
    main()