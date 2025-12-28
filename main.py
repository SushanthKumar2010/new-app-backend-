# main.py - Complete FastAPI backend for AP SSC Class 10 AI Tutor (GEMINI)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional
import google.generativeai as genai

# Import custom modules
from prompts import get_educational_prompt
from config import GEMINI_API_KEY, MODEL_NAME, SUBJECT_CONTEXTS

app = FastAPI(title="AP SSC Class 10 AI Tutor Backend")

# CORS - Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Pydantic model matching YOUR frontend exactly
class QuestionRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    question: str

# Chapter validation (matching your frontend)
CHAPTERS = {
    "Telugu": ["కథలు", "కవిత్వం", "వ్యాకరణం"],
    "English": ["Prose", "Poetry", "Grammar"],
    "Hindi": ["गद्य", "पद्य", "వ్యాకరణం"],
    "Mathematics": ["Real Numbers", "Polynomials", "Quadratic Equations", "Triangles"],
    "Science": ["Chemical Reactions", "Life Processes", "Control & Coordination"],
    "Social Studies": ["Nationalism in India", "Industrialization", "Citizenship"]
}

# Initialize Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ✅ THE MISSING POST ROUTE - This fixes your 405 "Method Not Allowed" error
@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """Main endpoint - matches your frontend exactly"""
    
    # Validate chapter exists (same as your frontend)
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter for subject")
    
    try:
        # Generate detailed AI answer using prompts.py
        full_prompt = get_educational_prompt(
            request.subject, 
            request.chapter, 
            request.question, 
            request.class_level
        )
        
        # Gemini API call
        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 1000,
                "top_p": 0.8,
            }
        )
        
        answer = response.text
        
        # ✅ Exact response format your frontend expects
        return {
            "answer": answer,
            "meta": {
                "subject": request.subject,
                "chapter": request.chapter
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

# Health check endpoints (browser-friendly)
@app.get("/")
async def root():
    return {"message": "AP SSC Class 10 AI Tutor Backend (Gemini) - Ready!", "status": "healthy"}

@app.get("/api/ask")
async def ask_get():
    """GET version - shows 405 in browser (expected behavior)"""
    raise HTTPException(status_code=405, detail="Method Not Allowed. Use POST request.")

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "model": MODEL_NAME,
        "provider": "Gemini",
        "chapters": CHAPTERS
    }

# Render.com startup
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
