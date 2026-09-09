"""Set up the document loader for the HR assistant."""

from pathlib import Path
from langchain_community.document_loaders import TextLoader
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def load_document(file_path: Path = settings.DATA_FILE_PATH):
    """Load the document from the specified file path and return a list of Document objects."""
    logger.info(f"Loading document from {file_path}")
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    logger.info(f"loaded {len(documents)} documents successfully")
    return documents
