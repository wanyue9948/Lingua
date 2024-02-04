from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a native translator."},
    {"role": "user", "content": "Translate I love you in finnish."}
  ]
)

response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input= "今天我很高兴也很疲惫",
)

response.stream_to_file("output.mp3")

print(completion.choices[0].message.content)