import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)


history = []


prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a helpful programming tutor. "
        "Remember the conversation and answer based on previous messages."
    ),

    MessagesPlaceholder(
        variable_name="history"
    ),

    (
        "human",
        "{question}"
    ),
])


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break


    messages = prompt.invoke({
        "history": history,
        "question": question,
    })

    # print("\n----- MESSAGES SENT TO LLM -----")

    # for message in messages.messages:
    #     print(
    #         f"{type(message).__name__}: {message.content}"
    #     )


    response = llm.invoke(messages)


    print("\nAI:", response.content)


    # Save conversation AFTER getting the response
    history.append(
        HumanMessage(content=question)
    )

    history.append(
        AIMessage(content=response.content)
    )


print("\n\n========== HISTORY ==========")

for message in history:

    print(
        f"{type(message).__name__}: {message.content}"
    )