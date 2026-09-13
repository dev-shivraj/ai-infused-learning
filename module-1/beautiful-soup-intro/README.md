# BeautifulSoup — Practical Cheat Sheet

A practical [BeautifulSoup (bs4)](https://www.crummy.com/software/BeautifulSoup/) cheat sheet covering the 80–90% of syntax commonly used for HTML parsing and web scraping.

## Table of Contents

1. [What is BeautifulSoup?](#1-what-is-beautifulsoup)
2. [Installation](#2-installation)
3. [Creating a Soup Object](#3-creating-a-soup-object)
4. [Fetching Pages with Requests](#4-fetching-pages-with-requests)
5. [Extracting Text](#5-extracting-text)
6. [Finding Elements — `find()` / `find_all()`](#6-finding-elements--find--find_all)
7. [Working with Attributes](#7-working-with-attributes)
8. [Links & Images](#8-links--images)
9. [CSS Selectors — `select()` / `select_one()`](#9-css-selectors--select--select_one)
10. [Navigating the Tree](#10-navigating-the-tree)
11. [Cleaning & Modifying HTML](#11-cleaning--modifying-html)
12. [Regex & Lambda Filters](#12-regex--lambda-filters)
13. [Extracting Structured Data](#13-extracting-structured-data)
14. [Robust / Safe Scraping](#14-robust--safe-scraping)
15. [Requests Essentials](#15-requests-essentials)
16. [URLs & Pagination](#16-urls--pagination)
17. [Practical Templates](#17-practical-templates)
18. [BeautifulSoup + AI/RAG/Gradio](#18-beautifulsoup--airaggradio)
19. [Common Mistakes](#19-common-mistakes)
20. [BeautifulSoup vs. Other Tools](#20-beautifulsoup-vs-other-tools)
21. [Full Method & Selector Cheat Sheet](#21-full-method--selector-cheat-sheet)
22. [Recommended Workflow](#22-recommended-workflow)
23. [Learning Priority](#23-learning-priority)
24. [Mental Model](#24-mental-model)

---

## 1. What is BeautifulSoup?

BeautifulSoup is a Python library for parsing HTML/XML documents, making it easy to:

- Find HTML elements
- Extract text, links, and attributes
- Navigate the HTML tree (parents, children, siblings)
- Search using CSS selectors
- Extract tables and forms
- Clean scraped HTML

**Typical web-scraping flow:**

```
Website → requests → HTML → BeautifulSoup → Parse HTML
→ Find required elements → Extract data
```

> `requests` downloads the webpage. `BeautifulSoup` parses and searches the HTML.

---

## 2. Installation

```bash
pip install beautifulsoup4
pip install requests beautifulsoup4   # usually installed together
```

```python
from bs4 import BeautifulSoup
import requests
```

---

## 3. Creating a Soup Object

### Sample HTML

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Website</title>
</head>
<body>
    <h1>Hello World</h1>
    <p class="description">This is my website.</p>
    <a href="https://example.com">Visit Website</a>
</body>
</html>
```

### Parse it

```python
html = """
<html>
    <body>
        <h1>Hello World</h1>
    </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")
```

The second argument specifies the **parser**.

### Common Parsers

| Parser | Use case |
|---|---|
| `"html.parser"` | Default, built-in, fine for most scraping |
| `"lxml"` | Faster, needs `lxml` installed |
| `"xml"` | For parsing XML documents |

```python
BeautifulSoup(html, "html.parser")
BeautifulSoup(html, "lxml")
BeautifulSoup(xml, "xml")
```

For most basic scraping, `"html.parser"` is enough.

### Parsing an HTML Fragment

You don't need a full page:

```python
html = """
<div class="product">
    <h2>iPhone</h2>
</div>
"""
soup = BeautifulSoup(html, "html.parser")
```

---

## 4. Fetching Pages with Requests

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
```

### Checking the Response

```python
response = requests.get(url)
print(response.status_code)
```

| Code | Meaning |
|---|---|
| 200 | Success |
| 301 | Redirect |
| 302 | Temporary redirect |
| 403 | Forbidden |
| 404 | Not found |
| 500 | Server error |

Raise an exception automatically on failure:

```python
response.raise_for_status()
```

---

## 5. Extracting Text

```python
soup.title                          # <title>My Website</title>
soup.title.text                     # "My Website"
soup.title.get_text()               # "My Website"
soup.get_text(strip=True)           # whole-page text, whitespace trimmed
```

`get_text(strip=True)` is very useful when extracting page content.

**Join fragments with a separator + strip:**

```python
text = element.get_text(" ", strip=True)
```

**Clean, whitespace-free strings only:**

```python
for text in element.stripped_strings:
    print(text)

for text in soup.strings:
    print(text)
```

---

## 6. Finding Elements — `find()` / `find_all()`

| Method | Returns |
|---|---|
| `soup.find("p")` | First matching element |
| `soup.find_all("p")` | All matching elements (list-like) |

```python
heading = soup.find("h1")
print(heading)          # <h1>Hello World</h1>

paragraphs = soup.find_all("p")
for p in paragraphs:
    print(p.text)
```

### Find by Class

```python
product = soup.find("div", class_="product")
products = soup.find_all("div", class_="product")
```

> `class` is a reserved Python keyword, so BeautifulSoup uses `class_` instead.

### Find by ID

```python
element = soup.find(id="main-content")
element = soup.find("div", id="main-content")
```

### Find by Attribute(s)

```python
input_box = soup.find("input", type="text", name="username")

# Or with an attrs dict:
element = soup.find("input", attrs={"type": "text", "name": "username"})

link = soup.find("a", href="/products")
```

### Find by Multiple Tags

```python
elements = soup.find_all(["h1", "h2", "h3"])   # useful for headings
```

### Limit Results

```python
elements = soup.find_all("a", limit=5)   # first 5 matches
elements = soup.find_all("a")[:5]        # equivalent alternative
```

### Search Within a Specific Element

```python
container = soup.find("div", class_="products")
products = container.find_all("div", class_="product")
```

Narrowing the search this way is often cleaner and faster than searching the whole page.

---

## 7. Working with Attributes

```python
element.get("attribute")        # safe — returns None if missing
element["attribute"]            # raises an error if missing
```

Prefer `.get()` when scraping unpredictable HTML:

```python
if link.get("href"):
    print(link["href"])
```

### Check / Get / Set / Remove

```python
element.has_attr("href")             # check existence
attributes = element.attrs           # dict of all attributes
element["data-id"] = "123"           # add an attribute
del element["data-id"]               # remove an attribute
```

### Classes

```python
classes = element.get("class")       # e.g. ["product", "featured"]

if "product" in element.get("class", []):
    print("Product found")
```

---

## 8. Links & Images

```python
links = soup.find_all("a")
for link in links:
    text = link.get_text(strip=True)
    href = link.get("href")
    print(text, href)

images = soup.find_all("img")
for image in images:
    src = image.get("src")
    alt = image.get("alt")
    print(src, alt)
```

---

## 9. CSS Selectors — `select()` / `select_one()`

| Method | Returns |
|---|---|
| `soup.select("p")` | All matches (like `find_all`) |
| `soup.select_one("p")` | First match (like `find`) |

```python
soup.select("p")              # all <p> elements
soup.select_one("h1")         # first <h1> element
```

### Selector Syntax

```python
soup.select(".product")               # class
soup.select("#main-content")          # ID
soup.select("div.product")            # tag + class
soup.select("div#main-content")       # tag + ID
soup.select("div.product h2")         # nested (any descendant)
soup.select("div.product > h2")       # direct child only
soup.select('a[href]')                # attribute exists
soup.select('a[href^="https"]')       # attribute starts with
soup.select('a[href*="example"]')     # attribute contains
soup.select('a[href$=".pdf"]')        # attribute ends with
soup.select("div.product.featured")   # multiple classes
```

**Nested vs. direct child:**

```
div.product h2    → any descendant <h2>
div.product > h2  → direct child <h2> only
```

---

## 10. Navigating the Tree

BeautifulSoup represents HTML as a tree:

```
html
├── head
│    └── title
└── body
     ├── h1
     ├── p
     └── a
```

```python
heading = soup.find("h2")

heading.parent                  # immediate parent
for p in heading.parents: ...   # all ancestors

element.children                # direct children (iterator)
element.descendants              # all nested elements
element.contents                 # direct children as a list
element.contents[0]              # first child

element.next_sibling
element.previous_sibling         # ⚠️ whitespace/newlines can appear as siblings

element.next_element
element.previous_element

element.name                     # tag name, e.g. "h1"
```

| Concept | Scope |
|---|---|
| `children` | Direct children only |
| `descendants` | All nested elements |

---

## 11. Cleaning & Modifying HTML

```python
print(element)                 # raw HTML
print(element.prettify())      # formatted HTML
print(soup.prettify())         # formatted full document — great for debugging
```

### Removing Elements

| Method | Effect |
|---|---|
| `element.decompose()` | Remove **and destroy** the tag |
| `element.extract()` | Remove **and return** the tag |
| `element.unwrap()` | Remove the tag but **keep its contents** |
| `element.replace_with(...)` | Replace the tag with new content |

```python
for script in soup.find_all("script"):
    script.decompose()

removed = soup.find("script").extract()

bold = soup.find("b")
bold.unwrap()                       # <p>Hello <b>World</b></p> → <p>Hello World</p>

element.replace_with("New content")
```

### Editing Content

```python
element.string = "New text"
link["href"] = "new.html"
```

### Stripping Script/Style Before Extracting Text

```python
for element in soup(["script", "style"]):
    element.decompose()

text = soup.get_text(" ", strip=True)
```

Very useful when preparing webpage content for LLM/RAG pipelines.

---

## 12. Regex & Lambda Filters

### Search by Exact or Partial Text

```python
import re

soup.find(string="Hello World")                       # exact match
soup.find(string=re.compile("Hello"))                  # contains "Hello"
soup.find_all("a", href=re.compile("^https"))           # href starts with https
soup.find_all(string=re.compile("Python"))               # any text containing "Python"
```

### Lambda Filtering

For cases normal selectors can't handle:

```python
elements = soup.find_all(lambda tag: tag.name == "div")

elements = soup.find_all(
    lambda tag: tag.name == "div" and tag.get("class")
)
```

---

## 13. Extracting Structured Data

### Lists

```python
items = soup.find_all("li")
for item in items:
    print(item.get_text(strip=True))
```

### Tables

```python
table = soup.find("table")
rows = table.find_all("tr")

for row in table.find_all("tr"):
    cells = row.find_all(["th", "td"])
    values = [cell.get_text(strip=True) for cell in cells]
    print(values)
```

Collect into a list:

```python
data = []
for row in rows:
    cells = row.find_all(["th", "td"])
    data.append([cell.get_text(strip=True) for cell in cells])
```

### Forms

```python
form = soup.find("form")
inputs = form.find_all("input")

for input_tag in inputs:
    name = input_tag.get("name")
    value = input_tag.get("value")
    input_type = input_tag.get("type")
    print(name, value, input_type)
```

### Meta Tags

```python
meta = soup.find("meta", attrs={"name": "description"})
description = meta.get("content")
```

### Repeated Cards (e.g. Products)

```html
<div class="product">
    <h2>iPhone</h2>
    <span class="price">$999</span>
</div>
<div class="product">
    <h2>MacBook</h2>
    <span class="price">$1999</span>
</div>
```

```python
products = soup.find_all("div", class_="product")

for product in products:
    name = product.find("h2")
    price = product.find("span", class_="price")
    print(name.get_text(strip=True), price.get_text(strip=True))
```

**Into dictionaries:**

```python
products = []
for product in soup.find_all("div", class_="product"):
    name = product.find("h2")
    price = product.find("span", class_="price")
    products.append({
        "name": name.get_text(strip=True),
        "price": price.get_text(strip=True)
    })
```

Result:

```python
[
    {"name": "iPhone", "price": "$999"},
    {"name": "MacBook", "price": "$1999"}
]
```

### With Pandas (for tables)

```python
import pandas as pd
tables = pd.read_html(response.text)
```

Not BeautifulSoup itself, but useful for structured HTML tables.

---

## 14. Robust / Safe Scraping

This matters a lot in real-world scraping — pages are inconsistent.

**Bad (crashes if `<h2>` is missing):**

```python
title = product.find("h2").text
```

**Safe:**

```python
title_element = product.find("h2")
title = title_element.get_text(strip=True) if title_element else None
```

Same idea for attributes:

```python
href = link.get("href")     # not link["href"]
if href:
    print(href)
```

Check existence before acting:

```python
element = soup.find("div", class_="product")
if element:
    print("Found")
else:
    print("Not found")
```

---

## 15. Requests Essentials

### Headers

Some sites behave differently depending on request headers.

```python
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
```

> Always respect a website's terms of service, `robots.txt`, and applicable laws.

### Timeout

```python
response = requests.get(url, timeout=10)
```

### Combined Production-ish Pattern

```python
response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
```

### Sessions

For multiple requests that should share cookies/connection settings:

```python
session = requests.Session()
response = session.get(url, timeout=10)
```

---

## 16. URLs & Pagination

### Multiple Pages

```python
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3"
]

for url in urls:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract data
```

### Pagination by Page Number

```python
for page in range(1, 6):
    url = f"https://example.com?page={page}"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.select(".product")
    for product in products:
        ...
```

### Absolute vs. Relative URLs

```python
from urllib.parse import urljoin

absolute_url = urljoin("https://example.com", "/products")
# → https://example.com/products
```

**Resolving every link on a page:**

```python
from urllib.parse import urljoin

base_url = "https://example.com"
for link in soup.find_all("a"):
    href = link.get("href")
    if not href:
        continue
    print(urljoin(base_url, href))
```

---

## 17. Practical Templates

### General-Purpose Scraping Template

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
products = soup.select(".product")

for product in products:
    name_element = product.select_one(".name")
    price_element = product.select_one(".price")

    name = name_element.get_text(strip=True) if name_element else None
    price = price_element.get_text(strip=True) if price_element else None
    print(name, price)
```

### Article / Main-Content Extraction

```python
article = soup.find("article")

if article:
    for element in article(["script", "style"]):
        element.decompose()
    text = article.get_text(" ", strip=True)
    print(text)
```

### "Visible-ish" Text Extraction

```python
for element in soup(["script", "style", "noscript"]):
    element.decompose()

text = soup.get_text(" ", strip=True)
```

> BeautifulSoup doesn't know what's truly *visible* in a browser — this is simply a useful HTML-cleaning technique.

---

## 18. BeautifulSoup + AI/RAG/Gradio

### Typical RAG Ingestion Pipeline

```
URL → requests → HTML → BeautifulSoup
→ Remove script/style/navigation → Extract useful text
→ Clean text → Chunk text → Embeddings → Vector Database → RAG → LLM
```

```python
response = requests.get(url, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for element in soup(["script", "style", "nav", "footer"]):
    element.decompose()

text = soup.get_text(" ", strip=True)
# → pass `text` into your document-processing pipeline
```

### Wiring It Into a Gradio App

```
Gradio → User enters URL → requests → HTML page → BeautifulSoup
→ Extract text → LLM / RAG pipeline → Response → Gradio
```

```python
def scrape_url(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for element in soup(["script", "style", "nav", "footer"]):
        element.decompose()
    return soup.get_text(" ", strip=True)
```

Connect `scrape_url()` to a Gradio textbox/button.

---

## 19. Common Mistakes

| Mistake | Wrong | Right |
|---|---|---|
| Forgetting to extract text | `print(element)` (prints HTML) | `print(element.get_text(strip=True))` |
| Assuming an element exists | `product.find("span").text` | Check for `None` first (see [§14](#14-robust--safe-scraping)) |
| Using `class` instead of `class_` | `soup.find("div", class="product")` | `soup.find("div", class_="product")` |
| Expecting JS to run | Scraping a JS-rendered page directly | Use Playwright/Selenium first, then parse the rendered HTML |

BeautifulSoup parses HTML — it does **not** behave like a browser and does **not** execute JavaScript.

---

## 20. BeautifulSoup vs. Other Tools

### `requests` vs. `BeautifulSoup`

```
requests       → downloads the HTTP response
BeautifulSoup  → parses the HTML
```

```python
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
```

### BeautifulSoup vs. Selenium/Playwright

| | Best for |
|---|---|
| **BeautifulSoup** | Parsing HTML, static pages, extracting/cleaning data |
| **Selenium / Playwright** | JS-rendered content, clicking/interacting, login flows, dynamic pages |

**Static site:**

```
requests → BeautifulSoup
```

**Dynamic site:**

```
Playwright/Selenium → Rendered HTML → BeautifulSoup → Extract data
```

---

## 21. Full Method & Selector Cheat Sheet

### Core Methods

```python
soup.find()
soup.find_all()
soup.select()
soup.select_one()

element.get_text(strip=True)
element.get()
element["attribute"]

element.name
element.attrs

element.find()
element.find_all()
element.select()
element.select_one()

element.parent
element.children
element.descendants

element.decompose()
element.extract()
element.unwrap()
element.replace_with()

soup.prettify()
```

### `find()` Patterns

```python
soup.find("div")
soup.find("div", class_="product")
soup.find("div", id="main")
soup.find("a", href="/products")
soup.find("input", attrs={"type": "text"})
soup.find(string="Hello")
```

### `find_all()` Patterns

```python
soup.find_all("a")
soup.find_all("p")
soup.find_all("div", class_="product")
soup.find_all(["h1", "h2", "h3"])
soup.find_all("a", limit=10)
soup.find_all(string=re.compile("Python"))
```

### CSS Selector Patterns

```python
soup.select("p")
soup.select(".product")
soup.select("#main")
soup.select("div.product")
soup.select("div.product h2")
soup.select("div.product > h2")
soup.select("a[href]")
soup.select('a[href^="https"]')
soup.select('a[href*="example"]')
soup.select('a[href$=".pdf"]')
soup.select(".product.featured")
```

### Extraction Patterns

```python
element.get_text(strip=True)   # text
element.get("href")            # generic attribute
image.get("src")               # image source
link.get("href")               # link URL
element.get("class")           # class list
element.name                   # tag name
```

---

## 22. Recommended Workflow

When scraping a new website, follow this process:

```python
# 1. Download HTML
response = requests.get(url, timeout=10)

# 2. Check the response
response.raise_for_status()

# 3. Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# 4. Inspect HTML
print(soup.prettify())

# 5. Find the container
container = soup.select_one(".products")

# 6. Find repeated elements
products = container.select(".product")

# 7. Extract data
for product in products:
    name = product.select_one(".name")
    price = product.select_one(".price")

    # 8. Clean text
    name = name.get_text(strip=True) if name else None

    # 9. Store structured data
    data.append({"name": name, "price": price})
```

### The Pattern You'll Write Repeatedly

```python
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

items = soup.select(".item")
results = []

for item in items:
    title = item.select_one(".title")
    link = item.select_one("a")
    results.append({
        "title": title.get_text(strip=True) if title else None,
        "url": link.get("href") if link else None
    })
```

---

## 23. Learning Priority

### 🔥 Level 1 — Must Know

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

soup.find()
soup.find_all()
soup.select()
soup.select_one()

element.get_text(strip=True)
element.get()
element["attribute"]

element.name
element.attrs
```

### 🟢 Level 2 — Very Useful

```python
element.find()
element.find_all()
element.select()
element.select_one()

element.parent
element.children
element.descendants

element.get("class")

soup.prettify()

element.decompose()
element.extract()
element.unwrap()
```

### 🟡 Level 3 — Learn When Needed

```python
element.next_sibling
element.previous_sibling
element.next_element
element.previous_element

soup.strings
element.stripped_strings

soup.find(string=...)
soup.find_all(string=...)

# lambda filters
# regular expressions
# custom parsing
# HTML modification
# XML parsing
```

---

## 24. Mental Model

BeautifulSoup revolves around five core operations:

| # | Step | Key methods |
|---|---|---|
| 1 | **Parse** | `BeautifulSoup(html, "html.parser")` |
| 2 | **Find** | `find()`, `find_all()` |
| 3 | **Select** | `select()`, `select_one()` |
| 4 | **Extract** | `get_text()`, `get()`, `.attrs` |
| 5 | **Navigate / Clean** | `.parent`, `.children`, `.descendants`, `decompose()`, `extract()`, `unwrap()` |

```
HTML
  │
  ▼
BeautifulSoup
  │
  ├── FIND ──────── find() / find_all()
  ├── SELECT ─────── select() / select_one()
  └── NAVIGATE ───── parent / children / siblings
  │
  ▼
EXTRACT ── text / href / src
  │
  ▼
STRUCTURED DATA
  │
  ▼
AI / RAG / Database
```

**One-sentence summary:** BeautifulSoup = Parse HTML → Find elements → Select elements → Extract data → Clean data.