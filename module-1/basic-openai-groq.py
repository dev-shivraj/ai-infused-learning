import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

'''
response = client.chat.completions.create(
    # model="llama-3.3-70b-versatile",        # a free Llama model on Groq
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a funny joke teller."},
        {"role": "user",   "content": "Tell me a joke."},
    ],
)
'''

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
    ],
)

print(response.choices[0].message.content)