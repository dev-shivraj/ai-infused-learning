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
def subtract_numbers(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b


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
        subtract_numbers,
        multiply_numbers,
    ],
)

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "Start with 100, subtract 20, "
                "multiply the result by 3, "
                "and then add 10."
            ),
        }
    ]
})

print(result["messages"][-1].content)