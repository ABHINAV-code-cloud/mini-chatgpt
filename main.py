
from agents.router import route_message

print("🤖 MyBolt Started")

while True:
    msg = input("You: ")

    if msg.strip().lower() in {"exit", "quit"}:
        print("Bot: Goodbye!")
        break

    try:
        reply = route_message("user1", msg)
        print("Bot:", reply)
    except ValueError as exc:
        print("Bot: Invalid input:", exc)
