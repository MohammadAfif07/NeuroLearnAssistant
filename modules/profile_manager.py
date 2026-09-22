# modules/profile_manager.py

import json
import os

PROFILE_PATH = "profiles/user_profile.json"

def load_profile():
    if not os.path.exists(PROFILE_PATH):
        # Return default profile if not exists
        return {
            "username": "User",
            "style": "default",     # visual, audio, text
            "pace": "normal",       # slow, normal, fast
            "tts": True             # Text to speech
        }
    with open(PROFILE_PATH, 'r') as f:
        return json.load(f)

def save_profile(profile):
    os.makedirs(os.path.dirname(PROFILE_PATH), exist_ok=True)
    with open(PROFILE_PATH, 'w') as f:
        json.dump(profile, f, indent=4)