"""Set up the Jina embeddings model."""
from langchain_community.embeddings import JinaEmbeddings
import requests
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def get_embedding_model():
    """Get the Jina embeddings model."""
    logger.info(f"Initializing embedding model {settings.EMBEDDING_MODEL_NAME}")
    return JinaEmbeddings(
        session=requests.Session(),
        model_name=settings.EMBEDDING_MODEL_NAME,
        jina_api_key= settings.JINA_API_KEY,    
    )
