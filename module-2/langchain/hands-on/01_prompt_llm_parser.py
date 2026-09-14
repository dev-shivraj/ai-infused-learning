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
        "You are an expert programming teacher."
    ),
    (
        "human",
        "Explain {topic} in {language} with a simple example."
    ),
])

parser = StrOutputParser()

chain = prompt | llm | parser

result = chain.invoke({
    "language": "Java",
    "topic": "Polymorphism",
})

print(result)