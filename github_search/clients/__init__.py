from django.conf import settings

from .github import GitHubClient

github_client = GitHubClient(
    token=settings.GITHUB_TOKEN,
)

__all__ = [
    "github_client",
]
