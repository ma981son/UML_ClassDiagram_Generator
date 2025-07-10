from llm_clients import gpt4
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load .env
load_dotenv()

# Settings
models = [
    {"model": "gpt-4o", 
     "client_fn": gpt4.query_gpt4,
     "temperature": 0.3
    }
    ]

#Paths
promt_dir = Path("prompts")
responses_dir = Path("responses")
responses_dir.mkdir(exist_ok=True)
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

def get_unique_filename(base_path: Path, base_name: str, suffix=".txt") -> Path:
    i = 1
    while True:
        candidate = base_path / f"{base_name}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1

# Function to run the model with a given prompt and save the response
def run_model(model: str, client_fn, temperature: float, prompt_file: Path, out_base:Path):
    promt = prompt_file.read_text(encoding="utf-8")
    
    response = client_fn(model, promt, temperature)
    message = response.choices[0].message.content.strip()
    usage = response.usage
    model_version = response.model
    completion_id = response.id
    system_fingerprint = getattr(response, "system_fingerprint", "N/A")
    created_timestamp = datetime.fromtimestamp(response.created).strftime('%Y-%m-%d %H:%M:%S')
    
    temp_folder = f"temp-{str(temperature).replace('.', '_')}"
    model_folder = out_base / model / temp_folder
    model_folder.mkdir(parents=True,exist_ok=True)
    
    base_name = prompt_file.stem + "_RESPONSE"
    out_path = get_unique_filename(model_folder, base_name)
    out_path.write_text(
    f"# Model: {model}\n"
    f"# Model version: {model_version}\n"
    f"# Temperature: {temperature}\n"
    f"# Prompt file: {prompt_file.name}\n"
    f"# Completion ID: {completion_id}\n"
    f"# Timestamp (local): {created_timestamp}\n"
    f"# System fingerprint: {system_fingerprint}\n"
    f"# Prompt tokens: {usage.prompt_tokens}\n"
    f"# Completion tokens: {usage.completion_tokens}\n"
    f"# Total tokens: {usage.total_tokens}\n"
    + "-" * 60 + "\n"
    f"# RESPONSE:\n{message}"
)

for prompt_file in promt_dir.glob("*.txt"):
    for model in models:
        run_model(
            model=model["model"],
            client_fn=model["client_fn"],
            temperature=model["temperature"],
            prompt_file=prompt_file,
            out_base=responses_dir
        )


