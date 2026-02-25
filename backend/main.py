from fastapi import FastAPI
from pydantic import BaseModel
from agent import ask_ai

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are a Personal Discipline Agent.
Reinforce identity.
Be strict but constructive.
Focus on consistency.
"""

@app.get("/")
def health():
    return {"status": "ok", "message": "Janani Backend is running"}

@app.post("/chat")
def chat(req: ChatRequest):
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {req.message}"
    reply = ask_ai(full_prompt)
    return {"reply": reply}