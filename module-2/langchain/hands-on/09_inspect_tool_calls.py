import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()


@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

agent = create_agent(
    model=llm,
    tools=[
        add_numbers,
        multiply_numbers,
    ],
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is 20 plus 30, and then multiply the result by 5?"
        }
    ]
})


for message in result["messages"]:
    print("\n--------------------")
    print("Type:", type(message))

    if hasattr(message, "tool_calls"):
        print("Tool calls:")
        print(message.tool_calls)