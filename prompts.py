# prompts.py - Advanced AP SSC Class 10 educational prompts (100% SYNTAX SAFE)
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

def get_educational_prompt(subject: str, chapter: str, question: str, class_level: str) -> str:
    """✅ SYNTAX SAFE - No f-strings, no errors"""
    
    # Get subject template
    template = SUBJECT_TEMPLATES.get(subject, SUBJECT_TEMPLATES["Mathematics"])
    
    # Format template safely
    formatted_template = template.format(chapter=chapter, question=question)
    
    # Build prompt step by step (NO f-strings)
    header = "You are an expert AP SSC Class {} tutor preparing students for board exams.".format(class_level)
    subject_line = "📖 **SUBJECT**: {}".format(subject)
    chapter_line = "📚 **CHAPTER**: {}".format(chapter)
    question_section = "**విద్యార్థి ప్రశ్న / Student Question:**\n``````".format(question)
    requirements = """**📝 AP SSC EXAM REQUIREMENTS:**
• Follow exact AP SSC textbook pattern (2/4/5 marks)
• Use simple Telugu/English (bilingual where needed)
• Include diagrams (text format: [Diagram: ...])
• End with practice question: "ప్రాక్టీస్ ప్రశ్న / Practice: ..."
• Add: "మరిన్ని ప్రశ్నలు ఉంటే చెప్పండి! / Ask more questions!"

**Format like textbook answer with headings and numbering.**"""
    
    # Join all parts
    full_prompt = "\n\n".join([
        header,
        subject_line,
        chapter_line,
        question_section,
        formatted_template,
        requirements
    ])
    
    return full_prompt.strip()
