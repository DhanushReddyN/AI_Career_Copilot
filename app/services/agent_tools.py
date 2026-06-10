from langchain_core.tools import tool

from app.services.resume_analyzer import analyze_resume
from app.services.skill_gap_service import analyze_skill_gap
from app.services.roadmap_service import generate_learning_roadmap
from app.services.interview_service import generate_interview_questions
from app.services.interview_prep_service import generate_interview_prep


@tool
def resume_analysis_tool():
    """Analyze the uploaded resume."""
    return analyze_resume()


@tool
def skill_gap_tool():
    """Find missing skills between resume and job description."""
    return analyze_skill_gap()


@tool
def roadmap_tool():
    """Generate a personalized learning roadmap."""
    return generate_learning_roadmap()


@tool
def interview_questions_tool():
    """Generate interview questions."""
    return generate_interview_questions()


@tool
def interview_prep_tool():
    """Generate interview preparation material."""
    return generate_interview_prep()


tools = [
    resume_analysis_tool,
    skill_gap_tool,
    roadmap_tool,
    interview_questions_tool,
    interview_prep_tool
]