import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

# ======================
# CONFIG
# ======================

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not set")

MODEL_NAME = "gemini-2.5-flash"
print("✅ Using model: {}".format(MODEL_NAME))

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
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    print("✅ Gemini client initialized")
except Exception as e:
    print("❌ Gemini client failed: {}".format(e))
    model = None

# ======================
# MODELS
# ======================

class QuestionRequest(BaseModel):
    class_level: str
    subject: str
    chapter: str
    question: str

# ======================
# AP SSC CHAPTERS & CONTEXT
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
# SUBJECT-SPECIFIC CONTEXT
# ======================

SUBJECT_CONTEXT = {
    "Mathematics": {
        "Real Numbers": "Euclid's Division Lemma (a = bq + r), HCF/LCM, Irrational numbers (√2, π), Decimal expansions",
        "Polynomials": "p(x)=0 zeroes, Factor Theorem, Division Algorithm, Quadratic graphs",
        "Quadratic Equations": "ax²+bx+c=0, D=b²-4ac, Nature of roots, Word problems",
        "Triangles": "Similarity criteria (AAA, SSS, SAS), Pythagoras theorem, Basic Proportionality Theorem"
    },
    "Science": {
        "Chemical Reactions": "Combination, Decomposition, Displacement, Double Displacement, Redox reactions, Balancing equations",
        "Life Processes": "Nutrition (Photosynthesis, Human digestion), Respiration (Aerobic/Anaerobic), Transportation, Excretion",
        "Control & Coordination": "Reflex arc, Neurons, Plant hormones (Auxin), Human brain (Cerebrum, Cerebellum)"
    },
    "English": {
        "Prose": "A Letter to God (Lencho), Nelson Mandela (Long Walk), Anne Frank Diary",
        "Poetry": "Dust of Snow (Robert Frost), Fire and Ice, Tiger in Zoo (Leslie Norris)"
    },
    "Social Studies": {
        "Nationalism in India": "Non-Cooperation (1920-22), Civil Disobedience (1930), Quit India (1942), Gandhi-Irwin Pact",
        "Industrialization": "First factories, Hand labour vs machines, Indian textiles decline"
    }
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
        "gemini_ready": model is not None,
        "chapters": CHAPTERS
    }

@app.post("/api/ask")
async def ask_ap_ssc_question(request: QuestionRequest):
    """🚀 PROFESSIONAL AP SSC EXAM TUTOR"""
    
    print("📨 Request: {}".format(request.dict()))
    
    if request.chapter not in CHAPTERS.get(request.subject, []):
        raise HTTPException(status_code=400, detail="Invalid chapter")
    
    if not model:
        raise HTTPException(status_code=500, detail="Gemini not ready")
    
    try:
        # 🔥 ULTIMATE AP SSC EXAM PREP PROMPT
        context = SUBJECT_CONTEXT.get(request.subject, {}).get(request.chapter, "")
        
        prompt = """
🚨 YOU ARE AN AP SSC CLASS 10 BOARD EXAM EXPERT 🚨

📚 SUBJECT: {subject} | 📖 CHAPTER: {chapter}
📄 TEXTBOOK CONTEXT: {context}
🎯 STUDENT QUESTION: {question}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 REQUIRED EXAM ANSWER FORMAT (FOLLOW EXACTLY):

📌 **I. CONCEPT EXPLANATION (2 MARKS)**
   • Definition + Key formula/theorem
   • 1 textbook diagram [Draw: ...]
   • 1 real-life example

📌 **II. STEP-BY-STEP SOLUTION (4 MARKS)**
   1. Given data
   2. Formula/Theorem used
   3. Step 1 → Step 2 → Final Answer ✅
   4. Verification

📌 **III. SOLVED EXAMPLE 1 (Similar Question)**
   Q: ... A: [Complete solution]

📌 **IV. SOLVED EXAMPLE 2 (Exam Pattern)**
   Q: ... A: [Complete solution]

📌 **V. PRACTICE QUESTION (Homework)**
   Q: [New question] 
   👉 Answer: [Direct answer]

📌 **VI. COMMON EXAM MISTAKES ⚠️**
   ❌ Mistake 1: ...
   ❌ Mistake 2: ...
   ✅ Correct method: ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 BOARD EXAM TIPS:
• Use AP SSC textbook exact terms
• Write in points/bullets for 5-mark questions
• Draw labelled diagrams (text format)
• Show ALL working steps
• Answer in Telugu/English as needed

📝 END WITH: "పరీక్షకు ముఖ్యమైన పాయింట్లు గుర్తుంచుకోండి! 💯"
        """.format(
            subject=request.subject,
            chapter=request.chapter,
            context=context,
            question=request.question
        )
        
        print("📝 Prompt: {} chars".format(len(prompt)))
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,  # More consistent
                "max_output_tokens": 1500,
                "top_p": 0.8,
            }
        )
        
        answer = response.text or "No answer generated"
        print("✅ Answer: {} chars".format(len(answer)))
        
    except Exception as e:
        print("❌ Error: {}".format(e))
        raise HTTPException(status_code=500, detail="AI Error: {}".format(e))

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
    raise HTTPException(status_code=405, detail="POST only")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
