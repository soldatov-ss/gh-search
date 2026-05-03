from django.conf import settings
import requests

from github_search.choices import SearchType


class GitHubAPIError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"GitHub API error {status_code}: {message}")


class GitHubClient:
    BASE_URL = "https://api.github.com/search"
    TIMEOUT = 15

    def __init__(self, token: str | None = None):
        self.token = token or getattr(settings, "GITHUB_TOKEN", None)

    def _get_headers(self) -> dict:
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _build_url(self, search_type: str) -> str:
        if search_type not in [choice[0] for choice in SearchType.choices]:
            raise ValueError(f"Unsupported search type: {search_type}")
        return f"{self.BASE_URL}/{search_type}"

    def search(self, search_type: SearchType, query: str, per_page: int = 10, page: int = 1) -> dict:
        url = self._build_url(search_type)

        response = requests.get(
            url,
            headers=self._get_headers(),
            params={"q": query, "per_page": per_page, "page": page},
            timeout=self.TIMEOUT,
        )

        if not response.ok:
            raise GitHubAPIError(response.status_code, response.text)

        return response.json()
