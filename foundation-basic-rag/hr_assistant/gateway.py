import json
from langchain_openai import ChatOpenAI
from portkey_ai import createHeaders, PORTKEY_GATEWAY_URL

from .config import settings
from .logger import get_logger

logger = get_logger(__name__)

PRIMARY_TARGET_MODEL = {"provider": "@hrpolicy",
                        "override_params": {"model": settings.LLM_MODEL_NAME}}
FALLBACK_TARGET_MODEL = {"provider": "@hrpolicybackup",
                         "override_params": {"model": settings.FALLBACK_LLM_MODEL_NAME}}

# Gateway features
# - Fallback
# - Load Balancing
# - Caching
# - Rate Limiting
# - Routing based on model capabilities
# - Retry and timeout handling

# config
GATEWAY_CONFIG = {
	"strategy": {
		"mode": "fallback"
	},
	"retry": {
		"attempts": 3,
		"on_status_codes": [
			429
		]
	},
	"cache": {
		"mode": "simple"
	},
	"targets": [
		{
			"provider": "@hrpolicy",
			"override_params": {
				"model": "openai/gpt-oss-20b"
			}
		},
		{
			"provider": "@hrpolicybackup",
			"override_params": {
				"model": "openai/gpt-oss-120b"
			}
		}
	]
}

def get_gateway_llm() -> ChatOpenAI:
    """Return a ChatOpenAI model that uses the Portkey gateway for LLM calls."""

    logger.info(f"Routing LLM calls through Portkey gateway with primary model {settings.LLM_MODEL_NAME} and fallback model {settings.FALLBACK_LLM_MODEL_NAME}.")

    headers = createHeaders(
        api_key=settings.PORTKEY_API_KEY, 
        config="pc-hrpoli-1275d7"
    )
    return ChatOpenAI(
        api_key="portkey", # dummy value, actual key is in headers
        base_url=PORTKEY_GATEWAY_URL,
        default_headers=headers
    )

