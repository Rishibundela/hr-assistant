"""
Evaluation utilities for the HR Assistant.
"""

from typing import Any, Callable
from langchain_openai import ChatOpenAI
from langsmith import Client
from langsmith.evaluation import evaluate
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT, RAG_GROUNDEDNESS_PROMPT
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

from .config import settings
from .logger import get_logger
from .pipeline import ask_assistant, build_hr_assistant
from .vector_store import get_retriever, load_vector_store

logger = get_logger(__name__)

DATASET_NAME = "hr_policy_qna"

TEST_CASES = [
    {"question": "How many days of paid annual leave do I get per year?", "answer": "20 days"},
    {"question": "How many days of unused annual leave can be carried forward?", "answer": "Up to 5 days"},
    {"question": "How many paid sick days do I get per year?", "answer": "10 days"},
    {"question": "How many days per week can I work from home?", "answer": "Up to 2 days, with manager approval"},
    {"question": "How long is the probation period?", "answer": "3 months"},
    {"question": "What is the notice period during probation?", "answer": "15 days"},
    {"question": "What is the standard notice period for resignation?", "answer": "30 days"},
    {"question": "Within how many days must reimbursement claims be submitted?", "answer": "30 days of the expense"},
    {"question": "How many public holidays does the company observe each year?", "answer": "12"},
    {"question": "Within how many days is full and final settlement processed after the last working day?", "answer": "45 days"},
]

JUDGE_MODEL_NAME = "openai/gpt-oss-20b"


def _get_judge_llm() -> ChatOpenAI:
    """Return a ChatOpenAI model that uses the Portkey gateway for LLM calls."""
    logger.info(f"Routing Judge LLM calls through Portkey gateway with model {JUDGE_MODEL_NAME}.")
    headers = createHeaders(
        api_key=settings.PORTKEY_API_KEY, 
        config="pc-hrpoli-1275d7"
    )
    return ChatOpenAI(
        api_key="portkey", # dummy value, actual key is in headers
        model=JUDGE_MODEL_NAME,
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers,
    )


def _get_or_create_dataset(client: Client):
    """Create or retrieve the dataset for HR policy evaluation."""
    if client.has_dataset(dataset_name=DATASET_NAME):
        dataset = client.read_dataset(dataset_name=DATASET_NAME)
        # Verify it actually contains examples
        if any(client.list_examples(dataset_id=dataset.id, limit=1)):
            logger.info(f"Dataset '{DATASET_NAME}' already exists with examples. Retrieving it.")
            return dataset
        logger.warning(f"Dataset '{DATASET_NAME}' exists but has 0 examples. Deleting and recreating...")
        client.delete_dataset(dataset_id=dataset.id)

    logger.info(f"Creating new dataset '{DATASET_NAME}' with {len(TEST_CASES)} test cases...")
    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description="Evaluation dataset for HR policy assistant.",
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"question": test_case["question"]},
                "outputs": {"answer": test_case["answer"]},
            }
            for test_case in TEST_CASES
        ],
    )
    logger.info(f"Dataset '{DATASET_NAME}' created successfully with {len(TEST_CASES)} test cases.")
    return dataset


def run_evalution():
    """Upload the evaluation dataset and run correctness and groundedness evaluation for the HR assistant."""
    client = Client()
    dataset = _get_or_create_dataset(client)

    logger.info("Building the HR assistant for evaluation...")
    agent = build_hr_assistant()
    retriever = get_retriever(load_vector_store())

    def target_func(inputs: dict) -> dict:
        """Run one test question through the HR assistant and capture vector context."""
        answer = ask_assistant(agent, inputs["question"])
        chunks = retriever.invoke(inputs["question"])
        context = "\n".join([chunk.page_content for chunk in chunks])
        return {
            "answer": answer,
            "context": context,
        }

    # Initialize evaluator judges
    correctness_evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        feedback_key="correctness",
        judge=_get_judge_llm(),
    )

    groundedness_judge: Callable = create_llm_as_judge(  # type: ignore[assignment]
        prompt=RAG_GROUNDEDNESS_PROMPT,
        feedback_key="groundedness",
        judge=_get_judge_llm(),
    )

    def groundedness_evaluator(
        run: Any = None,
        example: Any = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        """Check that the answer is grounded in the retrieved context, not invented."""
        if not outputs:
            return {"key": "groundedness", "score": 0}

        return groundedness_judge(
            outputs=outputs.get("answer", ""),
            context=outputs.get("context", ""),
        )

    logger.info(f"Starting evaluation against dataset '{DATASET_NAME}' with {len(TEST_CASES)} test cases...")
    return evaluate(
        target_func,
        data=dataset.name,
        evaluators=[
            correctness_evaluator,  # type: ignore[list-item]
            groundedness_evaluator,
        ],
        client=client,
        experiment_prefix="hr-policy-eval",
        description="HR policy assistant correctness + groundedness evaluation",
    )
        