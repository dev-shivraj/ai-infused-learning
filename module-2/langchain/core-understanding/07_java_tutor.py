import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a Java interview mentor.

        Explain concepts in:
        1. Simple language
        2. Interview-oriented language
        3. With a Java example
        4. With one common interview question
        """
    ),
    (
        "human",
        "Teach me about {topic}."
    ),
])

chain = prompt | llm | StrOutputParser()

while True:

    topic = input("\nEnter a Java topic (or 'exit'): ")

    if topic.lower() == "exit":
        break

    result = chain.invoke({
        "topic": topic
    })

    print("\n" + result)