""" Setup the LLM model for the HR assistant. """
from langchain_groq import ChatGroq
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def get_llm():
    """Return the Groq chat model based on the configuration settings."""
    logger.info(f"Initializing LLM model {settings.LLM_MODEL_NAME}")
    return ChatGroq(
        model=settings.LLM_MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0.3
    )