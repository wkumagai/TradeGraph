from logging import getLogger

from tradegraph.services.api_client.github_client import GithubClient, GithubClientError

logger = getLogger(__name__)


def check_repository_from_template(
    github_owner: str,
    repository_name: str,
    template_owner: str,
    template_repo: str,
    client: GithubClient | None = None,
) -> bool:
    if client is None:
        client = GithubClient()

    try:
        response = client.get_repository(
            github_owner=github_owner,
            repository_name=repository_name,
        )
    except GithubClientError as e:
        logger.warning(f"Repository does not exist or cannot be accessed: {e}")
        return False

    template_info = response.get("template_repository")
    if not template_info:
        raise ValueError(
            f"Repository '{github_owner}/{repository_name}' exists but is not created from a template."
        )

    is_template_match = (
        template_info.get("owner", {}).get("login") == template_owner
        and template_info.get("name") == template_repo
    )

    if not is_template_match:
        raise ValueError(
            f"Repository '{github_owner}/{repository_name}' is created from a different template "
            f"({template_info.get('owner', {}).get('login')}/{template_info.get('name')}) "
            f"than expected ({template_owner}/{template_repo})."
        )

    return True
