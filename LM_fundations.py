from langchain.agents.middleware import OutputAgentState
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_agent
import os
from typing import Optional, Literal, List, Any
from langchain_tavily import TavilySearch
from langgraph.graph.state import CompiledStateGraph

from many_video import messages

load_dotenv(dotenv_path= ".env")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")



class Init_model:
    def __init__(
        self,
        provider: Literal["qwen", "deepseek"] = "deepseek",
        model: str = "deepseek-v4-pro"
    ):
        api_key_map = {
            "qwen": QWEN_API_KEY,
            "deepseek": DEEPSEEK_API_KEY
        }
        base_url = {
            "qwen": "https://api.qwen-plus.cn/v1",
            "deepseek": "https://api.deepseek.com"
        }
        api_key = api_key_map[provider]
        self.messages = []
        self.model = init_chat_model(api_key=api_key, model=model, base_url = base_url[provider])

    def Init_Tavily(self, max_results: int = 2):
        self.web_search = TavilySearch(max_results=max_results, api_key=TAVILY_API_KEY)
        return self.web_search

    def Init_agnet(self, if_web_search: bool = False, middlewares: list | None = None) -> Any:
        if middlewares is None:
            middlewares = []
        self.agent = create_agent(
            model = self.model,
            tools = [self.web_search] if if_web_search else [],
            middleware = middlewares,
        ) 
        return self.agent

    def manage_messages(self, message: Optional[str, List[HumanMessage]], system_message: Optional[str, None] = None, if_clear: bool = False):
        if system_message is not None:
            self.messages.append(SystemMessage(system_message))
        if isinstance(message, list):
            self.messages.extend(message)
        else:
            self.messages.append(HumanMessage(message))
        if if_clear:
            self.messages.clear()


    def start_invoke(self, message: HumanMessage):
        res = self.agent.invoke(message)
        return res