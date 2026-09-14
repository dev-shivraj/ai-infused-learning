import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = llm.invoke("Explain polymorphism in Java.")

print("Type:")
print(type(response))

print("\nFull response:")
print(response)

print("\nContent:")
print(response.content)

print("\nResponse metadata:")
print(response.response_metadata)