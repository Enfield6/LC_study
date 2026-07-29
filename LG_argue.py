from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os

load_dotenv()
llm1 = init_chat_model(
    model="deepseek-v4-pro",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.9,  # 辩论需要一点创造性，温度稍高
)

llm2 = init_chat_model(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=1.5,  # 辩论需要一点创造性，温度稍高
)

class DebateState(BaseModel):
    topic : str = Field(description="辩论的主题")
    messages: List[BaseMessage] = Field(description="辩论的对话记录", default=[])
    current_speaker : Literal["affirmative", "negative"] = Field(description="下一位发言者", default="affirmative")
    turn_count : int = Field(description="当前发言次数", default=0)
    max_turns : int = Field(description="最大发言次数", default=3)


def affirmative_speak(state: DebateState):
    system_prompt = f"""你是本次辩论赛的正方选手，你坚定支持观点：「{state.topic}」。
    规则：
    1. 针对反方上一轮的观点进行针对性反驳，同时深化己方论点
    2. 逻辑清晰，有理有据，语言精炼，每次发言控制在150字以内
    3. 只输出发言内容，不要加“我方认为”之外的多余格式
    4.在逻辑通畅的前提下，适当展示文采
    5.满足以上要求的基础上，多一些幽默感，增加观赏性
    """

    full_messages = [SystemMessage(content=system_prompt)] + state.messages
    response = llm1.invoke(full_messages)
    response.content = f"正方：{response.content}"

    return {
        "messages": state.messages + [response],
        "turn_count": state.turn_count + 1,
        "current_speaker": "negative"
    }


def negative_speak(state: DebateState):
    system_prompt = f"""你是本次辩论赛的反方选手，你坚定反对观点：「{state.topic}」。
    规则：
    1. 针对正方上一轮的观点进行针对性反驳，同时深化己方论点
    2. 逻辑清晰，有理有据，语言精炼，每次发言控制在200字以内
    3. 只输出发言内容，不要加“我方认为”之外的多余格式
    """

    full_messages = [SystemMessage(content=system_prompt)] + state.messages
    response = llm2.invoke(full_messages)
    response.content = f"反方：{response.content}"

    return {
        "messages": state.messages + [response],
        "turn_count": state.turn_count + 1,
        "current_speaker": "affirmative"
    }


def route_next_step(state: DebateState):
    # 如果达到最大发言次数，辩论结束
    if state.turn_count >= state.max_turns:
        return END

    # 否则，按照 current_speaker 的标记，轮到下一位发言
    return state.current_speaker


# 1. 初始化图构建器，绑定我们定义的状态结构
builder = StateGraph(DebateState)

# 2. 向图中添加两个节点：节点名 + 对应的处理函数
builder.add_node("affirmative", affirmative_speak)
builder.add_node("negative", negative_speak)

# 3. 设置入口点：辩论从正方先发言开始
builder.set_entry_point("affirmative")

# 4. 添加条件边：从正方节点出来，走路由判断
builder.add_conditional_edges(
    source="affirmative",    # 起点：正方节点
    path=route_next_step,    # 路由判断函数
    path_map={               # 路由返回值 对应 目标节点
        "negative": "negative",
        END: END
    }
)

# 5. 添加条件边：从反方节点出来，也走路由判断
builder.add_conditional_edges(
    source="negative",
    path=route_next_step,
    path_map={
        "affirmative": "affirmative",
        END: END
    }
)

# 6. 编译图，变成可执行的工作流
graph = builder.compile()


# 初始化辩论状态
initial_state = DebateState(
    topic="人工智能的发展对人类社会利大于弊",
    messages=[],
    current_speaker="affirmative",
    turn_count=0,
    max_turns=6  # 总共6次发言，正反各3轮
)

# 流式运行，逐次输出每一轮的发言
print(f"辩题：{initial_state.topic}\n")
print("="*50 + " 辩论开始 " + "="*50 + "\n")

for output in graph.stream(initial_state):
    # output 是一个字典，key 是当前执行完的节点名
    for node_name, state_update in output.items():
        # 取出最新的那条发言并打印
        latest_message = state_update["messages"][-1]
        print(latest_message.content)
        print("-"*80)

print("\n辩论结束！")