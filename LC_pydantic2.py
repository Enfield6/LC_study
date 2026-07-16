from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_tavily import TavilySearch
from langchain_core.runnables import RunnableLambda
import os
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from rich import print as rprint


class Movie(BaseModel):
    title: str = Field(description="电影名称")
    director: str = Field(description="导演", max_length=20, min_length=1)
    actors: dict[str, str] = Field(description="演员表[角色姓名：演员姓名]", max_length=100, min_length=1)
    genre: str = Field(description="类型", default=None)
    release_date: datetime = Field(description="上映日期")
    duration: timedelta | None = Field(description="时长", default=None)
    description: str = Field(description="情节描述", min_length=100)
    imdb_rating: float | None = Field(description="IMDb评分", default=None)
    meta_score: float | None = Field(description="meta评分", default=None)


def main():
    load_dotenv(dotenv_path='.env')

    # 1. 初始化组件
    web_search = TavilySearch(max_results=4, api_key=os.getenv("TAVILY_API_KEY"))
    model = init_chat_model(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        model="deepseek-v4-pro",
        model_provider="deepseek",
        temperature=0,
    )
    parser = PydanticOutputParser(pydantic_object=Movie)

    # 2. 定义搜索函数（使用 invoke 方法）
    def search_movie(query):
        """搜索电影信息（正确调用方式）"""
        # 使用 invoke() 方法，传入字典参数
        return web_search.invoke({"query": query})

    # 3. 定义消息构建函数
    def build_messages(data):
        return [
            SystemMessage(content="你是一个电影专家，擅长整理电影信息。"),
            HumanMessage(content=f"""
                                    请根据以下搜索结果，提取电影 "{data["query"]}" 的详细信息：
                                    
                                    搜索结果：
                                    {data["search_results"]}
                                    
                                    请按照以下 JSON 格式输出：
                                    {parser.get_format_instructions()}
                                    """)
        ]

    # 4. 创建管道
    chain = (
            RunnableLambda(lambda query: {"query": query, "search_results": search_movie(query)})
            | RunnableLambda(build_messages)
            | model
            | parser
    )

    # 5. 执行
    res = chain.invoke("飞驰人生3")
    # print(f"电影名称: {res.title}")
    # print(f"导演: {res.director}")
    # print(f"演员: {res.actors}")
    # print(f"上映日期: {res.release_date}")
    # print(f"时长: {res.duration}")
    # print(f"简介: {res.description}")
    print(res)
    print("===" * 100,'\n', type(res))
    json_res = res.model_dump_json()
    rprint("===" * 100,'\n', json_res)
    print("--------" * 100, '\n',type(json_res))
if __name__ == "__main__":
    main()