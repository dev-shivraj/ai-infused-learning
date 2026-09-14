from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert Java teacher. "
        "Explain concepts clearly for someone preparing for interviews."
    ),
    (
        "human",
        "Explain {topic} with a simple example."
    ),
])

messages = prompt.invoke({
    "topic": "Dependency Injection"
})

print(messages)