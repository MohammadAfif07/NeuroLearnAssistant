# modules/visual_generator.py

import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import random
import io # <-- NEW IMPORT (Required for the fix)

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

try:
    image_client = InferenceClient(
        model="stabilityai/stable-diffusion-xl-base-1.0", 
        token=HF_TOKEN
    )
except Exception as e:
    print(f"⚠️ Could not initialize Image Client: {e}. Check token and diffusers install.")
    image_client = None

# --- Diverse Style Modifiers ---
VISUAL_STYLES = [
    "simple labeled schematic diagram, clear lines, educational graphic",
    "colorful, highly saturated cartoon illustration, friendly design",
    "black and white chalkboard sketch, hand-drawn look, detailed labels",
    "minimalist vector line art, flat colors, high contrast, clean background",
    "abstract infographic design, flow chart style, interconnected nodes"
]

def generate_visual(concept):
    """Generates a visually diverse educational image using Stable Diffusion."""
    if not image_client:
        print("❌ Image client not available. Skipping visual generation.")
        return False
        
    style_modifier = random.choice(VISUAL_STYLES)

    try:
        prompt = (
            f"An educational diagram of '{concept}'. The visual should be {style_modifier}. "
            f"The image must be simple, clear, and informative for a student."
        )
        print(f"\n🖼️ Generating visual (Style: {style_modifier.split(',')[0].strip()})...")
        
        # This calls the Inference API and may return a PIL Image or bytes
        generated_image = image_client.text_to_image(
            prompt, 
            negative_prompt="photorealistic, blurry, noisy, ugly, text, words",
            guidance_scale=8.0
        )
        
        filename = f"{concept.replace(' ', '_').lower()}_visual.png"
        
        # --- FIX FOR PIL.Image.Image OBJECTS ---
        if hasattr(generated_image, 'save'): # Check if it's a PIL Image object
            buffer = io.BytesIO()
            generated_image.save(buffer, format="PNG") # Save PIL Image to a byte buffer
            image_bytes = buffer.getvalue()
        else: # Assume it's already bytes 
            image_bytes = generated_image
        
        with open(filename, "wb") as f:
            f.write(image_bytes)
        # --- FIX ENDS HERE ---
            
        print(f"✅ Visual saved as: {filename}")

        # Auto-open logic
        if os.name == 'nt':
            os.system(f'start {filename}')
        else:
            os.system(f'xdg-open {filename}')
            
        return True
        
    except Exception as e:
        print(f"❌ Visual generation failed: {e}. Check Inference API access and model access.")
        return False