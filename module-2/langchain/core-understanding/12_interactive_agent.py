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


@tool
def divide_numbers(a: float, b: float) -> float:
    """Divide a by b."""
    if b == 0:
        return 0

    return a / b


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
        divide_numbers,
    ],
)


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ]
    })

    print("\nAgent:", result["messages"][-1].content)