from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import redis
import os
import uuid
from .llm_game import AkinatorGame

# Redis setup
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_cli = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=5)

app = FastAPI(title="Akinator-style Backend (LLM-based)")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class StartResponse(BaseModel):
    session_id: str
    question: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str
    is_feedback: bool = False  # Whether this is a response to a guess

class GuessResponse(BaseModel):
    message: str
    is_guess: bool
    confidence: float = 0.0
    game_over: bool = False

# Session management
def get_redis():
    return redis_cli

def get_game(session_id: str, redis_client) -> AkinatorGame:
    game_data = redis_client.get(f"game:{session_id}")
    if not game_data:
        raise HTTPException(status_code=404, detail="Game session not found")
    return AkinatorGame.from_dict(json.loads(game_data))

def save_game(session_id: str, game: AkinatorGame, redis_client):
    redis_client.set(f"game:{session_id}", json.dumps(game.to_dict()), ex=3600)

# API Endpoints
@app.post("/api/start", response_model=StartResponse)
async def start(redis=Depends(get_redis)):
    try:
        session_id = str(uuid.uuid4())
        game = AkinatorGame()
        first_question = game.generate_question()
        save_game(session_id, game, redis)
        return {"session_id": session_id, "question": first_question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start game: {str(e)}")

@app.post("/api/answer", response_model=GuessResponse)
async def answer(payload: AnswerRequest, redis=Depends(get_redis)):
    try:
        game = get_game(payload.session_id, redis)
        if payload.is_feedback:
            if payload.answer.lower().startswith('n'): 
                game.conversation.pop()  
                next_question = game.generate_question()
                save_game(payload.session_id, game, redis)
                return {"message": next_question, "is_guess": False}
            else: 
                guess_message = game.conversation[-1]["content"]
                character = guess_message.replace("I think your character is: ", "").split(".")[0]
                return {
                    "message": f"Great! I guessed it right! Your character is {character}. Would you like to play again?",
                    "is_guess": False,
                    "game_over": True,
                    "success": True
                }
        result, is_guess = game.process_answer(payload.answer)
        save_game(payload.session_id, game, redis)
        
        if is_guess:
            return {
                "message": f"I think your character is: {result}. Am I right? (Yes/No)",
                "is_guess": True,
                "confidence": 0.9
            }
        return {"message": result, "is_guess": False}
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing answer: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)