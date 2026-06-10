from fastapi import APIRouter

from app.services.agent_tools import tools

router = APIRouter()

@router.get("/tools")
def list_tools():

    return {
        "tools": [
            tool.name
            for tool in tools
        ]
    }