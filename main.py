import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

# ======================
# CONFIG (NO ENV NEEDED)
# ======================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set in Render Environment Variables")

MODEL_NAME = "gemini-2.5-flash"  # ✅ Hardcoded - NO ENV needed

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
        "gemini_ready": client is not None,
        "chapters": CHAPTERS
    }

@app.post("/api/ask")
async def ask_ap_ssc_question(request: QuestionRequest):
    """✅ Main endpoint - matches your frontend exactly (fixes 405 error)"""
    
    print(f"📨 Request: {request.dict()}")  # Debug log
    
    # Validate chapter exists (matching your frontend)
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter for subject")
    
    if not client:
        raise HTTPException(status_code=500, detail="Gemini client not initialized - check GEMINI_API_KEY")
    
    try:
        # ✅ Advanced educational prompt (inline - no prompts.py needed)
        prompt = f"""
You are an expert AP SSC Class {request.class_level} tutor preparing students for board exams.

📖 **SUBJECT**: {request.subject}
📚 **CHAPTER**: {request.chapter}

**విద్యార్థి ప్రశ్న / Student Question:**
