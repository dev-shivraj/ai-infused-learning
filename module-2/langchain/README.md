# LangChain — Messages, Tools, Agents & Conversation History

A hands-on reference covering how LangChain applications are built up from prompts and messages into full tool-using agents with memory.

All examples use **Groq's** OpenAI-compatible API:
- Model: `openai/gpt-oss-20b`
- API key: `GROQ_API_KEY`
- Base URL: `https://api.groq.com/openai/v1`

---

## Table of Contents

1. [What Is LangChain?](#1-what-is-langchain)
2. [Connecting to a Model](#2-connecting-to-a-model)
3. [Messages: The Basic Unit of Conversation](#3-messages-the-basic-unit-of-conversation)
4. [Prompts](#4-prompts)
5. [Chains and Output Parsing](#5-chains-and-output-parsing)
6. [Tools](#6-tools)
7. [Agents](#7-agents)
8. [Conversation History](#8-conversation-history)
9. [Putting It All Together](#9-putting-it-all-together)
10. [Common Mistakes](#10-common-mistakes)
11. [Cheat Sheet](#11-cheat-sheet)
12. [Mental Models](#12-mental-models)

---

## 1. What Is LangChain?

LangChain is a framework for building applications on top of large language models. Rather than calling a provider's API directly:

```python
response = openai_client.chat(...)
```

LangChain gives you reusable building blocks for models, prompts, messages, output parsers, tools, agents, memory, and retrieval — so these pieces can be composed instead of hand-rolled each time.

**Without tools**, the flow is linear:

```
User → Prompt → LLM → Response → Application
```

**With tools and agents**, the flow branches:

```
User → Agent → LLM → needs a tool?
                        ├── Yes → run Tool → back to LLM
                        └── No  → Final Answer
```

---

## 2. Connecting to a Model

### `ChatOpenAI`

`ChatOpenAI` is LangChain's chat-model interface. Despite the name, it works with any OpenAI-compatible endpoint — including Groq.

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
```

| Parameter | Purpose |
|---|---|
| `model` | Which model to call |
| `api_key` | Pulled from an environment variable |
| `base_url` | The OpenAI-compatible endpoint to hit |

Conceptually, the setup routes through an extra layer:

```
Groq → OpenAI-compatible API → ChatOpenAI → LangChain → Your app
```

---

## 3. Messages: The Basic Unit of Conversation

LangChain represents a conversation as a sequence of typed message objects rather than plain strings.

### `HumanMessage`

Represents something the user said.

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(content="What is polymorphism in Java?")
print(message.content)
```

### `AIMessage`

Represents something the model said — either the final response from `llm.invoke()`, or a manually constructed message you're adding to history.

```python
from langchain_core.messages import AIMessage

message = AIMessage(content="Polymorphism allows objects to take multiple forms.")
print(message.content)
```

Calling the model directly returns an `AIMessage` object, not a raw string:

```python
response = llm.invoke("Explain polymorphism in Java.")

print(type(response))     # AIMessage
print(response.content)   # the actual text
```

**Important:** an `AIMessage` isn't guaranteed to be a final answer — it may instead be a request to call a tool. More on this in [Agents](#7-agents).

### `ToolMessage`

Represents the result of executing a tool inside an agent loop. Covered in detail below.

---

## 4. Prompts

### `ChatPromptTemplate`

Lets you define a reusable, structured prompt with variable placeholders instead of hardcoding message text.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert programming teacher."),
    ("human", "Explain {topic} in {language}."),
])
```

`{topic}` and `{language}` are filled in at invocation time:

```python
messages = prompt.invoke({
    "topic": "Polymorphism",
    "language": "Java",
})
```

### Message Roles

A prompt is built from distinct roles:

- **`"system"`** — sets the model's behavior or persona (e.g. *"You are an expert Java teacher."*)
- **`"human"`** — represents the user's actual request (e.g. *"Explain {topic}."*)

These combine into a single template:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert Java teacher."),
    ("human", "Explain {topic}."),
])
```

### Sending a Prompt to the Model

```python
messages = prompt.invoke({"topic": "Polymorphism"})
response = llm.invoke(messages)
print(response.content)
```

Flow: `ChatPromptTemplate → Messages → ChatOpenAI → AIMessage`

---

## 5. Chains and Output Parsing

### `StrOutputParser`

Converts an `AIMessage` into a plain string, since `llm.invoke()` returns an object, not raw text.

```python
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
result = parser.invoke(response)

print(type(result))  # str
print(result)
```

### Composing a Chain with `|`

LangChain components can be piped together, so a full prompt → model → parser pipeline becomes one expression:

```python
chain = prompt | llm | parser
```

**Full example:**

```python
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
    ("system", "You are an expert programming teacher."),
    ("human", "Explain {topic} in {language} with a simple example."),
])

parser = StrOutputParser()
chain = prompt | llm | parser

result = chain.invoke({"language": "Java", "topic": "Polymorphism"})
print(result)
```

Flow: `Input → ChatPromptTemplate → ChatOpenAI → StrOutputParser → String`

---

## 6. Tools

A **tool** is a function an AI application can call to perform a concrete action — a calculation, a lookup, an API call.

A plain Python function isn't automatically usable by the model:

```python
def add_numbers(a, b):
    return a + b
```

The `@tool` decorator exposes it to LangChain, along with its name, parameter types, and description (taken from the docstring):

```python
from langchain_core.tools import tool

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
```

The docstring matters — it's what the model reads to decide when and how to use the tool.

```python
@tool
def calculate_square(number: float) -> float:
    """Calculate the square of a number."""
    return number * number
```

### Invoking a Tool Manually

You can call a tool directly without going through the model:

```python
result = add_numbers.invoke({"a": 10, "b": 20})
print(result)  # 30
```

This is distinct from the model *choosing* to call the tool on its own — that's the agent's job.

### Multiple Tools

```python
@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

@tool
def calculate_square(number: float) -> float:
    """Calculate the square of a number."""
    return number * number
```

### `bind_tools()`

Makes a set of tools *available* to the model, without managing execution:

```python
llm_with_tools = llm.bind_tools([add_numbers, multiply_numbers])
response = llm_with_tools.invoke("What is 25 multiplied by 4?")
```

The model can now decide it wants to call `multiply_numbers` — but `bind_tools()` stops there. It doesn't execute the tool, feed the result back, or manage a loop. That's what an **agent** adds.

```
LLM → tools available → LLM can request a tool
```

---

## 7. Agents

### Tools vs. Agents

| | Role |
|---|---|
| **Tool** | Performs one specific operation (e.g. `calculate_square(10) → 100`) |
| **Agent** | Decides *which* tool to use, runs it, and turns the result into an answer |

Example: given *"What is 25 multiplied by 4?"*, an agent reasons that `multiply_numbers` fits, calls `multiply_numbers(25, 4)`, gets `100`, and replies *"25 × 4 = 100."*

### Creating an Agent

```python
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=[add_numbers, multiply_numbers],
)

result = agent.invoke({
    "messages": [
        {"role": "user", "content": "What is 25 multiplied by 4?"}
    ]
})

print(result["messages"][-1].content)
```

An agent is built from three things: a model, a list of tools, and the incoming messages. The model itself decides whether any tool is needed.

### The Agent Loop

A plain LLM call is a single hop:

```
User → LLM → Answer
```

An agent call can loop through multiple tool calls before producing a final answer:

```
User → Agent → LLM → AIMessage
                        │
              contains tool_calls?
               ├── Yes → run Tool → ToolMessage → back to LLM → new AIMessage (loop)
               └── No  → Final answer
```

### `AIMessage` Can Contain Tool Calls

This is the key insight that makes agents work: an `AIMessage` is not automatically a final answer.

```python
AIMessage(
    content="",
    tool_calls=[
        {"name": "calculate_square", "args": {"number": 10}}
    ]
)
```

Here the model isn't answering — it's requesting that `calculate_square` be run with `10`.

### `ToolMessage`

Represents what a tool returned, once the agent executes the call the model requested.

```
HumanMessage "What is 10 squared?"
      ↓
AIMessage    "call calculate_square(10)"
      ↓
Tool         calculate_square(10)
      ↓
ToolMessage  "100"
      ↓
AIMessage    "10 squared is 100."
```

With several tool calls chained together:

```
HumanMessage → AIMessage(tool_calls) → ToolMessage
             → AIMessage(tool_calls) → ToolMessage
             → AIMessage(final)
```

### A Multi-Tool Agent

```python
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

agent = create_agent(model=llm, tools=[add_numbers, multiply_numbers])

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 25 multiplied by 4?"}]
})
```

The agent picks `multiply_numbers`, runs `multiply_numbers(25, 4)`, and returns `100`.

### An Interactive Command-Line Agent

```python
while True:
    question = input("\nYou: ")
    if question.lower() == "exit":
        break

    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })

    print("\nAgent:", result["messages"][-1].content)
```

```
You: What is 20 multiplied by 5?
Agent: 20 multiplied by 5 is 100.

You: What is 12 plus 30?
Agent: 12 plus 30 is 42.

You: exit
```

### A More Realistic Developer Agent

A four-tool agent that mixes lookups and calculations:

```python
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
    return projects.get(project.lower(), "Project information not available.")

@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width

@tool
def calculate_square(number: float) -> float:
    """Calculate the square of a number."""
    return number * number

llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

agent = create_agent(
    model=llm,
    tools=[get_java_version, get_project_info, calculate_area, calculate_square],
)

while True:
    question = input("\nYou: ")
    if question.lower() == "exit":
        break
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print("\nAgent:", result["messages"][-1].content)
```

Sample questions it can handle:

- *"What Java version are we using?"*
- *"Tell me about the Spring Boot project."*
- *"What is the square of 15?"*
- *"Calculate the area of a rectangle with length 10 and width 20."*

---

## 8. Conversation History

### Building a History List

Conversation history is just a list of alternating `HumanMessage` / `AIMessage` objects:

```python
from langchain_core.messages import HumanMessage, AIMessage

history = [
    HumanMessage(content="My name is Shiv."),
    AIMessage(content="Nice to meet you, Shiv!"),
    HumanMessage(content="I am learning Java."),
    AIMessage(content="That's great! Java is a powerful language."),
]
```

There's nothing special about `history` as a variable — it's an ordinary Python list you build up over time:

```python
history = []
history.append(HumanMessage(content="Hello"))
history.append(AIMessage(content="Hello! How can I help?"))
```

You can inspect it at any point:

```python
for message in history:
    print(type(message).__name__, ":", message.content)
```

```
HumanMessage : My name is Shiv.
AIMessage : Nice to meet you, Shiv!
HumanMessage : I am learning Java.
AIMessage : That's great! Java is a powerful language.
```

### `MessagesPlaceholder`

A single `{question}` variable can only hold one piece of text — it can't represent a whole list of role-tagged messages. `MessagesPlaceholder` solves that: it tells the prompt *"insert this list of messages here, exactly as messages."*

```python
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])
```

| | Holds |
|---|---|
| `{question}` | a single value |
| `MessagesPlaceholder("history")` | a list of role-tagged messages |

### Full Example with History

```python
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

history = [
    HumanMessage(content="My name is Shiv."),
    AIMessage(content="Nice to meet you, Shiv!"),
    HumanMessage(content="I am learning Java."),
    AIMessage(content="That's great! Java is a powerful language."),
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful programming tutor."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

messages = prompt.invoke({"history": history, "question": "What am I learning?"})
response = llm.invoke(messages)
print(response.content)  # "You are learning Java."
```

The model effectively sees:

```
SYSTEM  You are a helpful programming tutor.
HUMAN   My name is Shiv.
AI      Nice to meet you, Shiv!
HUMAN   I am learning Java.
AI      That's great! Java is a powerful language.
HUMAN   What am I learning?
```

### Inspecting What's Actually Sent to the LLM

Useful for debugging — shows the resolved message list after the template fills in:

```python
messages = prompt.invoke({"history": history, "question": "What am I learning?"})

for message in messages.messages:
    print(f"{type(message).__name__}: {message.content}")
```

---

## 9. Putting It All Together

A complete interactive chatbot with persistent memory:

```python
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
    ("system", "You are a helpful programming tutor. "
               "Remember the conversation and answer based on previous messages."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

while True:
    question = input("\nYou: ")
    if question.lower() == "exit":
        break

    messages = prompt.invoke({"history": history, "question": question})
    response = llm.invoke(messages)
    print("\nAI:", response.content)

    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=response.content))

print("\n\n========== HISTORY ==========")
for message in history:
    print(f"{type(message).__name__}: {message.content}")
```

**How it behaves:** if the user says *"My name is Shiv,"* the model replies *"Nice to meet you, Shiv!"* — and both messages get appended to `history`. On the next turn, *"What is my name?"* is sent along with the full prior exchange, so the model can correctly answer *"Your name is Shiv."*

---

## 10. Common Mistakes

**1. Forgetting the import**
`HumanMessage` and `AIMessage` must be imported from `langchain_core.messages` before use — a bare `HumanMessage(...)` without the import will fail.

**2. Only storing user messages**
If you append the user's message but never the model's reply, `history` no longer reflects the real conversation:

```python
# incomplete
history.append(HumanMessage(content=question))
```

```python
# correct
history.append(HumanMessage(content=question))
history.append(AIMessage(content=response.content))
```

**3. Duplicating the current question**
If you add the current question to `history` *before* calling `prompt.invoke()`, and the prompt also fills `{question}` separately, the same message appears twice. Append to history only **after** getting the response:

```python
messages = prompt.invoke({"history": history, "question": question})
response = llm.invoke(messages)

history.append(HumanMessage(content=question))
history.append(AIMessage(content=response.content))
```

**4. Assuming `AIMessage` always means "final answer"**
An `AIMessage` can carry `tool_calls` instead of a finished response — the agent may loop through several before it's actually done.

**5. Confusing `bind_tools()` with an agent**
`bind_tools()` only makes tools visible to the model. `create_agent()` is what actually runs the tool-call loop end to end.

---

## 11. Cheat Sheet

| Concept | What it does | Snippet |
|---|---|---|
| `ChatOpenAI` | Chat model interface | `ChatOpenAI(model=..., api_key=..., base_url=...)` |
| `ChatPromptTemplate` | Reusable structured prompt | `ChatPromptTemplate.from_messages([...])` |
| `StrOutputParser` | `AIMessage` → string | `prompt \| llm \| StrOutputParser()` |
| `HumanMessage` | A user message | `HumanMessage(content="Hello")` |
| `AIMessage` | A model message (may include tool calls) | `AIMessage(content="Hi!")` |
| `history` | List of past messages | `history = [HumanMessage(...), AIMessage(...)]` |
| `MessagesPlaceholder` | Injects `history` into a prompt | `MessagesPlaceholder(variable_name="history")` |
| `@tool` | Turns a function into a tool | `@tool` above a function with a docstring |
| `bind_tools()` | Exposes tools to the model (no execution loop) | `llm.bind_tools([tool1, tool2])` |
| `create_agent()` | Full tool-using agent | `create_agent(model=llm, tools=[...])` |
| `ToolMessage` | Result of a tool call | Produced automatically inside the agent loop |

---

## 12. Mental Models

**Basic chain**
```
Input → Prompt → LLM → AIMessage → Parser → String
```

**Messages**
```
HumanMessage → the user speaks
AIMessage    → the model speaks (possibly requesting a tool)
```

**History**
```
history = [HumanMessage, AIMessage, HumanMessage, AIMessage, ...]
```

**MessagesPlaceholder**
```
history → MessagesPlaceholder → Prompt
```
Think: *"put all these messages here."*

**Tool**
```
LLM → Tool → Result
```
A tool performs one operation.

**Agent**
```
User → Agent → LLM → choose tool → Tool → Result → LLM → Final answer
```
An agent decides *how* to accomplish the task, looping through tools as needed.

---

### The Full Picture

```
                      LANGCHAIN
        ┌────────────────┼────────────────┐
        │                │                │
     Prompts          Messages           Tools
        │                │                │
ChatPromptTemplate        │             @tool
        │          HumanMessage / AIMessage
        │                │
        │             history
        │                │
        │        MessagesPlaceholder
        └────────────────┼────────────────┘
                          │
                     ChatOpenAI
                          │
                      AIMessage
                          │
                  tool_calls present?
                 ┌────────┴────────┐
               Yes                 No
                │                   │
              Tool              Final Answer
                │
           ToolMessage
                │
               LLM
                │
          Final Answer
```

This progression — from a single prompt/model call, through structured messages and reusable chains, into tool-using agents with real memory — is the foundation for building more advanced LangChain applications: memory-enabled chatbots, API-powered agents, RAG pipelines, research agents, coding assistants, and multi-agent LangGraph workflows.