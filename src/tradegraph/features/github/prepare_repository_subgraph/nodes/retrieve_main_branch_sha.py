from logging import getLogger
from typing import Literal

from tradegraph.services.api_client.github_client import GithubClient

logger = getLogger(__name__)
DEVICETYPE = Literal["cpu", "gpu"]


def retrieve_main_branch_sha(
    github_owner: str,
    repository_name: str,
    client: GithubClient | None = None,
) -> str:
    if client is None:
        client = GithubClient()

    response = client.get_branch(
        github_owner=github_owner,
        repository_name=repository_name,
        branch_name="main",
    )

    if not response or not isinstance(response, dict):
        raise RuntimeError(
            f"Failed to retrieve branch info for 'main' branch of {github_owner}/{repository_name}"
        )

    try:
        sha = response["commit"]["sha"]
    except (TypeError, KeyError):
        msg = f"Invalid response format for 'main' branch of {github_owner}/{repository_name}"
        raise RuntimeError(msg)  # noqa: B904

    if not sha:
        raise RuntimeError(
            f"Empty SHA for 'main' branch of {github_owner}/{repository_name}"
        )
    return sha


if __name__ == "__main__":
    # Example usage
    github_owner = "auto-res2"
    repository_name = "test-branch"
    branch_name = "test"
    output = retrieve_main_branch_sha(github_owner, repository_name)
    print(output)
