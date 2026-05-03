import hashlib
import json

from django.core.cache import cache

from github_search.choices import SearchType
from github_search.clients import github_client

CACHE_TTL = 60 * 60 * 2  # 2 hours


def _cache_key(search_type: str, query: str, per_page: int, page: int) -> str:
    raw = f"github_search:{search_type}:{query}:{per_page}:{page}"
    return hashlib.md5(raw.encode()).hexdigest()


class GitHubSearchService:
    def search(self, search_type: SearchType, query: str, per_page: int = 10, page: int = 1) -> dict:
        key = _cache_key(search_type, query, per_page, page)

        cached = cache.get(key)
        if cached is not None:
            return json.loads(cached)

        result = github_client.search(
            search_type=search_type,
            query=query,
            per_page=per_page,
            page=page,
        )

        cache.set(key, json.dumps(result), timeout=CACHE_TTL)
        return result


github_search_service = GitHubSearchService()
