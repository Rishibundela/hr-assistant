"""Set up the vector store for the HR assistant."""
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from .embeddings import get_embedding_model
from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

def build_vector_store(chunks: list[Document]):
    """Build the FAISS vector store from the document chunks."""
    embedding_model = get_embedding_model()
    vector_store = FAISS.from_documents(chunks, embedding_model)
    logger.info(f"Vector store built with {len(chunks)} chunks.")
    return vector_store

# Save the vector store to disk
def save_vector_store(vector_store, file_path=settings.VECTOR_STORE_PATH):
    """Save the FAISS vector store to disk."""
    vector_store.save_local(file_path)
    logger.info(f"Vector store saved to {file_path}")

# load the vector store from disk
def load_vector_store(file_path=settings.VECTOR_STORE_PATH):
    """Load the FAISS vector store from disk."""
    embedding_model = get_embedding_model()
    logger.info(f"Loading vector store from {file_path}")
    return FAISS.load_local(str(file_path), embedding_model, allow_dangerous_deserialization=True)

def vector_store_exists(file_path=settings.VECTOR_STORE_PATH) -> bool:
    """Check if the FAISS vector store exists on disk."""
    logger.info(f"Checking if vector store exists at {file_path}")
    return file_path.exists()

def get_retriever(vector_store, k=settings.TOP_K):
    """Turns the vector store into a retriever that returns the top k matching chunks."""
    logger.info(f"Creating retriever with top {k} matches.")
    return vector_store.as_retriever(search_kwargs={"k": k})


