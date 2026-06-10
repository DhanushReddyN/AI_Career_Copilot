from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.career_agent_v2 import career_agent

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    history: str = ""   # history is optional, defaults to empty string


@router.post("/career-agent")
async def career_agent_api(request: ChatRequest):
    """
    Career coach chat endpoint.
    Returns a JSON body with a 'response' key in ALL cases —
    including when the agent encounters rate-limits or tool errors.
    This prevents the frontend from receiving an empty body and
    crashing with a JSONDecodeError.
    """
    try:
        result = career_agent(request.question, request.history)
        # career_agent now returns a string in all cases (including errors)
        return {"response": result}

    except Exception as e:
        # Last-resort catch — should not normally be reached
        error_str = str(e)
        if "rate_limit_exceeded" in error_str or "429" in error_str:
            # Return a friendly message rather than a 500
            return {
                "response": (
                    "⚠️ The AI model is temporarily rate-limited. "
                    "Please wait a few minutes and try again."
                )
            }
        # For unexpected errors, raise a proper HTTP 500 with detail
        raise HTTPException(status_code=500, detail=error_str)