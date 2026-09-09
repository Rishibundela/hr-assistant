"""
Main entry point for the Foundation Basic RAG application.
"""

from hr_assistant.pipeline import build_hr_assistant, ask_assistant
from hr_assistant.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Building the HR assistant...")
    agent = build_hr_assistant()
    logger.info("HR assistant built successfully.")

    while True:
        question = input("\nAsk the HR assistant a question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            logger.info("Exiting the HR assistant. Goodbye!")
            break
        answer = ask_assistant(agent, question)
        logger.info(f"Answer: {answer}")

if __name__ == "__main__":
    main()