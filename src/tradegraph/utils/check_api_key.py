import logging
import os

logger = logging.getLogger(__name__)


def check_api_key(
    llm_api_key_check: bool = False,
    devin_api_key_check: bool = False,
    fire_crawl_api_key_check: bool = False,
    github_personal_access_token_check: bool = False,
) -> None:
    missing_keys = []

    if llm_api_key_check:
        openai_key = os.getenv("OPENAI_API_KEY")
        vertex_key = os.getenv("VERTEX_AI_API_KEY")
        if not openai_key and not vertex_key:
            missing_keys.append(
                {
                    "name": "OpenAI API Key or Vertex AI API Key",
                    "env": "OPENAI_API_KEY or VERTEX_AI_API_KEY",
                    "url": (
                        "OpenAI: https://platform.openai.com/settings/organization/api-keys\n"
                        "Vertex AI: https://aistudio.google.com/apikey"
                    ),
                }
            )

    if devin_api_key_check:
        if not os.getenv("DEVIN_API_KEY"):
            missing_keys.append(
                {
                    "name": "Devin API Key",
                    "env": "DEVIN_API_KEY",
                    "url": "https://app.devin.ai/settings/api-keys",
                }
            )

    if fire_crawl_api_key_check:
        if not os.getenv("FIRE_CRAWL_API_KEY"):
            missing_keys.append(
                {
                    "name": "Firecrawl API Key",
                    "env": "FIRE_CRAWL_API_KEY",
                    "url": "https://www.firecrawl.dev/app/api-keys",
                }
            )

    if github_personal_access_token_check:
        if not os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"):
            missing_keys.append(
                {
                    "name": "GitHub Personal Access Token",
                    "env": "GITHUB_PERSONAL_ACCESS_TOKEN",
                    "url": "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token",
                }
            )

    if missing_keys:
        message_lines = ["The following API keys are not set:"]
        for key in missing_keys:
            message_lines.append(
                f"- {key['name']} (Environment variable: {key['env']})\n  Get it here: {key['url']}"
            )
        full_message = "\n".join(message_lines)
        logger.error(full_message)
        raise RuntimeError("Missing required API keys. Aborting process.")
