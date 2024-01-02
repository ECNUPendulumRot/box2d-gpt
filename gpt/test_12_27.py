import os

# setup the OPENAI key as a global variable
OPENAI_API_KEY = "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"

from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_API_KEY
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
