from .config import settings
from .agent import create_hr_agent
from .llm import get_llm
from .document_loader import load_document
from .splitter import split_documents
from .tools import create_search_tool
from .vector_store import (
    build_vector_store,
    get_retriever,
    load_vector_store,
    save_vector_store,
    vector_store_exists
)
from .logger import get_logger

logger = get_logger(__name__)

def build_vector_store_for_documents(file_path = settings.DATA_FILE_PATH):
    """Build a vector store for the documents loaded from the specified file path."""
    if vector_store_exists():
        logger.info("Vector store already exists. Loading from disk...")
        return load_vector_store()
    logger.info("Vector store does not exist. Building a new one...")
    documents = load_document(file_path)
    split_docs = split_documents(documents)
    logger.info(f"Number of document chunks: {len(split_docs)}")
    vector_store = build_vector_store(split_docs)
    save_vector_store(vector_store)
    logger.info("Vector store built and saved to disk for the next time...")
    return vector_store

def build_hr_assistant(file_path = settings.DATA_FILE_PATH):
    """Build the HR assistant by creating the vector store and the agent."""
    logger.info("Building HR assistant...")
    vector_store = build_vector_store_for_documents(file_path)
    retriever = get_retriever(vector_store)
    llm = get_llm()
    search_tool = create_search_tool(retriever)
    agent = create_hr_agent(llm, [search_tool])
    logger.info("HR assistant built successfully and ready to answer questions.")
    return agent

def ask_assistant(agent, question: str) -> str:
    """Ask the HR assistant a question and return the answer."""
    logger.info(f"User Question: {question}")
    response = agent.invoke({"messages": [{"role": "user", "content": question}]})
    answer = response["messages"][-1].content
    logger.info(f"Assistant Response: {answer}")
    return answer