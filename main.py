# main.py

import os
from dotenv import load_dotenv

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

# Optional: verify keys
print("HF_TOKEN:", os.getenv("HF_TOKEN"))
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))

# -------------------------
# Import project modules
# -------------------------
from modules.profile_manager import load_profile, save_profile
from modules.voice_engine import speak
from modules.adaptive_explainer import explain_concept
from rich import print

# -------------------------
# Main Program
# -------------------------
def main():
    profile = load_profile()

    # Adjust speech rate
    rate = {
        "slow": 120,
        "normal": 150,
        "fast": 180
    }.get(profile.get("pace", "normal"), 150)

    # Personalized greeting
    greeting = f"Welcome back, {profile['username']}! Let's begin your learning session."
    print(f"\n[bold cyan]{greeting}[/bold cyan]")

    if profile.get("tts", True):
        speak(greeting, rate)

    # Ask if user wants to change learning style
    change = input("\nDo you want to change your learning style? (yes/no): ").lower()
    if change == "yes":
        print("\n[bold yellow]How do you learn best?[/bold yellow]")
        print("1. 👁️ Visual (Images, diagrams)")
        print("2. 🎧 Audio (Listening)")
        print("3. 📖 Text (Reading/writing)")

        choice = input("Enter choice [1/2/3]: ").strip()

        if choice == "1":
            profile["style"] = "visual"
        elif choice == "2":
            profile["style"] = "audio"
        elif choice == "3":
            profile["style"] = "text"
        else:
            print("Invalid input. Keeping previous setting.")

        save_profile(profile)
        print(f"[green]Updated learning style to:[/green] {profile['style']}")

    # Ask user what they want to learn
    concept = input("\nEnter a concept you want to learn (e.g., gravity, photosynthesis, democracy): ").strip()

    # Explain the concept based on user profile
    explain_concept(
        concept=concept,
        style=profile.get("style", "text"),
        rate=rate,
        tts=profile.get("tts", True)
    )

    # Confirm current learning mode
    print("\n[green]🧠 Current Learning Mode:[/green]", profile.get("style", "default"))

if __name__ == "__main__":
    main()