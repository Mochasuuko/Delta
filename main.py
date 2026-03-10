from chat import chat_with_delta

print("Delta is Online. Type 'exit' to quit.\n")

while True:
    user = input("You: ")

    if user.lower() in ["exit", "quit", "shutdown"]:
        print("Delta shutting down.")
        break

    reply = chat_with_delta(user)
    print("Delta:", reply)