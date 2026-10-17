from llm import ask_llm
from memstore.memory import save_memory

def handle_message(user, message):
    reply = ask_llm(messages)
    save_memory(user, message, reply)
    return reply
