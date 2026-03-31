import os
import json
from dotenv import load_dotenv
from groq import Groq

# -------------------------------
# Load environment variables
# -------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Make sure it exists in your .env file.")

client = Groq(api_key=api_key)

# -------------------------------
# Settings
# -------------------------------

IMPORTANT_FILE = "delta_important.json"
MAX_RECENT = 10

# -------------------------------
# Load important facts
# -------------------------------

if os.path.exists(IMPORTANT_FILE):
    with open(IMPORTANT_FILE, "r") as f:
        important_memory = json.load(f)
else:
    important_memory = []

# -------------------------------
# System prompt
# -------------------------------

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are Delta, an AI assistant specialized in probability and logic. "
        "Keep answers concise unless explaining a concept. "
        "Explain reasoning clearly and show calculations when useful."
    )
}

# -------------------------------
# Conversation memory
# -------------------------------

recent_messages = []

# -------------------------------
# Add important fact
# -------------------------------

def add_important_fact(fact):

    fact = fact.strip()

    if fact and fact not in important_memory:

        important_memory.append(fact)

        with open(IMPORTANT_FILE, "w") as f:
            json.dump(important_memory, f, indent=2)

# -------------------------------
# Chat function
# -------------------------------

def chat_with_delta(user_input):

    global recent_messages

    # -------------------------------
    # Automatic memory detection
    # -------------------------------

    keyword = "remember that"

    if user_input.lower().startswith(keyword):

        fact = user_input[len(keyword):].strip()

        add_important_fact(fact)

        return f"✅ Got it! I'll remember that: {fact}"

    # -------------------------------
    # Build messages
    # -------------------------------

    messages = [SYSTEM_PROMPT]

    # Inject important memory
    for fact in important_memory:

        messages.append({
            "role": "system",
            "content": f"Important information about the user: {fact}. Do not repeat unless relevant."
        })

    # Add recent conversation context
    messages.extend(recent_messages)

    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # -------------------------------
    # Call Groq API
    # -------------------------------

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    # -------------------------------
    # Update conversation history
    # -------------------------------

    recent_messages.append({
        "role": "user",
        "content": user_input
    })

    recent_messages.append({
        "role": "assistant",
        "content": reply
    })

    # Limit conversation size
    if len(recent_messages) > MAX_RECENT * 2:
        recent_messages = recent_messages[-MAX_RECENT * 2:]

    return reply