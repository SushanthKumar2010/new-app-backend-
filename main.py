# main.py - Complete FastAPI backend with prompts.py & config.py integration
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional
import openai
from openai import OpenAI

# Import custom modules
from prompts import get_educational_prompt
from config import OPENAI_API_KEY, MODEL_NAME, SUBJECT_CONTEXTS

app = FastAPI(title="AP SSC Class 10 AI Tutor Backend")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class QuestionRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    question: str
    language: Optional[str] = "English"  # Telugu/English

class AnswerMeta(BaseModel):
    subject: str
    chapter: str
    class_level: str
    language: str

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

CHAPTERS = {
    "Telugu": ["కథలు", "కవిత్వం", "వ్యాకరణం"],
    "English": ["Prose", "Poetry", "Grammar"],
    "Hindi": ["गद्य", "पद्य", "వ్యాకరణం"],
    "Mathematics": ["Real Numbers", "Polynomials", "Quadratic Equations", "Triangles"],
    "Science": ["Chemical Reactions", "Life Processes", "Control & Coordination", "Light", "Electricity", "Magnetic effects of electric current", "Sources of energy"],
    "Social Studies": ["Nationalism in India", "Industrialization", "Citizenship"]
}

@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """Main AI-powered endpoint"""
    
    # Validate input
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter for subject")
    
    try:
        # Generate detailed answer using prompts.py
        full_prompt = get_educational_prompt(
            request.subject, 
            request.chapter, 
            request.question, 
            request.class_level,
            request.language,
            SUBJECT_CONTEXTS
        )
        
        # Call OpenAI
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "system", 
                "content": "You are an expert AP SSC Class 10 teacher."
            }, {
                "role": "user", 
                "content": full_prompt
            }],
            temperature=0.3,
            max_tokens=800
        )
        
        answer = response.choices[0].message.content
        
        return {
            "answer": answer,
            "meta": AnswerMeta(
                subject=request.subject,
                chapter=request.chapter,
                class_level=request.class_level,
                language=request.language
            )
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@app.get("/")
async def root():
    return {"message": "AP SSC Class 10 AI Tutor Backend - Ready!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model": MODEL_NAME}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
