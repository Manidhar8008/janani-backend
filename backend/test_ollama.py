import ollama

response = ollama.chat(
    model='llama3',
    messages=[
        {"role": "user", "content": "Say hello to Manidhar's personal AI system."}
    ]
)

print(response['message']['content'])