import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def gpt_explain(concept, style):
    style_prompt = {
        "visual": f"Explain '{concept}' using visual metaphors or examples. Use diagrams or describe visuals.",
        "audio": f"Explain '{concept}' in a conversational and spoken tone, like a teacher speaking out loud.",
        "text": f"Explain '{concept}' clearly and simply using plain text."
    }

    prompt = style_prompt.get(style, style_prompt["text"])

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful tutor for neurodivergent students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error generating explanation: {e}"