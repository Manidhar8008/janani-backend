from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ask_ai
from models import UserProfile, UserInput, Game, Goal, Feedback, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

app = FastAPI()

# Database setup
def get_db_url():
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    return "postgresql://postgres:Facebooklit@localhost:5432/manidhar_ai"

engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ChatRequest(BaseModel):
    message: str

# --- Pydantic Schemas for API ---
class UserProfileSchema(BaseModel):
    name: str
    email: str

class UserInputSchema(BaseModel):
    user_id: int
    input_type: str
    content: str

class GameSchema(BaseModel):
    user_id: int
    game_type: str
    result: str

class GoalSchema(BaseModel):
    user_id: int
    description: str
    status: str

class FeedbackSchema(BaseModel):
    user_id: int
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

# --- User Profile Endpoints ---
@app.post("/profile")
def create_profile(profile: UserProfileSchema):
    db = SessionLocal()
    user = UserProfile(name=profile.name, email=profile.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return {"id": user.id, "name": user.name, "email": user.email}

# --- User Input Endpoints ---
@app.post("/user-input")
def create_user_input(user_input: UserInputSchema):
    db = SessionLocal()
    inp = UserInput(user_id=user_input.user_id, input_type=user_input.input_type, content=user_input.content)
    db.add(inp)
    db.commit()
    db.refresh(inp)
    db.close()
    return {"id": inp.id}

# --- Game Endpoints ---
@app.post("/games")
def create_game(game: GameSchema):
    db = SessionLocal()
    g = Game(user_id=game.user_id, game_type=game.game_type, result=game.result)
    db.add(g)
    db.commit()
    db.refresh(g)
    db.close()
    return {"id": g.id}

# --- Goal Endpoints ---
@app.post("/goals")
def create_goal(goal: GoalSchema):
    db = SessionLocal()
    gl = Goal(user_id=goal.user_id, description=goal.description, status=goal.status)
    db.add(gl)
    db.commit()
    db.refresh(gl)
    db.close()
    return {"id": gl.id}

# --- Feedback Endpoints ---
@app.post("/feedback")
def create_feedback(feedback: FeedbackSchema):
    db = SessionLocal()
    fb = Feedback(user_id=feedback.user_id, message=feedback.message)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    db.close()
    return {"id": fb.id}