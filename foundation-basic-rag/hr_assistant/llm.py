""" Setup the LLM model for the HR assistant. """

from .gateway import get_gateway_llm
from .logger import get_logger

logger = get_logger(__name__)

def get_llm():
    """Return the Groq chat model based on the configuration settings."""
    logger.info(f"Initializing LLM model through Portkey gateway.")
    return get_gateway_llm()