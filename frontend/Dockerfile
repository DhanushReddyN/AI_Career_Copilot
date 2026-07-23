# ─────────────────────────────────────────────────────────────
# Frontend Dockerfile — AI Career Copilot Streamlit App
# ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Install frontend dependencies
COPY frontend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit app and config
COPY frontend/ ./frontend/
COPY .streamlit/ ./.streamlit/

# Expose Streamlit port
EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# Start Streamlit
CMD ["streamlit", "run", "frontend/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.fileWatcherType=none"]