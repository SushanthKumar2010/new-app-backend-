import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

try:
    from prompts import get_educational_prompt
except ImportError:
    print("⚠️ prompts.py not found - using inline prompts")

# ======================
# CONFIG
# ======================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set in Render Environment Variables")

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")
print(f"✅ Using model: {MODEL_NAME}")

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
# GEMINI CLIENT
# ======================

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("✅ Gemini client initialized")
except Exception as e:
    print(f"❌ Gemini client failed: {e}")
    client = None

# ======================
# MODELS
# ======================

class QuestionRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    question: str

# ======================
# CHAPTERS
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
        "gemini_ready": client is not None,
        "chapters": CHAPTERS
    }

@app.post("/api/ask")
async def ask_ap_ssc_question(request: QuestionRequest):  # ✅ ASYNC
    """Main endpoint - matches your frontend"""
    
    print(f"📨 Request: {request.dict()}")  # Debug log
    
    # Validate chapter
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter for subject")
    
    if not client:
        raise HTTPException(status_code=500, detail="Gemini client not initialized")
    
    try:
        # Simple inline prompt (no prompts.py dependency)
        prompt = f"""
You are an expert AP SSC Class {request.class_level} tutor.

Subject: {request.subject}
Chapter: {request.chapter}
Question: {request.question}

Provide detailed textbook-style explanation for board exams.
Include examples and practice questions.
"""
        
        print(f"📝 Prompt length: {len(prompt)} chars")
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 800,
            }
        )
        
        answer = response.text or "No response generated"
        print(f"✅ Answer length: {len(answer)} chars")
        
    except Exception as e:
        print(f"❌ Gemini error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")

    return {
        "answer": answer,
        "meta": {
            "class_level": request.class_level,
            "subject": request.subject,
            "chapter": request.chapter,
        },
    }

@app.get("/api/ask")
async def ask_get():
    raise HTTPException(status_code=405, detail="Use POST")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
