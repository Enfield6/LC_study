from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mysql.pymysql import PyMySQLSaver
# from langgraph.checkpoint.mysql import BaseMySQLSaver
import os
from dotenv import load_dotenv

from frist import response

load_dotenv(dotenv_path=".env")
DB_URL = "mysql+pymysql://root:root@localhost:3306/langGraph"

# 创建 saver 实例
# 方式1：使用 with 语句（推荐）
with PyMySQLSaver.from_conn_string(DB_URL) as saver:
    # 在 with 块内部调用 setup()
    saver.setup()
    model = init_chat_model(
        model="qwen3.5-omni-plus",
        model_provider="openai",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key=os.getenv("QWEN_API_KEY")

    )
    agent = create_agent(
        model = model,
        tools=[],
        checkpointer= saver,
    )
    config = {
        "configurable": {
            "thread_id": "1"
        }
    }

    response1 = agent.invoke({
        "messages": [HumanMessage("你好，我是康师傅")]},
        config= config,
    )

    for msg in  response1["messages"]:
        msg.pretty_print()

    response2 = agent.invoke({"messages": [HumanMessage("你知道我是谁吗？")]},
                             config= config,
    )

    for msg in response2["messages"]:
        msg.pretty_print()


