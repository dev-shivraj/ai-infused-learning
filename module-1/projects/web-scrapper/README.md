# 🔎 AI Website Summarizer

A simple AI-powered website summarizer built with **Python**, **Gradio**, **Requests**, **BeautifulSoup**, and an OpenAI-compatible LLM API via **Groq**.

The application accepts a website URL, downloads the page HTML, extracts meaningful text, sends that content to an LLM, and displays a short Markdown summary.

## Table of Contents

1. [What Does This Project Do?](#1-what-does-this-project-do)
2. [Architecture](#2-architecture)
3. [Application Components](#3-application-components)
4. [Technologies Used](#4-technologies-used)
5. [Environment Variables](#5-environment-variables)
6. [Installation](#6-installation)
7. [Running the Application](#7-running-the-application)
8. [`app.py` Explained](#8-apppy-explained)
9. [`scraper.py` Explained](#9-scraperpy-explained)
10. [`summarizer.py` Explained](#10-summarizerpy-explained)
11. [Complete Request Lifecycle](#11-complete-request-lifecycle)
12. [Python Concepts Used](#12-python-concepts-used)
13. [Web Concepts Used](#13-web-concepts-used)
14. [Why Split Into Three Files?](#14-why-split-into-three-files)
15. [Limitations](#15-limitations)
16. [Possible Future Improvements](#16-possible-future-improvements)
17. [Mental Model](#17-mental-model)
18. [Key Takeaways](#18-key-takeaways)

---

## 1. What Does This Project Do?

The application follows this pipeline:

```
User enters URL
      │
      ▼
    Gradio
      │
      ▼
  summarize()
      │
      ▼
 Fetch website (Requests + BeautifulSoup)
      │
      ▼
 Extract & clean text
      │
      ▼
 Send content to LLM
      │
      ▼
 Generate summary
      │
      ▼
 Display as Markdown
```

**Example:**

| Input | Output |
|---|---|
| `https://example.com` | `## Summary`<br>`This website provides information about...` |

---

## 2. Architecture

The application is split across three files, each with a single responsibility:

```
app.py  ──calls──▶  summarizer.py  ──calls──▶  scraper.py
                          ▲                         │
                          └────── website content ──┘
                          │
                          ▼
                     LLM Summary
                          │
                          ▼
                        app.py
                          │
                          ▼
                     Gradio UI
```

| File | Responsibility |
|---|---|
| `app.py` | Creates and launches the Gradio UI |
| `scraper.py` | Downloads and extracts website content |
| `summarizer.py` | Sends website content to the LLM and generates the summary |

---

## 3. Application Components

### `app.py` — User Interface

Uses **Gradio** and calls `summarize()` from `summarizer.py`.

```
User → Enter URL → Gradio → summarize(url) → Display summary
```

### `scraper.py` — Website Scraping

Uses **requests** and **BeautifulSoup**.

```
URL → HTTP GET → HTML response → BeautifulSoup
    → Remove unwanted elements → Extract text → Return website content
```

### `summarizer.py` — AI Summarization

Uses `os`, `python-dotenv`, the **OpenAI Python SDK**, and `fetch_website_contents()` from `scraper.py`.

```
URL → fetch_website_contents() → Website text → LLM API → Summary
```

---

## 4. Technologies Used

| Technology | Role |
|---|---|
| **Python** | Main programming language |
| **Gradio** | Web interface, no HTML/CSS/JS needed |
| **Requests** | Makes HTTP requests to websites |
| **BeautifulSoup** | Parses HTML and extracts useful text |
| **OpenAI Python SDK** | Client library for chat completion requests |
| **Groq** | Provides an OpenAI-compatible API endpoint and model infrastructure |
| **python-dotenv** | Loads environment variables from a `.env` file |

### Gradio

The core abstraction is `Input → Python Function → Output`. In this app:

```
Textbox → summarize() → Markdown
```

### Requests

```python
response = requests.get(url, headers=HEADERS, timeout=15)
```

Downloads the website's HTTP response.

### BeautifulSoup

```python
soup = BeautifulSoup(response.text, "html.parser")
```

Parses the HTML so it can be navigated and manipulated.

### OpenAI Python SDK + Groq

The app uses Groq's OpenAI-compatible endpoint:

```
https://api.groq.com/openai/v1
```

The OpenAI SDK acts as the Python API client, while Groq provides the endpoint and model infrastructure — the SDK doesn't require requests to go to OpenAI's own servers, since `base_url` determines where they're sent.

### python-dotenv

```python
load_dotenv()
os.getenv("GROQ_API_KEY")
```

---

## 5. Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
```

**Never hard-code API keys in source code.**

```python
# ❌ Avoid
client = OpenAI(api_key="your-secret-api-key")

# ✅ Prefer
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"))
```

Make sure `.env` is listed in `.gitignore`:

```
.env
```

---

## 6. Installation

```bash
pip install gradio requests beautifulsoup4 openai python-dotenv
```

Or via a `requirements.txt`:

```
gradio
requests
beautifulsoup4
openai
python-dotenv
```

```bash
pip install -r requirements.txt
```

---

## 7. Running the Application

After setting up the `.env` file, run:

```bash
python app.py
```

Gradio starts the application locally. Since the app calls `.launch(share=True)`, it can also generate a temporary public sharing URL.

---

## 8. `app.py` Explained

### Imports

```python
import gradio as gr
from summarizer import summarize
```

`gr` is the conventional alias for Gradio. `summarize` is the function implemented in `summarizer.py`.

### Creating the Interface

```python
gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="🔎 AI Website Summarizer",
)
```

```
Textbox → summarize() → Markdown
```

| Parameter | Meaning |
|---|---|
| `fn=summarize` | The function to run. **Pass the function itself — `summarize`, not `summarize()`** — calling it here would execute it immediately while building the interface, instead of on each input. |
| `inputs=gr.Textbox(...)` | Text field; its value becomes the argument to `summarize(url)`. |
| `outputs=gr.Markdown(...)` | Renders the returned string as Markdown, so the LLM can return headings, bullets, etc. |

### Launch

```python
demo.launch(share=True)
```

Starts the app; `share=True` can create a temporary public URL.

---

## 9. `scraper.py` Explained

### Imports

```python
import requests
from bs4 import BeautifulSoup
```

`requests` handles HTTP requests; `BeautifulSoup` parses HTML.

### HTTP Headers

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
```

Headers give the server extra context. The `User-Agent` makes the request look more like a browser, since some sites behave differently depending on it.

### `fetch_website_contents()`

The main scraping function:

```python
def fetch_website_contents(url):
    ...
```

It receives a URL and returns the website's content.

#### Handling a Missing URL Scheme

A user might type `example.com` instead of `https://example.com`. The code fills in the scheme:

```python
if not url.startswith(("http://", "https://")):
    url = "https://" + url
```

#### Sending the Request

```python
response = requests.get(url, headers=HEADERS, timeout=15)
```

| Argument | Meaning |
|---|---|
| `url` | The website to fetch |
| `headers` | Extra HTTP request metadata |
| `timeout` | Max time to wait for a response |

#### HTTP Error Handling

```python
response.raise_for_status()
```

Raises an exception for unsuccessful status codes:

| Code | Meaning |
|---|---|
| 200 | Success |
| 301 | Redirect |
| 403 | Forbidden |
| 404 | Not found |
| 500 | Server error |

#### Exception Handling

```python
except requests.exceptions.RequestException as e:
    return f"Could not fetch the website. Error: {e}"
```

`RequestException` covers common failure modes — connection errors, timeouts, invalid requests, HTTP errors — and the function returns a message instead of crashing.

#### Parsing HTML

```python
soup = BeautifulSoup(response.text, "html.parser")
```

```
Raw HTML → BeautifulSoup → Parsed HTML document
```

#### Extracting the Page Title

```python
title = soup.title.string if soup.title else "No title found"
```

For `<title>My Website</title>`, this returns `"My Website"`. This is Python's conditional (ternary) expression — `x if condition else y` — equivalent to:

```python
if soup.title:
    title = soup.title.string
else:
    title = "No title found"
```

#### Removing Unwanted Elements

```python
for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
    tag.decompose()
```

These elements are generally not useful for summarization — e.g. navigation menus or `<script>` blocks add noise without adding meaning for the LLM.

#### Extracting Text

```python
text = soup.get_text(separator="\n", strip=True)
```

| Argument | Effect |
|---|---|
| `separator="\n"` | Places newlines between extracted text sections |
| `strip=True` | Removes unnecessary whitespace |

#### Returning the Content

```python
return f"Title: {title}\n\nPage contents:\n{text}"
```

This string becomes the input passed to the LLM.

---

## 10. `summarizer.py` Explained

### Imports

```python
import os
from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_contents
```

| Import | Purpose |
|---|---|
| `os` | Access environment variables |
| `OpenAI` | Create the API client |
| `load_dotenv` | Load `.env` variables |
| `fetch_website_contents` | Fetch website content |

### Loading `.env`

```python
load_dotenv()
```

Loads variables like `GROQ_API_KEY=...` into the process environment, retrievable via `os.getenv("GROQ_API_KEY")`.

### Creating the API Client

```python
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
```

```
OpenAI Python SDK → API request → Groq OpenAI-compatible API → Selected model
```

The SDK doesn't necessarily send requests to OpenAI's own servers — `base_url` determines the destination.

### System Prompt

```python
system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""
```

This defines the model's behavior: analyze the content, write a short and friendly summary, ignore navigation menus, and respond in Markdown.

### `summarize()`

```python
def summarize(url):
    ...
```

The main application function, called directly by Gradio.

**Step 1 — Fetch the website:**

```python
website = fetch_website_contents(url)
```

Internally: `URL → requests.get() → HTML → BeautifulSoup → remove unwanted tags → extract text → return content`.

**Step 2 — Call the LLM:**

```python
response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Summarize this website:\n\n{website}"},
    ],
)
```

| Field | Purpose |
|---|---|
| `model` | Which model generates the summary |
| `system` message | Defines the model's behavior |
| `user` message | Contains the actual website content |

**Step 3 — Extract the generated text:**

```python
return response.choices[0].message.content
```

```
response → choices → first choice [0] → message → content
```

This is what's returned to Gradio.

---

## 11. Complete Request Lifecycle

Walking through what happens when a user enters `example.com`:

| Step | What happens |
|---|---|
| 1 | Gradio receives `"example.com"` |
| 2 | Gradio calls `summarize("example.com")` |
| 3 | `summarizer.py` calls `fetch_website_contents("example.com")` |
| 4 | `scraper.py` adds the scheme → `"https://example.com"` |
| 5 | Requests downloads the HTML |
| 6 | BeautifulSoup parses the HTML |
| 7 | Unwanted tags removed (`script`, `style`, `nav`, `footer`, `header`, `img`, `input`) |
| 8 | Text extracted via `soup.get_text(separator="\n", strip=True)` |
| 9 | Website content returned to `summarizer.py` |
| 10 | System prompt + website content sent to the LLM |
| 11 | LLM generates a Markdown summary |
| 12 | Summary returned to Gradio |
| 13 | Gradio renders the Markdown in the UI |

```
┌────────────────────────────────────┐
│ 🔎 AI Website Summarizer            │
│                                      │
│ Website URL                         │
│ ┌──────────────────────────────┐   │
│ │ https://example.com          │   │
│ └──────────────────────────────┘   │
│                                      │
│ Summary                             │
│                                      │
│ ## Summary                          │
│ The website provides...             │
└────────────────────────────────────┘
```

---

## 12. Python Concepts Used

| Concept | Example |
|---|---|
| Imports | `import requests`, `from bs4 import BeautifulSoup` |
| Functions | `def summarize(url): ...` |
| Function composition | `summarize()` calls `fetch_website_contents()` |
| Dictionaries | `HEADERS = {"User-Agent": "...", "Accept": "..."}` |
| Tuples | `("http://", "https://")` with `.startswith()` |
| Exception handling | `try: ... except requests.exceptions.RequestException as e: ...` |
| Conditional expression | `title = soup.title.string if soup.title else "No title found"` |
| Environment variables | `os.getenv("GROQ_API_KEY")` |
| f-strings | `f"Title: {title}\n\nPage contents:\n{text}"` |
| List iteration | `for tag in soup([...]): tag.decompose()` |

---

## 13. Web Concepts Used

The general pipeline behind most web scrapers:

```
URL → HTTP Request → HTTP Response → HTML
    → HTML Parser → DOM-like structure → Extract information
```

### Requests vs. BeautifulSoup

| | Role | Answers |
|---|---|---|
| **Requests** | Downloads the website | "How do I download the page?" |
| **BeautifulSoup** | Processes the downloaded HTML | "How do I understand and extract information from the HTML?" |

### Scraping vs. Summarization

These are kept as separate stages:

```
Scraping:       Website → HTML → Clean text
Summarization:  Clean text → LLM → Summary
```

Keeping them separate makes the application easier to understand and maintain.

---

## 14. Why Split Into Three Files?

**Without separation**, everything lives in one file:

```
app.py
├── Gradio
├── Requests
├── BeautifulSoup
├── API client
├── Prompt
└── Summarization
```

**With separation**, each file has one job:

```
app.py         → UI
scraper.py     → Website extraction
summarizer.py  → AI summarization
```

This makes the code easier to read, debug, test, modify, extend, and reuse.

---

## 15. Limitations

This scraper is intentionally simple — not every website will work perfectly.

### 1. JavaScript-Rendered Websites

```
Initial HTML → Very little content → JavaScript executes → Actual content appears
```

`requests` doesn't execute JavaScript like a real browser, so `requests` + `BeautifulSoup` may miss content that only appears after JS runs. A browser automation tool like Playwright or Selenium may be needed for those sites.

### 2. Robots & Website Policies

A production scraper should consider `robots.txt`, terms of service, rate limits, authentication requirements, copyright restrictions, and server load.

### 3. Anti-Bot Protection

CAPTCHAs, Cloudflare, bot detection, rate limiting, and authentication can all defeat a simple `requests`-based scraper.

### 4. Content Size

A large website can produce a huge amount of text. Sending all of it to an LLM directly can mean large API requests, higher token usage and cost, slower responses, and context-window problems. A production version could instead:

```
Website → Extract text → Clean text → Chunk text
       → Summarize chunks → Combine summaries → Final summary
```

---

## 16. Possible Future Improvements

| # | Improvement | Description |
|---|---|---|
| 1 | Better content extraction | Identify the main article/content area instead of grabbing all page text |
| 2 | URL validation | Validate URLs before making requests |
| 3 | Better error handling | Friendly messages for invalid URLs, timeouts, 403/404, DNS failures, empty pages |
| 4 | Text length limits | Cap the amount of content sent to the LLM |
| 5 | Chunking | Split large pages into chunks, summarize each, then combine |
| 6 | Summary length selection | Let the user choose Short / Medium / Detailed |
| 7 | Summary style | Let the user choose Professional / Simple / Technical / Bullet points / Executive summary |
| 8 | Multiple output formats | Summary, key points, important entities, action items, keywords |
| 9 | Browser-based scraping | Use Playwright to render JS-heavy pages before extracting content |

**Chunking concept:**

```
Large website → Chunk 1 / Chunk 2 / Chunk 3 → Individual summaries → Final summary
```

**Browser-based scraping concept:**

```
Gradio → Summarizer → Playwright → Browser → Rendered website → Extract content → LLM
```

---

## 17. Mental Model

```
┌───────────────────────┐
│        Gradio          │
│        app.py          │
│       UI Layer         │
└───────────┬─────────────┘
            │ URL
            ▼
┌───────────────────────┐
│     summarizer.py       │
│        AI Layer         │
└───────────┬─────────────┘
            │ URL
            ▼
┌───────────────────────┐
│      scraper.py         │
│    Requests + BS4       │
│    Scraping Layer       │
└───────────┬─────────────┘
            │ Website text
            ▼
┌───────────────────────┐
│     summarizer.py       │
│        LLM API          │
└───────────┬─────────────┘
            │ Summary
            ▼
┌───────────────────────┐
│        Gradio          │
│     Display result      │
└───────────────────────┘
```

---

## 18. Key Takeaways

1. Gradio creates a UI around a Python function.
2. Requests downloads website content over HTTP.
3. BeautifulSoup parses HTML and extracts useful information.
4. `response.text` contains the downloaded HTML.
5. `raise_for_status()` detects unsuccessful HTTP responses.
6. `try`/`except` handles request failures gracefully.
7. `decompose()` removes unwanted HTML elements.
8. `get_text()` extracts readable text from HTML.
9. `.env` keeps secrets outside source code.
10. `os.getenv()` reads environment variables.
11. The OpenAI SDK can be pointed at any OpenAI-compatible API endpoint.
12. System prompts define the behavior expected from the LLM.
13. User messages provide the actual content to process.
14. The LLM generates the summary.
15. Gradio displays the generated Markdown.

**The whole application, in one line:**

```
UI → Function → Scrape → Clean → LLM → Summary → UI
```

This is a broadly useful pattern for small AI applications:

```
User Interface → Business Logic → External Data → AI Processing → User Interface
```