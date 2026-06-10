from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.resume import router as resume_router
from app.routes.jd import router as jd_router
from app.routes.test_tools import router as tools_router
from app.routes.agent import router as agent_router


app = FastAPI(
    title="AI Career Copilot",
    description="Intelligent Resume Analyzer & Career Assistant using RAG and AI Agents",
    version="1.0.0"
)

# Allow Streamlit Cloud frontend to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Tighten this to your Streamlit Cloud URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(jd_router)
app.include_router(tools_router)
app.include_router(agent_router)


@app.get("/health")
def health_check():
    """Health check endpoint for Render and Docker."""
    return {"status": "ok", "service": "AI Career Copilot API"}