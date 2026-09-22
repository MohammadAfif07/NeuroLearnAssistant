# modules/adaptive_explainer.py (FINAL VERSION)

import os
from modules.voice_engine import speak
from huggingface_hub import InferenceClient
from modules.visual_generator import generate_visual 
from rich import print
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize Hugging Face client for text generation
client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=HF_TOKEN
)

def clean_ai_output(text: str) -> str:
    """
    Removes common AI/chat format tags (like [/ASSISTANT]) that crash rich.print.
    """
    unwanted_tags = [
        '[USER]', '[/USER]', '[INST]', '[/INST]', 
        '[BOT]', '[/BOT]', '<|im_start|>', '<|im_end|>', 
        '<user>', '</user>', '<assistant>', '</assistant>',
        '[/ASSISTANT]'
    ]
    
    cleaned_text = text
    for tag in unwanted_tags:
        cleaned_text = cleaned_text.replace(tag, '')
        
    return cleaned_text.strip()

def gpt_explain(prompt):
    """A unified wrapper for the AI text model that sanitizes the output."""
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        raw_explanation = response.choices[0].message.content.strip()
        
        # FIX: Apply cleaning here, before returning
        return clean_ai_output(raw_explanation) 
        
    except Exception as e:
        return f"⚠️ Error generating explanation: {str(e)}"

def explain_concept(concept, style="text", rate=150, tts=True):
    """Explains a concept based on learning style."""
    
    # 1. Define Prompt
    if style == "text":
        prompt = f"Explain the concept of '{concept}' in a clear, simple way for a student who prefers reading text."
    
    elif style == "audio":
        prompt = f"Explain the concept of '{concept}' in a warm, simple, and conversational tone, like a friendly podcast host, for an auditory learner."
    
    elif style == "visual":
        prompt = (
            f"Explain the concept of '{concept}' in a single paragraph, describing the core idea and its visual metaphors. "
            f"The output must be pure, clean text. "
            f"STRICTLY DO NOT USE: video script format, voiceover, camera directions, narrator tags, or [brackets]."
        )
    else: 
        prompt = f"Explain the concept of '{concept}' in a simple and clear way for a student."

    # 2. Generate Explanation
    explanation = gpt_explain(prompt)

    # 3. Print Output
    print(f"\n[bold green]Explanation for {concept}:[/bold green]\n{explanation}")

    # 4. Handle Visual/Audio Generation
    if style == "visual":
        generate_visual(concept) 
        
    if tts and style == "audio":
        speak(explanation, rate)