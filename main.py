from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import random
from datetime import datetime
from tips import wellness_tips

app = FastAPI(title="Colloki Wellness API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for feedback
feedback_storage = []

class FeedbackModel(BaseModel):
    name: str
    email: Optional[str] = None
    message: str
    category: Optional[str] = "general"

class TipResponse(BaseModel):
    id: int
    category: str
    tip: str
    icon: str

@app.get("/")
async def root():
    return {"message": "Welcome to Colloki Wellness API"}

@app.get("/api/tip", response_model=TipResponse)
async def get_daily_tip(category: Optional[str] = None):
    """Get a random wellness tip, optionally filtered by category"""
    try:
        if category:
            filtered_tips = [tip for tip in wellness_tips if tip["category"] == category]
            if not filtered_tips:
                raise HTTPException(status_code=404, detail="No tips found for this category")
            return random.choice(filtered_tips)
        else:
            return random.choice(wellness_tips)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching tip")

@app.get("/api/tips", response_model=List[TipResponse])
async def get_all_tips():
    """Get all wellness tips"""
    return wellness_tips

@app.get("/api/tips/categories")
async def get_categories():
    """Get all available tip categories"""
    categories = list(set(tip["category"] for tip in wellness_tips))
    return {"categories": categories}

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackModel):
    """Submit user feedback"""
    try:
        feedback_entry = {
            "id": len(feedback_storage) + 1,
            "name": feedback.name,
            "email": feedback.email,
            "message": feedback.message,
            "category": feedback.category,
            "timestamp": datetime.now().isoformat(),
        }
        feedback_storage.append(feedback_entry)
        return {
            "message": "Feedback submitted successfully",
            "id": feedback_entry["id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error submitting feedback")

@app.get("/api/feedbacks")
async def get_all_feedback():
    """Get all submitted feedback (admin endpoint)"""
    return {"feedbacks": feedback_storage, "total": len(feedback_storage)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)