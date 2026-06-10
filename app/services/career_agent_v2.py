from langchain_core.messages import HumanMessage, ToolMessage
from app.services.llm_service import get_llm_smart

from app.services.agent_tools import (
    resume_analysis_tool,
    skill_gap_tool,
    roadmap_tool,
    interview_questions_tool,
    interview_prep_tool
)

# Map tool names → callable tool objects
TOOL_MAP = {
    "resume_analysis_tool": resume_analysis_tool,
    "skill_gap_tool": skill_gap_tool,
    "roadmap_tool": roadmap_tool,
    "interview_questions_tool": interview_questions_tool,
    "interview_prep_tool": interview_prep_tool,
}

# Use the rate-limit-aware LLM wrapper
_llm_smart = get_llm_smart()


def _get_llm_with_tools():
    """
    Build the LLM + tools binding each time, using whichever Groq model
    is currently available (the smart wrapper picks the working one).
    """
    from app.services.llm_service import get_llm, PRIMARY_MODEL, FALLBACK_MODELS
    import groq

    models = [PRIMARY_MODEL] + FALLBACK_MODELS
    for model in models:
        try:
            llm = get_llm(model)
            return llm.bind_tools(list(TOOL_MAP.values()))
        except Exception:
            continue

    # Final fallback: return a plain LLM without tools
    from app.services.llm_service import get_llm
    return get_llm(FALLBACK_MODELS[-1])


def career_agent(query: str, history: str = "") -> str:
    """
    Main career coach agent function.

    Decides whether to invoke a specialised tool (resume analysis,
    skill gap, roadmap, interview prep/questions) or answer directly,
    then returns a plain string response.
    """

    system_instructions = """You are an expert AI Career Coach.

You have access to the following tools:
- resume_analysis_tool: Analyze the uploaded resume
- skill_gap_tool: Find skills the candidate is missing vs the job description
- roadmap_tool: Generate a personalised 6-month learning roadmap
- interview_questions_tool: Generate tailored interview questions
- interview_prep_tool: Generate interview preparation material with model answers

Rules:
1. ALWAYS use a tool when the question is about resume, skills, roadmap, or interview.
2. For general career advice, answer directly without a tool.
3. Keep responses professional and helpful.
4. If a tool call fails, explain what happened and suggest the user retry.
"""

    full_prompt = f"""{system_instructions}

Conversation History (use only if relevant):
{history}

User Question:
{query}
"""

    try:
        llm_with_tools = _get_llm_with_tools()
        response = llm_with_tools.invoke([HumanMessage(content=full_prompt)])
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            return (
                "⚠️ The AI model is temporarily rate-limited (daily token quota reached). "
                "Please wait a few minutes and try again."
            )
        return f"❌ An error occurred while contacting the AI: {error_str}"

    # No tool was chosen — direct answer
    if not response.tool_calls:
        return response.content or "I'm not sure how to help with that. Try asking about your resume, skill gaps, or interview prep."

    # Execute the first requested tool
    tool_name = response.tool_calls[0].get("name", "")
    tool_fn = TOOL_MAP.get(tool_name)

    if tool_fn is None:
        return f"I tried to use the tool '{tool_name}' but it wasn't found. Please try again."

    try:
        result = tool_fn.invoke({})
        return result
    except Exception as e:
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            return (
                "⚠️ The AI model hit its daily token limit while generating your answer. "
                "Please wait a few minutes and try again."
            )
        return f"❌ Error while running '{tool_name}': {error_str}"