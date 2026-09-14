import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert Java teacher."
    ),
    (
        "human",
        "Explain {topic} in simple terms."
    ),
])

chain = prompt | llm

response = chain.invoke({
    "topic": "Polymorphism"
})

print(response)