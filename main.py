import os
import time
from datetime import datetime
import ollama

# Load prompts
with open("prompts.txt", "r") as f:
    PROMPTS = f.read().split("\n\n\n")

# Load topics
with open("topics.txt", "r") as f:
    TOPICS = [line.strip() for line in f if line.strip()]

# Set model name (adjust to your installed local model)
MODEL = "llama3"

def run_chain(topic):
    current = PROMPTS[0].replace("{input}", topic)
    for i in range(5):
        print(f"[Stage {i+1}] Sending prompt...")
        response = ollama.chat(model=MODEL, messages=[
            { "role": "user", "content": current }
        ])
        current = PROMPTS[i+1].replace("what you just wrote", response["message"]["content"])
    return current

def save_output(topic, output):
    folder = "outputs"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{folder}/{topic.replace(' ', '_')}_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(output)
    print(f"✅ Saved: {filename}")

if __name__ == "__main__":
    for topic in TOPICS:
        print(f"\n=== Running ATLAS-MAKER for: {topic} ===\n")
        final_script = run_chain(topic)
        save_output(topic, final_script)
