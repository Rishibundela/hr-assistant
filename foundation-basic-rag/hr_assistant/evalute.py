from .evalution import run_evalution
from .logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Starting evaluation of the HR assistant...")
    results = run_evalution()
    logger.info("Evaluation completed successfully. Now open the langsmith and see the experiments and results.")

if __name__ == "__main__":
    main()
    

