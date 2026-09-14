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
        "You are a programming teacher."
    ),
    (
        "human",
        "Explain {topic} for a {difficulty} level learner."
    ),
])

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "topic": "Dependency Injection",
    "difficulty": "beginner",
})

print(result)