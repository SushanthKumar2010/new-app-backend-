import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# Import prompts module
from prompts import get_educational_prompt

# ======================
# CONFIG
# ======================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set")

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

# ======================
# APP SETUP
# ======================

app = FastAPI(
    title="AP SSC Class 10 AI Tutor",
    description="FastAPI backend for AP SSC Class 10 tutor using Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# GEMINI CLIENT (NEW SDK)
# ======================

client = genai.Client(api_key=GEMINI_API_KEY)

# ======================
# MODELS (matching your frontend)
# ======================

class QuestionRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    question: str

# ======================
# CHAPTER VALIDATION (matching your frontend)
# ======================

CHAPTERS = {
    "Telugu": ["కథలు", "కవిత్వం", "వ్యాకరణం"],
    "English": ["Prose", "Poetry", "Grammar"],
    "Hindi": ["गद्य", "पद्य", "వ్యాకరణం"],
    "Mathematics": ["Real Numbers", "Polynomials", "Quadratic Equations", "Triangles"],
    "Science": ["Chemical Reactions", "Life Processes", "Control & Coordination"],
    "Social Studies": ["Nationalism in India", "Industrialization", "Citizenship"]
}

# ======================
# ROUTES
# ======================

@app.get("/")
def root():
    return {"status": "AP SSC Class 10 AI Tutor Backend running ✅"}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "chapters": CHAPTERS
    }

@app.post("/api/chat")
def simple_chat(data: dict):
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ask")
def ask_ap_ssc_question(request: QuestionRequest):
    """✅ Main endpoint - matches your frontend exactly (fixes 405 error)"""
    
    # Validate chapter exists (matching your frontend)
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter for subject")
    
    try:
        # ✅ Use advanced prompts.py for structured educational answers
        prompt = get_educational_prompt(
            request.subject, 
            request.chapter, 
            request.question, 
            request.class_level
        )
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 1200,
                "top_p": 0.8,
            }
        )
        answer = (response.text or "I could not generate an answer.").strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {e}")

    # ✅ Exact response format your frontend expects
    return {
        "answer": answer,
        "meta": {
            "class_level": request.class_level,
            "subject": request.subject,
            "chapter": request.chapter,
        },
    }

@app.get("/api/ask")
def ask_get():
    """GET version - shows 405 in browser (expected)"""
    raise HTTPException(status_code=405, detail="Method Not Allowed. Use POST.")

# ======================
# RENDER DEPLOYMENT
# ======================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
