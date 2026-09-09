from langchain.agents import create_agent
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def create_hr_agent(llm , tools):
    """Return a RAG agent for the HR assistant 
    that can call tools and provide answers."""
    logger.info(f"Creating HR agent with {llm} and {tools}.")
    agent = create_agent(model=llm, tools=tools, system_prompt=settings.SYSTEM_PROMPT)
    logger.info("HR agent created successfully.")
    return agent
