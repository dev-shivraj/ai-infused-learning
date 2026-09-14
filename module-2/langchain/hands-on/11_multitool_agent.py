import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent

load_dotenv()


@tool
def get_java_version() -> str:
    """Return the Java version configured for the project."""
    return "Java 25 is currently configured for this project."


@tool
def get_project_info(project: str) -> str:
    """Return information about a learning project."""

    projects = {
        "spring-boot": "Spring Boot learning project",
        "llm": "LLM and LangChain learning project",
        "dsa": "Java DSA preparation",
    }

    return projects.get(
        project.lower(),
        "Project information not available."
    )


@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

agent = create_agent(
    model=llm,
    tools=[
        get_java_version,
        get_project_info,
        calculate_area,
    ],
)


# result = agent.invoke({
#     "messages": [
#         {
#             "role": "user",
#             "content": "What Java version is configured?"
#         }
#     ]
# })


# result = agent.invoke({
#     "messages": [
#         {
#             "role": "user",
#             "content": "What project am I working on if I am learning LangChain?"
#         }
#     ]
# })


result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": (
                "What Java version is configured, "
                "and what is the area of a rectangle "
                "with length 15 and width 8?"
            ),
        }
    ]
})

# print(result["messages"][-1].content)


# for message in result["messages"]:
#     print("\n==============================")
#     print("TYPE:", type(message))
#     print("CONTENT:", message.content)

#     if hasattr(message, "tool_calls") and message.tool_calls:
#         print("TOOL CALLS:", message.tool_calls)


for message in result["messages"]:
    print("\n==============================")
    print("TYPE:", type(message))
    print("CONTENT:", message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("TOOL CALLS:", message.tool_calls)