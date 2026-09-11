"All settings for the app live here, in one place"

import os
from dotenv import load_dotenv
from pathlib import Path
from .logger import get_logger

logger = get_logger(__name__)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
# print(f"BASE_DIR: {BASE_DIR}")

class Settings:
    # LLM api key
    GROQ_API_KEY = os.getenv("GROQ_API_KEY","")
    # Emdedding api key
    JINA_API_KEY = os.getenv("JINA_API_KEY")
    # Gateway api key
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY", "")
    # Guard model
    Guard_MODEL_NAME = os.getenv("GUARD_MODEL_NAME", "openai/gpt-oss-safeguard-20b")
    # Data file path
    DATA_FILE_PATH = BASE_DIR / "data" / "basic-rag" / "hr_policy.txt"
    # vector store path
    VECTOR_STORE_PATH = BASE_DIR / "data" / "basic-rag" / "faiss_index"
    # LLM model name
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai/gpt-oss-20b")
    FALLBACK_LLM_MODEL_NAME = os.getenv("FALLBACK_LLM_MODEL_NAME", "openai/gpt oss 120b")
    # Embedding model name
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "jina-embeddings-v2-base-en")

    # cloud vector store settings   
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
    QDRANT_URL = os.getenv("QDRANT_URL", "")
    QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "hr_policy")

    # chunk cofig
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))

    # top retrieval results
    TOP_K = int(os.getenv("TOP_K", 3))

    # system prompt for the RAG agent
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", 
"""You are a friendly HR assistant working for Acme Corp.
You are designed to answer questions about the company's HR policies and procedures.
You should provide accurate and helpful information to the best of your ability.
Always use the search_hr_policy tool to look up facts before answering.
If you don't know the answer to a question or cannot find the information in the search results, you should say so rather than guessing.
""")

    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false")
    LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "hr_policy_assistant")

    @classmethod
    def check_api_keys(cls):
        if not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set in the environment variables.")
        if not cls.JINA_API_KEY:
            raise ValueError("JINA_API_KEY is not set in the environment variables.")
        logger.info("API keys are set.")

    @classmethod
    def check_langsmith_tracing(cls):
        if cls.LANGSMITH_TRACING.lower() == "true":
            logger.info("LangSmith tracing is enabled. Checking for required LangSmith environment variables...")
            if not cls  .LANGSMITH_API_KEY:
                raise ValueError("LANGSMITH_API_KEY is not set in the environment variables.")
            if not cls.LANGSMITH_PROJECT:
                raise ValueError("LANGSMITH_PROJECT is not set in the environment variables.")
            logger.info("LangSmith tracing is enabled for project {cls.LANGSMITH_PROJECT} at {cls.LANGSMITH_ENDPOINT}.")
        else:
            logger.info("LangSmith tracing is disabled. Set LANGSMITH_TRACING=true in the environment variables to enable it.")
            

settings = Settings()

# Check API keys and LangSmith tracing settings at startup
settings.check_api_keys()
settings.check_langsmith_tracing()