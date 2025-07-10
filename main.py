import openai
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env and set API key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#Paths
promt_dir = Path("prompts")
result_dir = Path("results")
result_dir.mkdir(exist_ok=True)

for promt_file in promt_dir.glob("*.txt"):
    promt_text = promt_file.read_text(encoding="utf-8")
    
    print(f"Sending prompt: {promt_file.name}")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": promt_text}],
        temperature=0.3,
        max_tokens=1000
    )
    
    answer = response.choices[0].message.content.strip()
    
    result_file = result_dir / f"{promt_file.name}_RESULT.txt"
    result_file.write_text(answer, encoding="utf-8")
    
    print(f"Result saved to: {result_file}")
