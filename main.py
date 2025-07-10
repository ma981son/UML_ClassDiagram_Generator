import openai
import os
from dotenv import load_dotenv

# Load .env and set API key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Create chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Sag mir bitte kurz, was ein UML-Klassendiagramm ist."}
    ],
    temperature=0.3,
    max_tokens=200
)

# Print the response
print(response.choices[0].message.content)
