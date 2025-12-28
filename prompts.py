# prompts.py - Educational prompts for AP SSC Class 10 (unchanged)
SUBJECT_TEMPLATES = {
    "Mathematics": """
    AP SSC Class 10 {subject} - Chapter: {chapter}
    Student Question: {question}
    
    Provide:
    1. Step-by-step solution with formulas
    2. 2 solved examples 
    3. 1 practice question with answer
    4. Common exam mistakes to avoid
    
    Use simple language. Include diagrams in text form.
    """,
    
    "Science": """
    AP SSC Class 10 {subject} - Chapter: {chapter}
    Student Question: {question}
    
    Answer format:
    1. Definition + diagram (text-based)
    2. Key concepts with examples
    3. 2-mark/4-mark question style
    4. Practical application
    
    Use textbook terminology exactly.
    """,
    
    "English": """
    AP SSC Class 10 {subject} - Chapter: {chapter}
    Student Question: {question}
    
    Provide:
    1. Detailed explanation with quotes
    2. Character/theme analysis
    3. Important lines for exams
    4. 5-mark question answer format
    """,
    
    "Telugu": """
    AP SSC 10వ తరగతి {subject} - అధ్యాయం: {chapter}
    విద్యార్థి ప్రశ్న: {question}
    
    తెలుగులో వివరంగా వివరించండి:
    1. ముఖ్య భావాలు
    2. కవి/సాహిత్యకారుడి ప్రత్యేకతలు
    3. పరీక్షకు ముఖ్యమైన పంక్తులు
    4. 5 మార్కుల ప్రశ్నలకు సమాధానం
    """,
    
    "Social Studies": """
    AP SSC Class 10 {subject} - Chapter: {chapter}
    Student Question: {question}
    
    Structured answer:
    1. Historical context + timeline
    2. Key events with dates
    3. Important personalities
    4. Map work (describe locations)
    5. Exam-style long answer
    """,
    
    "Hindi": """
    AP SSC कक्षा 10 {subject} - अध्याय: {chapter}
    छात्र प्रश्न: {question}
    
    हिंदी में विस्तृत व्याख्या:
    1. मुख्य बिंदु
    2. कवि/लेखक विशेषताएं
    3. परीक्षा के लिए महत्वपूर्ण पंक्तियां
    4. 5 अंकों का उत्तर
    """
}

def get_educational_prompt(subject: str, chapter: str, question: str, class_level: str) -> str:
    """Generate complete educational prompt for Gemini"""
    
    template = SUBJECT_TEMPLATES.get(subject, """
    You are an AP SSC Class 10 {subject} teacher.
    
    Question: {question}
    Chapter: {chapter}
    
    Provide detailed textbook-style explanation for board exams.
    Include examples, key points, and practice questions.
    """)
    
    return template.format(
        subject=subject, 
        chapter=chapter, 
        question=question
    )
