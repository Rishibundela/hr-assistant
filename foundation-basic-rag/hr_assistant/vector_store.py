"""Set up the qdrant vector store for the HR assistant."""
from langchain_qdrant import Qdrant, QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_core.documents import Document
from .embeddings import get_embedding_model
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

_client = QdrantClient(
    url=settings.QDRANT_URL, 
    api_key=settings.QDRANT_API_KEY,
    timeout=60,
    check_compatibility=False,
)

def build_vector_store(chunks: list[Document]):
    """Build the qdrant vector store from the document chunks."""
    embedding_model = get_embedding_model()
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding_model,
        api_key=settings.QDRANT_API_KEY,
        url = settings.QDRANT_URL,
        collection_name=settings.QDRANT_COLLECTION_NAME,
    )
    logger.info(f"Vector store built with {len(chunks)} chunks and stored in Qdrant collection '{settings.QDRANT_COLLECTION_NAME}'.")
    return vector_store

# Save the vector store to disk

# load the vector store from disk
def load_vector_store():
    """Load the  vector store from disk."""
    embedding_model = get_embedding_model()
    logger.info(f"Loading vector store from existing collection")
    return  QdrantVectorStore.from_existing_collection(
    collection_name=settings.QDRANT_COLLECTION_NAME,
    embedding=embedding_model,
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)

def vector_store_exists():
    """Check if the qdrant vector store exists on cloud"""
    logger.info(f"Checking if vector store exists")
    return _client.collection_exists(collection_name=settings.QDRANT_COLLECTION_NAME)

def get_retriever(vector_store, k=settings.TOP_K):
    """Turns the vector store into a retriever that returns the top k matching chunks."""
    logger.info(f"Creating retriever with top {k} matches.")
    return vector_store.as_retriever(search_kwargs={"k": k})