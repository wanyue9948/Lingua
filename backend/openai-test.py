from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a native translator."},
    {"role": "user", "content": "Translate I love you in finnish."}
  ]
)

print(completion.choices[0].message.content)