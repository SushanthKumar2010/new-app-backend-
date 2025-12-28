# main.py - Complete FastAPI backend for AP SSC Class 10 AI Tutor
# Deploy this to Render.com (https://new-app-backend-bp5i.onrender.com)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Optional

app = FastAPI(title="AP SSC Class 10 AI Tutor Backend")

# CORS - Allow your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model matching your frontend
class QuestionRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    question: str

class AnswerMeta(BaseModel):
    subject: str
    chapter: str

# Sample chapter data (expand as needed)
CHAPTERS = {
    "Telugu": ["కథలు", "కవిత్వం", "వ్యాకరణం"],
    "English": ["Prose", "Poetry", "Grammar"],
    "Hindi": ["गद्य", "पद्य", "వ్యాకరణం"],
    "Mathematics": ["Real Numbers", "Polynomials", "Quadratic Equations", "Triangles"],
    "Science": ["Chemical Reactions", "Life Processes", "Control & Coordination"],
    "Social Studies": ["Nationalism in India", "Industrialization", "Citizenship"]
}

# ✅ THE MISSING POST ROUTE - This fixes your 405 error
@app.post("/api/ask")
async def ask_question(request: QuestionRequest):
    """Main endpoint - returns answer for student's question"""
    
    # Validate chapter exists for subject
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter for subject")
    
    # TODO: Replace with real AI (OpenAI/Groq/Gemini)
    # For now, generate structured educational response
    answer = generate_educational_answer(request)
    
    return {
        "answer": answer,
        "meta": {
            "subject": request.subject,
            "chapter": request.chapter,
            "class_level": request.class_level
        }
    }

def generate_educational_answer(request: QuestionRequest) -> str:
    """Generate structured answer (replace with AI API call)"""
    
    subject_answers = {
        "Mathematics": "Real numbers are all rational and irrational numbers on the number line. For example, √2 and π are irrational real numbers.",
        "Science": "Chemical reactions involve rearrangement of atoms. Example: 2H₂ + O₂ → 2H₂O (combustion).",
        "English": "Prose is written in sentences and paragraphs, unlike poetry which uses rhythm and rhyme.",
        # Add more subject-specific explanations
    }
    
    base_answer = subject_answers.get(request.subject, "Great question! Here's a detailed explanation...")
    
    return f"""
**📚 {request.subject} - {request.chapter}**

{base_answer}

**💡 Key Points:**
• Understand the concept first
• Practice 5-10 related questions daily
• Refer to your AP SSC textbook page 45-52

**❓ Practice Question:** What is another example of this concept?
    """.strip()

# Health check (for Render)
@app.get("/")
async def root():
    return {"message": "AP SSC Class 10 AI Tutor Backend - Ready!"}

@app.get("/api/ask")
async def ask_get():
    """Health check for GET - Frontend uses POST only"""
    raise HTTPException(status_code=405, detail="Method Not Allowed. Use POST.")

# Run with: uvicorn main:app --host 0.0.0.0 --port $PORT
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
