from langchain.tools import tool
from .vector_store import get_retriever, load_vector_store
from .logger import get_logger

logger = get_logger(__name__)

def create_search_tool(retriever):
    """
    Create a search tool for the HR policy document.
    This tool is used by the RAG agent to retrieve information from the HR policy document.
    """
    @tool
    def search_hr_policy(question: str) -> str:
        """
        Search the HR policy document for relevant information based on the query.
        This tool is used by the RAG agent to retrieve information from the HR policy document.
        """
        logger.info(f"Searching HR policy for question: {question}")
        # Use the retriever to get relevant chunks from the vector store
        relevant_chunks = retriever.invoke(question) 
        logger.info(f"Found {len(relevant_chunks)} relevant chunks for the question.")
        # Combine the content of the relevant chunks into a single string
        combined_content = "\n".join([chunk.page_content for chunk in relevant_chunks]) 
        return combined_content
    
    return search_hr_policy

