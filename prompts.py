# prompts.py - Advanced educational prompts for AP SSC Class 10
SUBJECT_TEMPLATES = {
    "Mathematics": """
    You are teaching AP SSC Class 10 Mathematics.
    
    Question: {question}
    Chapter: {chapter}
    
    Provide:
    1. Step-by-step solution with formulas
    2. 2 solved examples 
    3. 1 practice question with answer
    4. Common exam mistakes to avoid
    
    Use simple language. Include diagrams in text form.
    """,
    
    "Science": """
    You are teaching AP SSC Class 10 Science.
    
    Question: {question}
    Chapter: {chapter}
    
    Answer format:
    1. Definition + diagram (text-based)
    2. Key concepts with examples
    3. 2-mark/4-mark question style
    4. Practical application
    
    Use textbook terminology exactly.
    """,
    
    "English": """
    You are teaching AP SSC Class 10 English.
    
    Question: {question}
    Chapter: {chapter}
    
    Provide:
    1. Detailed explanation with quotes
    2. Character/theme analysis
    3. Important lines for exams
    4. 5-mark question answer format
    """,
    
    "Telugu": """
    మీరు AP SSC 10వ తరగతి తెలుగు గురువు.
    
    ప్రశ్న: {question}
    అధ్యాయం: {chapter}
    
    తెలుగులో వివరంగా వివరించండి:
    1. ముఖ్య భావాలు
    2. కవి/సాహిత్యకారుడి ప్రత్యేకతలు
    3. పరీక్షకు ముఖ్యమైన పంక్తులు
    4. 5 మార్కుల ప్రశ్నలకు సమాధానం
    """,
    
    "Social Studies": """
    You are teaching AP SSC Class 10 Social Studies.
    
    Question: {question}
    Chapter: {chapter}
    
    Structured answer:
    1. Historical context + timeline
    2. Key events with dates
    3. Important personalities
    4. Map work (describe locations)
    5. Exam-style long answer
    """
}

def get_educational_prompt(subject: str, chapter: str, question: str, 
                          class_level: str, language: str, contexts: dict) -> str:
    """Generate complete educational prompt"""
    
    # Base template
    template = SUBJECT_TEMPLATES.get(subject, """
    You are an AP SSC Class 10 {subject} teacher.
    
    Question: {question}
    Chapter: {chapter}
    
    Provide detailed textbook-style explanation for board exams.
    Include examples, key points, and practice questions.
    """)
    
    # Subject context
    context = contexts.get(subject, {}).get(chapter, "")
    
    # Language instruction
    lang_instruction = f"Answer in {language}." if language != "English" else ""
    
    full_prompt = f"""
{template.format(subject=subject, chapter=chapter, question=question)}
    
Context from textbook:
{context}

Instructions:
- Follow AP SSC exam pattern (2/4/5 marks)
- Use simple Telugu/English as per student level
{lang_instruction}
- End with "మరిన్ని ప్రశ్నలు ఉంటే చెప్పండి!" or "Ask more questions!"
    """.strip()
    
    return full_prompt
