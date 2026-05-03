from django.conf import settings
import requests

from github_search.choices import SearchType


class GitHubClient:
    BASE_URL = "https://api.github.com/search"
    TIMEOUT = 5

    def __init__(self, token: str | None = None):
        self.token = token or getattr(settings, "GITHUB_TOKEN", None)

    def _get_headers(self) -> dict:
        headers = {
            "Accept": "application/vnd.github+json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _build_url(self, search_type: str) -> str:
        if search_type not in [choice[0] for choice in SearchType.choices]:
            raise ValueError(f"Unsupported search type: {search_type}")
        return f"{self.BASE_URL}/{search_type}"

    def search(self, search_type: SearchType, query: str, per_page: int = 10) -> dict:
        """
        Generic search method.
        """
        url = self._build_url(search_type)

        params = {
            "q": query,
            "per_page": per_page,
        }

        response = requests.get(
            url,
            headers=self._get_headers(),
            params=params,
            timeout=self.TIMEOUT,
        )

        if response.status_code != 200:
            raise Exception(
                f"GitHub API error: {response.status_code} - {response.text}"
            )

        return response.json()

    def search_users(self, query: str) -> dict:
        return self.search(SearchType.USERS, query)

    def search_repositories(self, query: str) -> dict:
        return self.search(SearchType.REPOSITORIES, query)

    def search_issues(self, query: str) -> dict:
        return self.search(SearchType.ISSUES, query)
