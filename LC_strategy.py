from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.structured_output import AutoStrategy
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field, model_validator
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_tavily import TavilySearch
import os
import datetime as dt
import json

class Personage_info(BaseModel):
    name: str = Field(description="人物名称", min_length=1)
    birth_date: dt.datetime = Field(description="人物出生日期")
    sex: Literal["男", "女"] = Field(description="人物性别", )
    description: str = Field(description="人物生平", min_length=1, max_length= 500)
    exist: Literal["在世", "已故"] = Field(description="人物是否在在世", default="在世")
    death_date: dt.datetime = Field(description="人物死亡日期", default=None)

    @model_validator(mode='after')
    def check_death_date(self):
        if self.exist == "已故" and self.death_date is None:
            raise ValueError("已故人物必须填写死亡日期")
        if self.exist == "在世" and self.death_date is not None:
            raise ValueError("在世人物不应有死亡日期")
        return self

def main():
    load_dotenv(dotenv_path= ".env")
    web_search = TavilySearch(max_results=1, api_key=os.getenv("TAVILY_API_KEY"))
    # LLM_model = init_chat_model(
    #     api_key=os.getenv("DEEPSEEK_API_KEY"),
    #     model="deepseek-v4-flash",
    #     model_provider="deepseek",
    #     base_url = "https://api.deepseek.com",
    # )
    api_key = os.getenv("QWEN_API_KEY")

    LLM_model = init_chat_model(api_key=api_key, model="qwen3.5-omni-plus", model_provider="openai",
                            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

    agent = create_agent(
        model = LLM_model,
        tools = [web_search],
        response_format = AutoStrategy(schema= Personage_info)

    )

    res = agent.invoke({"messages": ["丁谓"]})
    print(res["messages"])
    print("===" * 20)
    # text = (res["messages"][-1][1][])
    # print(res.model_jump_json())
    # for msg in res["messages"]:
    #     print(msg.model_dump_json())
    result = res["messages"][-2]["args"]
    print(result.model_dump_json())
    # res = agent.invoke({"messages": ["丁谓"]})

    # 提取结构化数据
    # last_msg = res["messages"][-1]

    # if hasattr(res, 'structured_response'):
    #     json_str = res.structured_response.model_dump_json(indent=2)
    #     print(json_str)

if __name__ == "__main__":
    main()