import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import traceback

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize client with a chat-compatible model
client = InferenceClient(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    token=HF_TOKEN
)

def explain_concept(concept):
    messages = [
        {"role": "user", "content": f"Explain the concept of {concept} in a simple and clear way for students."}
    ]
    try:
        response = client.chat_completion(
            messages=messages,
            temperature=0.7,   # This is supported
            max_tokens=150     # ? Use max_tokens instead of max_new_tokens
        )
        return response.choices[0].message["content"].strip()
    except Exception:
        return f"? Exception occurred:\n{traceback.format_exc()}"

# Interactive shell
if __name__ == "__main__":
    while True:
        concept = input("?? Enter a concept (or 'exit'): ")
        if concept.lower() == "exit":
            break
        explanation = explain_concept(concept)
        print(f"\n?? Explanation:\n{explanation}\n")
