import os
import time
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Primary model (high quality, higher token usage)
PRIMARY_MODEL = "llama-3.3-70b-versatile"

# Fallback models in order of preference — all free on Groq
FALLBACK_MODELS = [
    "llama-3.1-8b-instant",       # Very fast, low token usage
    "gemma2-9b-it",               # Google Gemma 2, reliable fallback
    "mixtral-8x7b-32768",         # Mixtral, larger context window
]


def get_llm(model_name: str = PRIMARY_MODEL):
    """Return a ChatGroq LLM instance for the given model."""
    return ChatGroq(
        model=model_name,
        temperature=0
    )


class RateLimitAwareLLM:
    """
    A thin wrapper around ChatGroq that automatically retries with
    progressively smaller fallback models when a 429 rate-limit error
    is encountered. This prevents Internal Server Errors when the
    primary model's daily quota is exhausted.
    """

    def __init__(self):
        self._primary = PRIMARY_MODEL
        self._fallbacks = FALLBACK_MODELS

    def invoke(self, prompt: str):
        models_to_try = [self._primary] + self._fallbacks

        last_error = None
        for model in models_to_try:
            try:
                llm = get_llm(model)
                response = llm.invoke(prompt)
                return response
            except Exception as e:
                error_str = str(e)
                # Check for rate-limit (429) or token-limit errors
                if "rate_limit_exceeded" in error_str or "429" in error_str or "tokens per" in error_str:
                    print(f"[LLM] Rate limit hit on '{model}', trying next fallback...")
                    last_error = e
                    # Small back-off before switching model
                    time.sleep(1)
                    continue
                else:
                    # Non-rate-limit error — re-raise immediately
                    raise

        # All models exhausted — raise the last rate-limit error with a
        # clear, human-readable message
        raise RuntimeError(
            "All Groq models have hit their rate limits. "
            "Please wait a few minutes and try again, or upgrade your Groq plan at "
            "https://console.groq.com/settings/billing\n"
            f"Last error: {last_error}"
        )


# Singleton instance used by all services
_llm_instance = None


def get_llm_smart() -> RateLimitAwareLLM:
    """
    Returns a singleton RateLimitAwareLLM.
    Import and call this instead of get_llm() in services that need
    resilience against daily quota exhaustion.
    """
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = RateLimitAwareLLM()
    return _llm_instance