from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms with one example."
)

messages = prompt.invoke({
    "topic": "Dependency Injection"
})

print(messages)