conversation_history = [
    {"role": "system", "content": "You are Delta, an AI designed for probability, logic, and deep reasoning."}
]

def add_user_message(msg):
    conversation_history.append({"role": "user", "content": msg})

def add_ai_message(msg):
    conversation_history.append({"role": "assistant", "content": msg})

def get_history():
    return conversation_history