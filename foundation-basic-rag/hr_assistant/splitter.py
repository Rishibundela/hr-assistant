"""Set up the text splitter for the HR assistant."""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def split_documents(documents: list[Document]):
    """Split the documents into smaller chunks using RecursiveCharacterTextSplitter."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Splitting documents into chunks of size {settings.CHUNK_SIZE} with overlap {settings.CHUNK_OVERLAP}. Total chunks created: {len(chunks)}")
    return chunks
