# prompts.py - Advanced AP SSC Class 10 educational prompts
# Works with your main.py Gemini backend

SUBJECT_TEMPLATES = {
    "Mathematics": """
You are an expert AP SSC Class 10 Mathematics teacher.

Chapter: {chapter}
Student Question: {question}

📚 **DETAILED ANSWER REQUIRED:**

1️⃣ **Concept Explanation** (with formulas)
2️⃣ **Step-by-step solution** (show all working)
3️⃣ **2 Solved Examples** (similar difficulty)
4️⃣ **1 Practice Question** + answer
5️⃣ **Common Exam Mistakes** to avoid

💡 Use AP SSC textbook examples and notation exactly.
""",

    "Science": """
You are an expert AP SSC Class 10 Science teacher.

Chapter: {chapter}
Student Question: {question}

🧪 **COMPLETE ANSWER STRUCTURE:**

1️⃣ **Definition** + diagram (text format)
2️⃣ **Key Concepts** with real examples
3️⃣ **Chemical/Physical process** explanation
4️⃣ **2-mark & 4-mark question** format
5️⃣ **Practical application** + diagram

🔬 Use exact textbook terminology and diagrams.
""",

    "English": """
You are an expert AP SSC Class 10 English teacher.

Chapter: {chapter}
Student Question: {question}

📖 **LITERATURE ANALYSIS:**

1️⃣ **Detailed explanation** with text quotes
2️⃣ **Character/Theme analysis**
3️⃣ **Important lines** (5-mark questions)
4️⃣ **Context & background**
5️⃣ **Exam-style answer** format

✍️ Quote exact lines from AP SSC textbook.
""",

    "Telugu": """
మీరు AP SSC 10వ తరగతి తెలుగు గురువు.

అధ్యాయం: {chapter}
విద్యార్థి ప్రశ్న: {question}

📚 **వివరణాత్మక సమాధానం:**

1️⃣ **ముఖ్య భావం** వివరణ
2️⃣ **కవి/సాహిత్యకారుడు** విశ్లేషణ
3️⃣ **పరీక్ష ముఖ్య పంక్తులు**
4️⃣ **5 మార్కుల ప్రశ్న** ఫార్మాట్
5️⃣ **సమాన ఉదాహరణలు**

📖 పాఠ్యపుస్తకం నుండి ఖచ్చితమైన పంక్తులు ఉపయోగించండి.
""",

    "Hindi": """
आप AP SSC कक्षा 10 हिंदी के विशेषज्ञ शिक्षक हैं।

अध्याय: {chapter}
छात्र प्रश्न: {question}

📚 **विस्तृत उत्तर:**

1️⃣ **मुख्य भाव** की व्याख्या
2️⃣ **कवि/लेखक** विश्लेषण
3️⃣ **परीक्षा महत्वपूर्ण पंक्तियाँ**
4️⃣ **5 अंकों का उत्तर** प्रारूप
5️⃣ **समान उदाहरण**

📖 पाठ्यपुस्तक से सटीक पंक्तियाँ उद्धृत करें।
""",

    "Social Studies": """
You are an expert AP SSC Class 10 Social Studies teacher.

Chapter: {chapter}
Student Question: {question}

🌍 **COMPLETE EXAM ANSWER:**

1️⃣ **Historical Context** + timeline
2️⃣ **Key Events** with exact dates
3️⃣ **Important Personalities**
4️⃣ **Map Work** (describe locations)
5️⃣ **5-mark question** format

📅 Use AP SSC textbook dates and facts exactly.
"""
}

CHAPTER_SPECIFIC_CONTEXT = {
    "Mathematics": {
        "Real Numbers": "Euclid's Division Lemma: For a,b > 0, a = bq + r (0 ≤ r < b). HCF, LCM, Irrational numbers (√2, π)",
        "Polynomials": "Zeroes of polynomial p(x), Factor theorem, Division algorithm",
        "Quadratic Equations": "ax² + bx + c = 0, Discriminant D = b²-4ac, Nature of roots",
    },
    "Science": {
        "Chemical Reactions": "Combination, Decomposition, Displacement, Double Displacement, Redox reactions",
        "Life Processes": "Autotrophic nutrition (photosynthesis), Human digestive system, Respiration (aerobic/anaerobic)",
        "Control & Coordination": "Reflex arc, Plant hormones (auxin), Human brain parts",
    },
    "English": {
        "Prose": "A Letter to God, Nelson Mandela, From the Diary of Anne Frank (key quotes)",
        "Poetry": "Dust of Snow, Fire and Ice, A Tiger in the Zoo (poetic devices)",
    },
    "Telugu": {
        "కథలు": "పొత్తి సీతారాములు, అమ్మమొహనం - ముఖ్య సంఘటనలు",
        "కవిత్వం": "అమరావతి గల్లు, సామాజిక దృక్పథం - కవి భావాలు",
    }
}

def get_educational_prompt(subject: str, chapter: str, question: str, class_level: str) -> str:
    """
    Generate complete educational prompt for your main.py /api/ask endpoint
    Returns ready-to-use prompt string for Gemini
    """
    
    # Get subject template
    template = SUBJECT_TEMPLATES.get(subject, SUBJECT_TEMPLATES["Mathematics"])
    
    # Get chapter context
    context = CHAPTER_SPECIFIC_CONTEXT.get(subject, {}).get(chapter, "")
    
    full_prompt = f"""
You are an expert AP SSC Class {class_level} tutor preparing students for board exams.

📖 **SUBJECT**: {subject}
📚 **CHAPTER**: {chapter}
{'📄 **CONTEXT**: ' + context if context else ''}

**విద్యార్థి ప్రశ్న / Student Question:**
