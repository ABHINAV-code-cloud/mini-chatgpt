import openai

openai.api_key = "YOUR_API_KEY"

def ask_llm(prompt):
    res = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
