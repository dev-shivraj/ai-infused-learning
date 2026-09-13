# Gradio — Practical Cheat Sheet

A practical reference covering the syntax and patterns used most frequently when building AI, ML, LLM, RAG, and Python applications with [Gradio](https://www.gradio.app/).

## Table of Contents

1. [What is Gradio?](#1-what-is-gradio)
2. [Installation](#2-installation)
3. [The Basic Gradio Pattern](#3-the-basic-gradio-pattern)
4. [`gr.Interface`](#4-grinterface)
5. [Interface Parameters](#5-interface-parameters)
6. [Input & Output Components](#6-input--output-components)
7. [Layout](#7-layout)
8. [Component Reference](#8-component-reference)
9. [`gr.Blocks`](#9-grblocks)
10. [Events](#10-events)
11. [State](#11-state)
12. [Dynamic Updates & Visibility](#12-dynamic-updates--visibility)
13. [Examples & Progress](#13-examples--progress)
14. [Streaming & Async](#14-streaming--async)
15. [Theming, CSS & JS](#15-theming-css--js)
16. [Launching & Deployment](#16-launching--deployment)
17. [API Exposure](#17-api-exposure)
18. [Common Application Patterns](#18-common-application-patterns)
19. [Complete Examples](#19-complete-examples)
20. [Quick Reference](#20-quick-reference)
21. [Learning Priority](#21-learning-priority)
22. [Mental Model](#22-mental-model)

---

## 1. What is Gradio?

Gradio is a Python library for quickly building web UIs around Python functions, machine-learning models, and AI applications.

```
Python Function / Model → Gradio → Web UI
```

**Minimal example:**

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

---

## 2. Installation

```bash
pip install gradio              # install
pip install --upgrade gradio    # upgrade
pip show gradio                 # check version
```

```python
import gradio as gr
```

---

## 3. The Basic Gradio Pattern

```python
import gradio as gr

def my_function(input):
    # process input
    return output

demo = gr.Interface(fn=my_function, inputs=..., outputs=...)
demo.launch()
```

```
Function → Input Components → Function executes → Output Components
```

---

## 4. `gr.Interface`

The simplest way to expose a Python function through a UI.

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

---

## 5. Interface Parameters

```python
demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(),
    outputs=gr.Textbox(),
    title="Greeting App",
    description="A simple Gradio application",
    api_name="greet"
)
```

| Parameter | Purpose |
|---|---|
| `fn` | Python function to run |
| `inputs` | Input component(s) |
| `outputs` | Output component(s) |
| `title` | Application title |
| `description` | Description shown in UI |
| `api_name` | Expose function as an API endpoint |
| `examples` | Predefined example inputs |
| `flagging_mode` | Feedback/flagging configuration |

---

## 6. Input & Output Components

### Textbox

```python
name = gr.Textbox(
    label="Name",
    placeholder="Enter your name",
    value="Shivraj",
    lines=1
)
```

Multiline / with max length:

```python
text = gr.Textbox(
    label="Question",
    placeholder="Ask something…",
    lines=5,
    max_lines=10
)
```

Simple text output: `outputs = "text"` or `gr.Textbox(label="Answer")`

### Multiple Inputs

```python
def add(a, b):
    return a + b

demo = gr.Interface(
    fn=add,
    inputs=[gr.Number(label="First Number"), gr.Number(label="Second Number")],
    outputs=gr.Number(label="Result")
)
```

Function arguments map to inputs **in order**.

### Multiple Outputs

```python
def calculate(a, b):
    return a + b, a * b

demo = gr.Interface(
    fn=calculate,
    inputs=[gr.Number(), gr.Number()],
    outputs=[gr.Number(label="Sum"), gr.Number(label="Product")]
)
```

The return order must match the output order.

### Number & Slider

```python
gr.Number(label="Temperature", minimum=0, maximum=2, value=0.7, step=0.1)

gr.Slider(minimum=0, maximum=2, value=0.7, step=0.1, label="Temperature")
```

### Dropdown, Radio, Checkbox

```python
gr.Dropdown(choices=["GPT", "Claude", "Gemini"], label="Model", value="GPT")
gr.Dropdown(choices=["GPT", "Claude"], allow_custom_value=True)

gr.Radio(choices=["Fast", "Balanced", "Accurate"], label="Mode")

gr.Checkbox(label="Enable feature", value=True)
gr.CheckboxGroup(choices=["Web Search", "RAG", "Citations"], label="Features")
```

### Media & Files

```python
gr.Image(label="Upload Image")          # or type="filepath" / type="numpy"
gr.Audio(label="Upload Audio")
gr.Video(label="Upload Video")
gr.File(label="Upload File")
gr.File(file_count="multiple")          # multiple files
```

### Structured Data

```python
gr.Dataframe(headers=["Name", "Age"], label="Users")
gr.JSON(label="Response")               # e.g. return {"name": "Shivraj", "age": 27}
gr.HTML("Hello")                        # custom HTML
gr.Label()                              # e.g. return {"cat": 0.85, "dog": 0.15}
```

### Buttons

```python
gr.Button("Submit")
gr.Button("Primary", variant="primary")
gr.Button("Secondary", variant="secondary")
gr.Button("Stop", variant="stop")
```

### Markdown

```python
gr.Markdown("# My Application")

gr.Markdown(
    """
    # AI Assistant
    Ask questions and get answers.
    """
)
```

Useful for headings, descriptions, instructions, documentation, and status messages.

---

## 7. Layout

### Row (horizontal)

```python
with gr.Row():
    input_box = gr.Textbox()
    submit = gr.Button("Submit")
```

### Column (vertical — the default)

```python
with gr.Column():
    input_box = gr.Textbox()
    output_box = gr.Textbox()
    button = gr.Button("Submit")
```

### Tabs

```python
with gr.Blocks() as demo:
    with gr.Tab("Chat"):
        gr.Markdown("Chat application")
    with gr.Tab("Settings"):
        gr.Markdown("Settings")
```

### Accordion

```python
with gr.Accordion("Advanced Settings"):
    temperature = gr.Slider(minimum=0, maximum=2, value=0.7)
```

---

## 8. Component Reference

| Component | Purpose |
|---|---|
| `gr.Textbox` | Text input/output |
| `gr.Markdown` | Markdown content |
| `gr.Button` | Button |
| `gr.Number` | Number |
| `gr.Slider` | Numeric range |
| `gr.Dropdown` | Select option |
| `gr.Radio` | Single selection |
| `gr.Checkbox` | Boolean option |
| `gr.CheckboxGroup` | Multiple selections |
| `gr.Image` | Image input/output |
| `gr.Audio` | Audio input/output |
| `gr.Video` | Video |
| `gr.File` | File upload |
| `gr.Dataframe` | Tables |
| `gr.JSON` | JSON data |
| `gr.HTML` | HTML |
| `gr.Label` | Classification labels |
| `gr.Chatbot` | Chat UI |
| `gr.State` | Hidden state |
| `gr.Accordion` | Collapsible section |

---

## 9. `gr.Blocks`

`gr.Blocks` is the core API for building custom applications — more flexible than `gr.Interface`.

```python
import gradio as gr

with gr.Blocks() as demo:
    textbox = gr.Textbox(label="Name")
    button = gr.Button("Submit")
    output = gr.Textbox(label="Result")

    button.click(fn=greet, inputs=textbox, outputs=output)

demo.launch()
```

```
Blocks
├── Components
├── Layout
├── Events
└── State
```

### Configuration

```python
with gr.Blocks(title="My Application", theme=gr.themes.Soft()) as demo:
    ...
```

---

## 10. Events

Events are the heart of `gr.Blocks`.

| Event | Fires when… |
|---|---|
| `.click()` | a button is clicked |
| `.submit()` | Enter is pressed / form submitted |
| `.change()` | a component's value changes |
| `.input()` | the user is entering/changing input |
| `.upload()` | a file/image is uploaded |
| `.select()` | an item is selected |
| `.clear()` | a value is cleared |
| `.start()` | a streaming/recording event begins |
| `.load()` | the page/component loads |

### Button `.click()`

```python
button.click(fn=greet, inputs=name, outputs=output)
button.click(fn=calculate, inputs=[a, b], outputs=result)  # multiple inputs
```

### Textbox `.submit()`

Triggered on Enter — very useful for chat apps.

```python
textbox.submit(fn=greet, inputs=textbox, outputs=output)
```

### `.change()`, `.input()`, `.upload()`, `.clear()`, `.select()`

```python
dropdown.change(fn=change_model, inputs=dropdown, outputs=status)
textbox.input(fn=process, inputs=textbox, outputs=output)
image.upload(fn=process_image, inputs=image, outputs=result)
textbox.clear(fn=clear_function, inputs=None, outputs=output)
dropdown.select(fn=handle_selection, inputs=dropdown, outputs=output)
```

### Wiring the Same Function to Multiple Events

```python
button.click(fn=process, inputs=input_box, outputs=output_box)
input_box.submit(fn=process, inputs=input_box, outputs=output_box)
```

```
Click Submit  OR  Press Enter  →  Same function
```

---

## 11. State

`gr.State` stores values between events without displaying them in the UI. Useful for conversation history, session info, counters, and configuration.

```python
history = gr.State([])

button.click(fn=process, inputs=[message, history], outputs=[output, history])
```

### Example: Counter

```python
import gradio as gr

def increment(count):
    count += 1
    return count, count

with gr.Blocks() as demo:
    state = gr.State(0)
    button = gr.Button("Increment")
    output = gr.Number()

    button.click(fn=increment, inputs=state, outputs=[output, state])

demo.launch()
```

### Returning Multiple Values

```python
def process(name, age):
    return f"Name: {name}", age * 2

button.click(fn=process, inputs=[name, age], outputs=[name_output, age_output])
```

Order matters on both sides.

---

## 12. Dynamic Updates & Visibility

```python
def update_visibility(enabled):
    return gr.update(visible=enabled)

checkbox.change(fn=update_visibility, inputs=checkbox, outputs=component)
```

Depending on the Gradio version, updates may also be returned as a new component configuration:

```python
def update_dropdown():
    return gr.Dropdown(choices=["A", "B", "C"])
```

**Visibility:**

```python
output = gr.Textbox(visible=False)   # hidden initially
```

```
User action → Event → Update component → visible=True
```

**Interactivity:**

```python
gr.Textbox(interactive=True)   # editable
gr.Textbox(interactive=False)  # read-only
```

---

## 13. Examples & Progress

### Predefined Examples

```python
examples = gr.Examples(
    examples=[["Hello"], ["How are you?"], ["Explain Java"]],
    inputs=textbox
)
```

With `gr.Interface`:

```python
demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(),
    outputs=gr.Textbox(),
    examples=[["Shivraj"], ["John"], ["Alice"]]
)
```

### Progress Tracking

```python
def process(progress=gr.Progress()):
    for i in range(10):
        progress((i + 1) / 10)
    return "Done"
```

### Queueing

Useful for longer-running tasks or multiple concurrent users.

```python
demo.queue()
demo.launch()
```

---

## 14. Streaming & Async

### Streaming Output

Important for LLM applications — `yield` partial results instead of `return`ing the complete answer.

```python
def generate_response(message):
    response = ""
    for token in ["Hello", " ", "Shivraj", "!"]:
        response += token
        yield response

button.click(fn=generate_response, inputs=message, outputs=output)
```

### Async Functions

```python
async def process(message):
    result = await some_async_function(message)
    return result

button.click(fn=process, inputs=input_box, outputs=output_box)
```

Useful with asynchronous APIs and LLM clients.

---

## 15. Theming, CSS & JS

### Built-in Themes

```python
gr.themes.Default()
gr.themes.Soft()
gr.themes.Monochrome()
gr.themes.Glass()
gr.themes.Base()
```

```python
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    ...
```

### Custom CSS

```python
css = """
#title {
    text-align: center;
}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1 id='title'>My AI App</h1>")
```

Use custom CSS sparingly unless you really need it.

### Custom JavaScript

```python
js = """
function() {
    console.log("Application loaded");
}
"""

with gr.Blocks(js=js) as demo:
    ...
```

More advanced — not needed for most applications.

---

## 16. Launching & Deployment

```python
demo.launch()                                   # basic
demo.launch(share=True)                         # temporary public link (demos only, not production)
demo.launch(server_name="0.0.0.0")               # bind host
demo.launch(server_port=7860)                    # set port
demo.launch(server_name="0.0.0.0", server_port=7860)  # common Docker-style setup
demo.launch(inbrowser=False)                     # don't auto-open browser
```

---

## 17. API Exposure

```python
button.click(fn=process, inputs=input_box, outputs=output_box, api_name="process")
```

```
Client → Gradio API → Python Function → Result
```

This is useful when another application needs to call your Gradio app programmatically. Not every UI event should automatically become a public API — configure exposure deliberately for your Gradio version.

---

## 18. Common Application Patterns

### Chatbot (`gr.Chatbot`)

```python
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    message = gr.Textbox()
    send = gr.Button("Send")

    send.click(fn=chat_function, inputs=message, outputs=chatbot)

demo.launch()
```

Modern message-append pattern:

```python
def respond(message, history):
    answer = "Hello!"
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": answer})
    return history

message.submit(fn=respond, inputs=[message, chatbot], outputs=chatbot)
```

### `gr.ChatInterface` (simplest chatbot)

```python
import gradio as gr

def chat(message, history):
    return f"You said: {message}"

demo = gr.ChatInterface(fn=chat, title="AI Assistant", description="Ask me anything")
demo.launch()
```

### Typical LLM App

```python
def ask_llm(question):
    return llm.invoke(question)

with gr.Blocks() as demo:
    gr.Markdown("# AI Assistant")
    question = gr.Textbox(label="Question", lines=5)
    ask_button = gr.Button("Ask", variant="primary")
    answer = gr.Markdown()

    ask_button.click(fn=ask_llm, inputs=question, outputs=answer)

demo.launch()
```

### Typical RAG App

```
User → Gradio UI → Question → Retrieval → Relevant Documents → LLM → Answer → Gradio UI
```

```python
def ask_rag(question):
    documents = retriever.invoke(question)
    context = "\n".join(doc.page_content for doc in documents)
    prompt = f"Answer using the following context:\n{context}\nQuestion:\n{question}"
    return llm.invoke(prompt)

with gr.Blocks() as demo:
    question = gr.Textbox(label="Ask a question")
    button = gr.Button("Ask")
    answer = gr.Markdown()

    button.click(fn=ask_rag, inputs=question, outputs=answer)

demo.launch()
```

### File + RAG Pipeline

```
Upload PDF → Extract text → Chunk documents → Create embeddings →
Vector DB → Question → Retrieve chunks → LLM → Answer
```

```python
file = gr.File(label="Upload PDF")
question = gr.Textbox(label="Question")
upload_button = gr.Button("Process")
ask_button = gr.Button("Ask")
answer = gr.Markdown()
```

### Image / Audio Models

```python
# Image classification
demo = gr.Interface(fn=classify, inputs=gr.Image(), outputs=gr.Label())

# Image-to-text
demo = gr.Interface(fn=describe_image, inputs=gr.Image(), outputs=gr.Textbox())

# Audio-to-text
demo = gr.Interface(fn=transcribe, inputs=gr.Audio(), outputs=gr.Textbox())
```

### Keeping Logic Separate From UI

Keep AI/business logic separate from Gradio UI wiring for maintainability:

```python
def ask_ai(question):
    # AI logic lives here
    return response

button.click(fn=ask_ai, inputs=question, outputs=answer)
```

```
Python Application
├── AI / ML Logic
├── Data Processing
├── RAG / Retrieval
├── Business Logic
└── Gradio UI
    ├── Inputs
    ├── Buttons
    ├── Outputs
    └── Events
```

---

## 19. Complete Examples

### Small Application

```python
import gradio as gr

def greet(name, age):
    return f"Hello {name}! You are {age} years old."

with gr.Blocks(title="Greeting App", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Greeting Application")
    with gr.Row():
        name = gr.Textbox(label="Name", placeholder="Enter your name")
        age = gr.Number(label="Age", value=25)
    button = gr.Button("Greet", variant="primary")
    output = gr.Textbox(label="Result")

    button.click(fn=greet, inputs=[name, age], outputs=output)

demo.launch()
```

### Simple Chatbot

```python
import gradio as gr

def chat(message, history):
    return f"You asked: {message}"

demo = gr.ChatInterface(fn=chat, title="My AI Assistant", description="Ask a question.")
demo.launch()
```

### More Realistic Chatbot

```python
import gradio as gr

def chat(message, history):
    response = llm.invoke(message)  # call LLM here
    return response

with gr.Blocks() as demo:
    gr.Markdown("# AI Assistant")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Ask something...")
    send = gr.Button("Send")

    send.click(fn=chat, inputs=[message, chatbot], outputs=chatbot)
    message.submit(fn=chat, inputs=[message, chatbot], outputs=chatbot)

demo.launch()
```

---

## 20. Quick Reference

```python
# Basic app skeleton
with gr.Blocks() as demo:
    ...
demo.launch()

# Input / output
gr.Textbox()

# Button
gr.Button("Submit")

# Event
button.click(fn=function, inputs=input, outputs=output)

# Multiple inputs / outputs
inputs=[input1, input2]
outputs=[output1, output2]

# Chatbot
gr.Chatbot()
gr.ChatInterface(fn=chat)

# Hidden state
gr.State(initial_value)

# File / Image
gr.File()
gr.Image()

# Layout
with gr.Row():
    ...
with gr.Column():
    ...

# Markdown
gr.Markdown("# Hello")

# Public demo link
demo.launch(share=True)
```

**The one snippet to memorize:**

```python
import gradio as gr

def process(user_input):
    return f"You entered: {user_input}"

with gr.Blocks() as demo:
    input_box = gr.Textbox(label="Input")
    button = gr.Button("Submit")
    output_box = gr.Textbox(label="Output")

    button.click(fn=process, inputs=input_box, outputs=output_box)

demo.launch()
```

If you understand this pattern, the rest of Gradio is mostly learning additional components, layouts, events, and state-management options.

---

## 21. Learning Priority

### 🔥 Must Know

Covers most everyday usage:

`gr.Blocks` · `gr.Interface` · `gr.ChatInterface` · `gr.Textbox` · `gr.Button` · `gr.Markdown` · `gr.Row` · `gr.Column` · `gr.Chatbot` · `gr.File` · `gr.Image` · `gr.Dropdown` · `gr.Slider` · `gr.State` · `.click()` · `.submit()` · `.change()` · `.input()` · `.upload()` · `demo.launch()`

### 🟢 Should Know

`gr.Number` · `gr.Radio` · `gr.Checkbox` · `gr.CheckboxGroup` · `gr.Dataframe` · `gr.JSON` · `gr.Audio` · `gr.Video` · `gr.Accordion` · `gr.Tab` · `gr.Examples` · `gr.Progress` · `demo.queue()`

### 🟡 Learn When Needed

Custom CSS · Custom JavaScript · Advanced API configuration · Advanced component updates · Authentication · Custom themes · Streaming · Advanced state management · Concurrency · Advanced event chaining

---

## 22. Mental Model

Five things to keep in mind when building with Gradio:

1. **Components** — what does the user interact with? (`gr.Textbox()`, `gr.Button()`, `gr.Image()`, `gr.File()`, `gr.Chatbot()`)
2. **Layout** — how are components arranged? (`gr.Row()`, `gr.Column()`, `gr.Tab()`, `gr.Accordion()`)
3. **Functions** — what should happen? (`def process(input): return output`)
4. **Events** — when should it happen? (`.click()`, `.submit()`, `.change()`)
5. **State** — what should be remembered? (`gr.State(...)`)

```
GRADIO
├── COMPONENTS ─── Input / Button / Output
├── LAYOUT ──────── Row / Column / Tabs / Accordion
├── EVENTS ──────── .click() / .submit() / .change() / .input()
│                         │
│                         ▼
│                 PYTHON FUNCTION
│                    │    │    │
│                   LLM  RAG   ML
│                    │    │    │
│                    └────┼────┘
│                         ▼
│                      OUTPUT
└─────────────────────────▼
                      GRADIO UI
```

**One-sentence summary:** Gradio lets you connect Python functions, AI models, and LLM/RAG pipelines to web UI components using a small amount of Python code.