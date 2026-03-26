import sys
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Check both keys are present
missing = []
if not os.environ.get("GROQ_API_KEY"):
    missing.append("GROQ_API_KEY  → get free key at https://console.groq.com")
if not os.environ.get("SERPER_API_KEY"):
    missing.append("SERPER_API_KEY → get free key at https://serper.dev")

if missing:
    print("\n  Missing API keys in your .env file:")
    for m in missing:
        print(f"    - {m}")
    print("\n  Open .env and paste your keys, then run again.\n")
    sys.exit(1)

# Create outputs/ folder if it doesn't exist
Path("outputs").mkdir(exist_ok=True)

# Get topic from CLI arg or interactive prompt
if len(sys.argv) > 1:
    topic = " ".join(sys.argv[1:])
else:
    print("\n" + "─" * 55)
    print("  CrewAI Study Assistant")
    print("─" * 55)
    topic = input("\n  What do you want to learn today?\n  → ").strip()
    if not topic:
        topic = "how neural networks learn"
        print(f"  (Using default: {topic})")

print(f"\n{'─'*55}")
print(f"  Topic  : {topic}")
print(f"  Status : Starting 3-agent crew...")
print(f"{'─'*55}\n")

from crew import study_crew

result = study_crew.kickoff(inputs={"topic": topic})

print(f"\n{'─'*55}")
print("  Done! Your learning materials are ready:\n")
print("  outputs/01_research.md    < web research report")
print("  outputs/02_explanation.md < beginner explanation")
print("  outputs/03_quiz.md        < 5-question quiz")
print(f"{'─'*55}\n")
