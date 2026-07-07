from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.utils.function_calling import tool_example_to_messages
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import os
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from dotenv import load_dotenv


# class Movie(BaseModel):
#     title: str = Field(description="电影名称")
#     director: str = Field(description="导演", max_length= 20, min_length=1)
#     actors: dict[str, str] = Field(description="演员表", max_length= 100, min_length=1)
#     genre: str = Field(description="类型", default= None)
#     release_date: datetime = Field(description="上映日期")
#     duration: timedelta = Field(description="时长")
#     description: str = Field(description="情节描述", min_length= 100)
#     # poster: str = Field(description="海报")
#     # trailer: str = Field(description="预告片")
#     imdb_rating: str = Field(description="IMDb评分")
#     meta_score: str = Field(description="meta评分")
#
# def main():
#     load_dotenv(dotenv_path='.env')
#     web_search = TavilySearch(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))
#     model = init_chat_model(
#         api_key=os.getenv("DEEPSEEK_API_KEY"),
#         model="deepseek-v4-pro",
#         model_provider="deepseek",
#         temperature=0,
#     )
#     parser = PydanticOutputParser(pydantic_object=Movie)
#
#     message = [HumanMessage(content="当幸福来敲门")]
#     chain = (
#         {"search": web_search}
#         | model
#         | parser
#     )
#     res = chain.invoke(message)
#     print(res)
#
#
def main():
    load_dotenv(dotenv_path= ".env")
    


if __name__ == "__main__":
    main()



