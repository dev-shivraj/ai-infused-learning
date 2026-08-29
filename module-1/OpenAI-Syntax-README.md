## OpenAI Python SDK Syntax Cheat Sheet
##### It covers 80–90% syntax being used on regular basis

---

### Most Important Syntax to Memorize

**If you forget everything else, remember this structure:**

---
---
```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model=“MODEL_NAME”,
    messages=[
        {
            “role”: “system”,
            “content”: “SYSTEM_INSTRUCTION”
        },
        {
            “role”: “user”,
            “content”: “USER_REQUEST”
        }
    ]
)

print(response.choices[0].message.content)
```

**And the modern Responses API pattern:**

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model=“MODEL_NAME”,
    input=“USER_REQUEST”
)

print(response.output_text)
```

---
---


**This README covers the most commonly used OpenAI Python SDK syntax and concepts needed for practical AI/LLM application development.**

The goal is not to memorize every API parameter.

The goal is to understand the structure:

```text
Client
↓
API method
↓
Model
↓
Input
↓
Options
↓
Response
```

---

**1. Installation**

Install the OpenAI SDK and python-dotenv:

```bash
pip install openai python-dotenv
```

Verify:

```bash
pip show openai
pip show python-dotenv
```

---

**2. Recommended Project Structure**

```text
openai/
├── .env
├── basic-openai-syntax.py
└── basic-openai-groq.py
```

---

**3. Environment Variables**

Create a .env file:

```text
OPENAI_API_KEY=your_openai_api_key
```

For Groq:

```text
GROQ_API_KEY=your_groq_api_key
```

Never commit .env to Git.

.gitignore:

```text
.venv/
.env
pycache/
*.pyc
```

---

**4. Importing the SDK**

```python
from openai import OpenAI
```

This imports the OpenAI client from the OpenAI Python SDK.

Conceptually:

```text
Your Python application
↓
OpenAI Python SDK
↓
API Provider
↓
AI Model
```

---

**5. Loading .env**

Install:

```bash
pip install python-dotenv
```

Import:

```python
from dotenv import load_dotenv
```

Load environment variables:

```python
load_dotenv()
```

After this, variables from .env become available through the environment.

For example:

```text
OPENAI_API_KEY=sk-xxxxxxxx
```

can be accessed using:

```python
import os

api_key = os.getenv(“OPENAI_API_KEY”)
```

---

**6. Creating the OpenAI Client**

Simplest Version

```python
from openai import OpenAI

client = OpenAI()
```

OpenAI() automatically looks for:

```text
OPENAI_API_KEY
```

in the environment.

Therefore:

```python
load_dotenv()

client = OpenAI()
```

is enough when .env contains:

```text
OPENAI_API_KEY=…
```

---

**7. Explicit API Key**

You can also provide the key manually:

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv(“OPENAI_API_KEY”)
)
```

This is useful when you want explicit control over which key is used.

---

**8. Custom API Provider**

The OpenAI SDK can also communicate with providers that expose an OpenAI-compatible API.

Example using Groq:

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv(“GROQ_API_KEY”),
    base_url=“https://api.groq.com/openai/v1”,
)
```

The important part is:

```python
base_url=“https://api.groq.com/openai/v1”
```

This tells the SDK:

“Send API requests to Groq instead of the default OpenAI endpoint.”

Architecture:

```text
Your Python Application
↓
OpenAI Python SDK
↓
OpenAI-compatible API
↓
Groq
↓
Groq Model
```

---

**9. Basic Chat Completion**

The basic Chat Completions syntax:

```python
response = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        {
            “role”: “user”,
            “content”: “Tell me a joke.”
        }
    ],
)
```

Then:

```python
print(response.choices[0].message.content)
```

This is one of the most important patterns to understand.

---

**10. Complete Basic Example**

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        { “role”: “system”, “content”: “You are a witty travel guide.” },
        { “role”: “user”, “content”: “Suggest one thing to do in Bangalore.” },
    ],
)

print(response.choices[0].message.content)
```

---

**11. Understanding messages**

The messages parameter represents the conversation.

```python
messages=[
    {“role”: “system”, “content”: “…”},
    {“role”: “user”, “content”: “…”},
]
```

Common roles:

```text
system
user
assistant
```

---

**12. System Message**

The system message provides instructions about how the model should behave.

Example:

```python
{
    “role”: “system”,
    “content”: “You are a Java teacher.”
}
```

Meaning:

“You are a Java teacher. Answer questions accordingly.”

---

**13. User Message**

The user message contains the user’s request.

```python
{
    “role”: “user”,
    “content”: “Explain HashMap.”
}
```

---

**14. Assistant Message**

An assistant message represents a previous model response.

```python
{
    “role”: “assistant”,
    “content”: “HashMap stores key-value pairs.”
}
```

This becomes useful when maintaining conversation history.

---

**15. Conversation History**

The model generally needs the relevant conversation history supplied as part of the request.

Example:

```python
messages = [
    { “role”: “system”, “content”: “You are a helpful Java teacher.” },
    { “role”: “user”, “content”: “What is HashMap?” },
    { “role”: “assistant”, “content”: “HashMap stores key-value pairs.” },
    { “role”: “user”, “content”: “How does it handle collisions?” }
]

response = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=messages,
)
```

Conceptually:

```text
User question
↓
Conversation history
↓
LLM
↓
New response
```

---

**16. Model**

The model parameter determines which AI model processes the request.

```python
response = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        {“role”: “user”, “content”: “Hello”}
    ],
)
```

Different providers have different model IDs.

Example:

OpenAI:

```python
model=“gpt-4o-mini”
```

Groq:

```python
model=“openai/gpt-oss-20b”
```

Always check the provider’s current model list/documentation.

---

**17. Understanding the Response**

The API returns a response object.

Conceptually:

```text
response
│
├── id
├── model
├── choices
│   │
│   └── [0]
│       │
│       └── message
│           ├── role
│           └── content
│
└── usage
```

---

**18. Extracting the Generated Text**

The commonly used expression:

```python
response.choices[0].message.content
```

Breakdown:

```text
response
↓
choices
↓
[0]
↓
message
↓
content
```

Meaning:

“Get the generated text from the first response choice.”

---

**19. choices**

The response can contain one or more choices.

```python
response.choices
```

To access the first choice:

```python
response.choices[0]
```

Then:

```python
response.choices[0].message
```

Then:

```python
response.choices[0].message.content
```

---

**20. Token Usage**

You can inspect token usage:

```python
print(response.usage)
```

Conceptually:

```text
usage
├── input/prompt tokens
├── output/completion tokens
└── total tokens
```

Token usage matters for:

* Cost
* Rate limits
* Context windows
* Performance

---

**21. Temperature**

Some generation APIs/models expose:

```python
temperature=0.7
```

Conceptually:

```text
Lower temperature
↓
More predictable

Higher temperature
↓
More variation
```

Example:

```python
response = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        {“role”: “user”, “content”: “Give me a creative story idea.”}
    ],
    temperature=0.8,
)
```

Important:

The exact supported parameters depend on the API and model. Do not assume every current model supports every generation parameter.

---

**22. Output / Token Limits**

You may encounter parameters for limiting output length.

For example, older/common Chat Completions code may use:

```python
max_tokens=500
```

The exact parameter can vary across newer APIs/models, so always check the current API documentation before using it.

The basic concept is:

```text
Maximum output
↓
Control how much the model generates
```

---

**23. Streaming**

Without streaming:

```python
response = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        {“role”: “user”, “content”: “Write a story.”}
    ],
)

print(response.choices[0].message.content)
```

The application waits for the complete response.

With streaming:

```python
stream = client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        {“role”: “user”, “content”: “Write a story.”}
    ],
    stream=True,
)

for chunk in stream:
print(chunk.choices[0].delta.content or “”, end=””)
```

Conceptually:

```text
Without streaming:

Request
↓
Wait
↓
Complete response

With streaming:

Request
↓
Chunk
↓
Chunk
↓
Chunk
↓
Chunk
↓
Complete response
```

Streaming is commonly used in chat applications.

---

**24. Async OpenAI Client**

For asynchronous applications:

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()
```

Then:

```python
response = await client.chat.completions.create(
    model=“gpt-4o-mini”,
    messages=[
        {“role”: “user”, “content”: “Hello”}
    ],
)
```

This is useful with:

* FastAPI
* Async Python
* Concurrent applications
* High-throughput backend services

---

**25. Error Handling**

Basic error handling:

```python
from openai import OpenAI

client = OpenAI()

try:
    response = client.chat.completions.create(
        model=“gpt-4o-mini”,
        messages=[
            {“role”: “user”, “content”: “Hello”}
        ],
    )

    print(response.choices[0].message.content)

except Exception as e:
print(f”Error: {e}”)
```

---

**26. Specific API Errors**

You can handle specific errors.

Example:

```python
from openai import OpenAI, RateLimitError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model=“gpt-4o-mini”,
        messages=[
            {“role”: “user”, “content”: “Hello”}
        ],
    )

except RateLimitError:
    print(“Rate limit or quota problem.”)
```

You may encounter different API/client errors depending on the failure.

Common categories include:

* Authentication errors
* Rate limit errors
* Invalid request errors
* Permission errors
* Not found errors
* Connection errors
* Server errors

---

**27. Modern Responses API**

You will encounter two major API styles:


Chat Completions
```text
client.chat.completions.create()
```

Responses API
```text
client.responses.create()
```

The newer Responses API is designed as a more unified interface for modern model interactions and tool use.

Basic conceptual syntax:

```python
response = client.responses.create(
    model=”…”,
    input=“Tell me a joke.”
)
```

The Responses API should be learned alongside Chat Completions when working with current OpenAI projects.

---

**28. Responses API — Basic Mental Model**

Chat Completions:

```python
response = client.chat.completions.create(
    model=”…”,
    messages=[
        {“role”: “user”, “content”: “Hello”}
    ]
)
```

Responses API:

```python
response = client.responses.create(
    model=”…”,
    input=“Hello”
)
```

Think:

```text
Chat Completions
↓
messages

Responses API
↓
input
```

The exact response access patterns differ, so don’t blindly use:

```python
response.choices[0].message.content
```

for Responses API responses.

---

**29. Structured Outputs**

A common real-world requirement is:

“Return data in a specific structure.”

Instead of:

```text
John is 25 years old.
```

you may want:

```json
{
    “name”: “John”,
    “age”: 25
}
```

Modern OpenAI APIs support structured outputs using schemas.

A common approach is Pydantic:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
```

The exact structured-output syntax depends on the API method/SDK version being used.

Core idea:

```text
Natural language request
↓
Structured schema
↓
LLM
↓
Predictable structured data
```

This is much more reliable than simply asking:

“Please return valid JSON.”

---

**30. Why Structured Outputs Matter**

Without structured output:

```text
LLM
↓
Free-form text
↓
Your application must parse it
```

With structured output:

```text
LLM
↓
Defined schema
↓
Validated structured data
↓
Your application
```

Useful for:

* API responses
* Data extraction
* Classification
* Forms
* Database operations
* Backend services

---

**31. Tool / Function Calling**

One of the most important AI application concepts.

Suppose the user asks:

“What’s the weather in Bangalore?”

The model should not necessarily invent the current weather.

Instead:

```text
User
↓
LLM
↓
Decides to call get_weather()
↓
Your Python application
↓
Weather API
↓
Weather result
↓
LLM
↓
Final response
```

---

**32. Defining a Tool**

Conceptually:

```python
tools = [
    {
        “type”: “function”,
        “function”: {
        “name”: “get_weather”,
        “description”: “Get current weather for a city”,
            “parameters”: {
                “type”: “object”,
                “properties”: {
                    “city”: {
                        “type”: “string”
                    }
                },
                “required”: [“city”]
            }
        }
    }
]
```

Then:

```python
response = client.chat.completions.create(
    model=”…”,
    messages=messages,
    tools=tools,
)
```

The exact tool-calling structure differs between API interfaces, especially between Chat Completions and Responses.

The important concept is:

```text
Tool definition
↓
Model decides whether to call it
↓
Your application executes it
↓
Result goes back to model
```

---

**33. Function Calling Flow**

A complete conceptual flow:

```text

1. User asks a question
    ↓
2. Send question + tool definitions to model
    ↓
3. Model requests a tool call
    ↓
4. Your application receives tool call
    ↓
5. Your application executes function
    ↓
6. Send function result back
    ↓
7. Model generates final answer
```

This is the foundation of:

* AI agents
* Tool use
* API agents
* Database agents
* Autonomous workflows

---

**34. Multimodal Input**

Modern models can work with multiple input types.

Conceptually:

```text
Text
Image
Audio
↓
Multimodal model
↓
Response
```

For example:

```text
User
↓
Image + question
↓
Vision-capable model
↓
Answer
```

Applications include:

* Image analysis
* Screenshot analysis
* OCR-like workflows
* Document understanding
* Visual question answering

---

**35. Image Input**

Instead of only sending text:

```python
{
    “role”: “user”,
    “content”: “What is this?”
}
```

multimodal APIs can accept content containing different input parts, such as:

```text
text
+
image
```

The exact syntax depends on the API/model being used.

---

**36. Embeddings**

Embeddings convert text into numerical vectors.

Example concept:

```text
“Java HashMap stores key-value pairs”
↓
Embedding
↓
[0.023, -0.182, 0.743, …]
```

Conceptually:

```python
response = client.embeddings.create(
    model=“text-embedding-model”,
    input=“Java HashMap stores key-value pairs”
)
```

Embeddings are commonly used for:

* Semantic search
* Similarity search
* Recommendations
* RAG
* Document retrieval

---

**37. What Is an Embedding?**

An embedding represents the semantic meaning of data as numbers.

For example:

```text
“Java HashMap”
↓
Vector A

“Java Map implementation”
↓
Vector B
```

Because the meanings are related, their vectors can be close to each other in vector space.

This enables semantic search.

---

**38. RAG**

RAG means:

Retrieval-Augmented Generation

RAG is an architecture, not simply one API call.

Typical flow:

```text
Documents
↓
Chunking
↓
Embeddings
↓
Vector Database
↓
User Question
↓
Similarity Search
↓
Relevant Documents
↓
LLM
↓
Answer
```

Typical use cases:

* Chat with PDFs
* Company knowledge bases
* Documentation assistants
* Internal search
* Customer support bots

---

**39. Moderation**

Moderation APIs can be used to classify potentially unsafe content.

Conceptually:

```python
response = client.moderations.create(
    model=”…”,
    input=”…”
)
```

The exact supported models and response structure can change, so check the current API documentation when implementing this.

---

**40. Image Generation**

AI APIs can also generate images from text prompts.

Conceptually:

```text
Prompt
↓
Image generation model
↓
Generated image
```

Typical use cases:

* Marketing images
* Illustrations
* Product concepts
* UI assets
* Creative applications

Image generation uses image-generation APIs rather than the basic chat-completion pattern.

---

**41. Audio — Speech to Text**

Audio can be converted into text:

```text
Microphone
↓
Audio
↓
Speech-to-text model
↓
Text
```

Useful for:

* Voice assistants
* Meeting transcription
* Voice search
* Notes
* Accessibility

---

**42. Audio — Text to Speech**

The reverse flow:

```text
LLM response
↓
Text-to-speech model
↓
Audio
↓
User hears response
```

Useful for:

* Voice assistants
* Accessibility
* Narration
* Conversational applications

---

**43. Async vs Sync**

Synchronous:

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model=”…”,
    input=“Hello”
)
```

Asynchronous:

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()

response = await client.responses.create(
    model=”…”,
    input=“Hello”
)
```

Mental model:

```text
Sync
↓
Do request
↓
Wait
↓
Get result

Async
↓
Start request
↓
Other work can happen
↓
Await result
```

---

**44. Common Client Pattern**

For OpenAI:

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()
```

For a compatible provider:

```python
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv(“GROQ_API_KEY”),
    base_url=“https://api.groq.com/openai/v1”,
)
```

---

**45. OpenAI vs Groq**

The conceptual difference:

```text
OPENAI

OpenAI SDK
↓
OpenAI API
↓
OpenAI model

GROQ

OpenAI SDK
↓
Groq OpenAI-compatible API
↓
Groq model
```

The SDK can remain the same because Groq exposes an OpenAI-compatible interface.

---

**46. Complete Groq Example**

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv(“GROQ_API_KEY”),
    base_url=“https://api.groq.com/openai/v1”,
)

response = client.chat.completions.create(
    model=“openai/gpt-oss-20b”,
    messages=[
        {
            “role”: “system”,
            “content”: “You are a funny joke teller.”
        },
        {
            “role”: “user”,
            “content”: “Tell me a joke.”
        },
    ],
)

print(response.choices[0].message.content)
```

---

**47. Important Mental Model**

Always think in these layers:

```text
┌───────────────────────────────────┐
│       Your Python Application     │
└─────────────────┬─────────────────┘
│
▼
┌───────────────────────────────────┐
│       Python SDK / Client         │
│       OpenAI()                    │
└─────────────────┬─────────────────┘
│
▼
┌───────────────────────────────────┐
│            API Provider           │
│                                   │
│       OpenAI / Groq / etc.        │
└─────────────────┬─────────────────┘
│
▼
┌───────────────────────────────────┐
│             AI Model              │
│                                   │
│       GPT / Llama / etc.          │
└───────────────────────────────────┘
```

Three concepts must not be confused:

```text
SDK
API Provider
AI Model
```

They are different things.

---

**48. Core Syntax Cheat Sheet**

Client

```python
client = OpenAI()
```

Explicit API key

```python
client = OpenAI(
api_key=os.getenv(“OPENAI_API_KEY”)
)
```

Custom provider

```python
client = OpenAI(
    api_key=os.getenv(“GROQ_API_KEY”),
    base_url=“https://api.groq.com/openai/v1”,
)
```

Chat completion

```python
response = client.chat.completions.create(
    model=”…”,
    messages=[
        {“role”: “user”, “content”: “…”}
    ],
)
```

Extract text

```python
text = response.choices[0].message.content
```

Streaming

```python
stream = client.chat.completions.create(
    model=”…”,
    messages=[
        {“role”: “user”, “content”: “…”}
    ],
    stream=True,
)

for chunk in stream:
print(chunk.choices[0].delta.content or “”, end=””)
```

Usage

```python
print(response.usage)
```

Async

```python
from openai import AsyncOpenAI

client = AsyncOpenAI()

response = await client.chat.completions.create(
    model=”…”,
    messages=[
        {“role”: “user”, “content”: “…”}
    ],
)
```

Responses API

```python
response = client.responses.create(
    model=”…”,
    input=“Hello”
)
```

Embeddings

```python
response = client.embeddings.create(
    model=”…”,
    input=“Some text”
)
```

Moderation

```python
response = client.moderations.create(
    model=”…”,
    input=“Some text”
)
```

---

**49. 80–90% Syntax Roadmap**

These are the concepts worth learning in order.

Part 1 — Fundamentals

```text

1. API key
2. .env
3. load_dotenv()
4. OpenAI()
5. api_key
6. base_url
7. model
8. messages
9. system
10. user
11. assistant
12. response
13. choices
14. message
15. content
```

Part 2 — Generation

```text
16. temperature
17. Output/token limits
18. Conversation history
19. usage
20. Error handling
```

Part 3 — Streaming

```text
21. stream=True
22. stream
23. chunks
24. delta
25. Building streamed output
```

Part 4 — Modern OpenAI API

```text
26. Responses API
27. input
28. output
29. output_text
30. Structured outputs
31. JSON schema
32. Pydantic
```

Part 5 — Tools

```text
33. tools
34. Function definition
35. Tool call
36. Tool arguments
37. Executing the function
38. Returning the result
39. Agent loop
```

Part 6 — Multimodal

```text
40. Text input
41. Image input
42. Audio input
43. Speech-to-text
44. Text-to-speech
45. Image generation
```

Part 7 — AI Application Foundations

```text
46. Embeddings
47. Vector search
48. RAG
49. Moderation
50. Async
51. Retries
52. Production error handling
```

---

**50. Most Important Syntax to Memorize**

If you forget everything else, remember this structure:

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model=“MODEL_NAME”,
    messages=[
        {
            “role”: “system”,
            “content”: “SYSTEM_INSTRUCTION”
        },
        {
            “role”: “user”,
            “content”: “USER_REQUEST”
        }
    ]
)

print(response.choices[0].message.content)
```

And the modern Responses API pattern:

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model=“MODEL_NAME”,
    input=“USER_REQUEST”
)

print(response.output_text)
```

---

**51. Final Mental Model**

When reading OpenAI code, ask these questions in order:

```text

1. Which SDK is being used?
    ↓
2. Which API provider?
    ↓
3. Which model?
    ↓
4. What input is being sent?
    ↓
5. What options are configured?
    ↓
6. Is the request streamed?
    ↓
7. What does the response look like?
    ↓
8. How is the generated output extracted?
    ↓
9. Are tools involved?
    ↓
10. Are structured outputs involved?
```

The fundamental pattern is:

```text
CLIENT
↓
MODEL
↓
INPUT
↓
REQUEST
↓
RESPONSE
↓
OUTPUT
```

Once this mental model is clear, most OpenAI SDK code becomes much easier to understand.

---

**52. Quick Reference Table**

Concept	Common Syntax
Load .env	load_dotenv()
Create client	OpenAI()
API key	api_key=...
Custom provider	base_url=...
Chat API	client.chat.completions.create()
Model	model="..."
Input	messages=[...]
System instruction	role="system"
User input	role="user"
Previous response	role="assistant"
Generated text	response.choices[0].message.content
Usage	response.usage
Streaming	stream=True
Async client	AsyncOpenAI()
Modern API	client.responses.create()
Structured output	Schema / Pydantic
Tools	tools=[...]
Embeddings	client.embeddings.create()
Moderation	client.moderations.create()
Image/audio	Multimodal APIs

---

**53. Key Takeaways**

1. SDK is not the same as API provider

```text
OpenAI SDK
↓
Can communicate with compatible APIs
```

2. API key identifies/authenticates the provider

```text
OPENAI_API_KEY
↓
OpenAI

GROQ_API_KEY
↓
Groq
```

3. Model determines the AI engine

```text
Provider
↓
Model
↓
Generation
```

4. Messages represent conversation context

```text
system
user
assistant
```

5. Response contains much more than the generated text

```text
response
├── metadata
├── choices/output
└── usage
```

6. Streaming gives incremental output

```text
Request
↓
Chunk
↓
Chunk
↓
Chunk
↓
Final output
```

7. Tools allow the model to interact with your application

```text
LLM
↓
Tool call
↓
Your code
↓
External system
↓
Tool result
↓
LLM
↓
Answer
```

8. Structured outputs make LLM responses easier for applications to consume

```text
LLM
↓
Schema
↓
Structured data
↓
Application
```

9. Embeddings enable semantic search and RAG

```text
Text
↓
Embedding
↓
Vector
↓
Similarity search
↓
Relevant information
```

10. The API evolves

OpenAI’s SDK and APIs continue to evolve.

Therefore:

* Understand the concepts.
* Learn the current API pattern.
* Check current model/API documentation when implementing production code.
* Don’t blindly copy old examples.
* Know the difference between Chat Completions and the newer Responses API.

---

**54. The One Diagram to Remember**

```text
AI APPLICATION
│
▼
┌───────────────┐
│     CLIENT    │
│   OpenAI()    │
└───────┬───────┘
│
▼
┌───────────────┐
│  API PROVIDER │
│               │
│ OpenAI / Groq │
└───────┬───────┘
│
▼
┌───────────────┐
│     MODEL     │
│ GPT / Llama   │
└───────┬───────┘
│
▼
┌───────────────┐
│     INPUT     │
│               │
│ text/image/   │
│ audio/tools   │
└───────┬───────┘
│
▼
┌───────────────┐
│    RESPONSE   │
│               │
│ text/JSON/    │
│ tool call/etc │
└───────────────┘
```

This is the mental model that connects almost everything in the OpenAI SDK.