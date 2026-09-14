import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = llm.invoke(
    "Explain the difference between an interface and an abstract class in Java."
)

print("Response:")
print(response)

print("\nType:")
print(type(response))

print("\nContent:")
print(response.content)