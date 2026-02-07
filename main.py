from agents.agent1.agent import handle_message

print("🤖 MyBolt Started")
while True:
    msg = input("You: ")
    print("Bot:", handle_message("user1", msg))
