import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("HW1_PYTHONKEY"),)

completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content" : "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)

print(completion.choices[0].message)