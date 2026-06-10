from app.services.resume_analyzer import analyze_resume
from app.services.skill_gap_service import analyze_skill_gap
from app.services.roadmap_service import generate_learning_roadmap
from app.services.interview_service import generate_interview_questions
from app.services.interview_prep_service import generate_interview_prep


def career_coach(query):

    query = query.lower()

    if any(word in query for word in [
        "analyze",
        "resume review",
        "review resume"
    ]):
        return analyze_resume()

    elif any(word in query for word in [
        "skill",
        "missing skill",
        "skills missing",
        "gap"
    ]):
        return analyze_skill_gap()

    elif any(word in query for word in [
        "roadmap",
        "learn",
        "study plan",
        "what should i learn"
    ]):
        return generate_learning_roadmap()

    elif any(word in query for word in [
        "interview question",
        "questions"
    ]):
        return generate_interview_questions()

    elif any(word in query for word in [
        "interview prep",
        "prepare me",
        "interview preparation"
    ]):
        return generate_interview_prep()

    else:
        return """
I can help with:

1. Resume Analysis
2. Skill Gap Detection
3. Learning Roadmap
4. Interview Questions
5. Interview Preparation
"""