import json
import os

MEMORY_FILE = os.path.join(
    os.path.dirname(__file__),
    "memory.json"
)

def save_memory(user, q, a):
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump([], f)

    with open(MEMORY_FILE, "r+") as f:
        data = json.load(f)
        data.append({
            "user": user,
            "question": q,
            "answer": a
        })
        f.seek(0)
        json.dump(data, f, indent=2)
