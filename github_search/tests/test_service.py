import json

import pytest
from django.core.cache import cache

from github_search.choices import SearchType
from github_search.services import GitHubSearchService, _cache_key
from github_search.tests.fixtures import GITHUB_USER_ITEM, make_github_response


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def service():
    return GitHubSearchService()


@pytest.fixture
def github_response():
    return make_github_response([GITHUB_USER_ITEM])


@pytest.mark.django_db
def test_search_calls_client_on_cache_miss(service, github_response, mocker):
    mock_search = mocker.patch("github_search.services.github_client.search", return_value=github_response)

    result = service.search(SearchType.USERS, "octocat")

    mock_search.assert_called_once_with(search_type=SearchType.USERS, query="octocat", per_page=10, page=1)
    assert result == github_response


@pytest.mark.django_db
def test_search_stores_result_in_cache(service, github_response, mocker):
    mocker.patch("github_search.services.github_client.search", return_value=github_response)

    service.search(SearchType.USERS, "octocat")

    key = _cache_key(SearchType.USERS, "octocat", 10, 1)
    cached = cache.get(key)
    assert cached is not None
    assert json.loads(cached) == github_response


@pytest.mark.django_db
def test_search_returns_from_cache_on_hit(service, github_response, mocker):
    mock_search = mocker.patch("github_search.services.github_client.search", return_value=github_response)

    service.search(SearchType.USERS, "octocat")
    service.search(SearchType.USERS, "octocat")

    mock_search.assert_called_once()


@pytest.mark.django_db
def test_cache_key_differs_by_params(service, mocker):
    mocker.patch("github_search.services.github_client.search", return_value=make_github_response([]))

    service.search(SearchType.USERS, "octocat", per_page=10, page=1)
    service.search(SearchType.USERS, "octocat", per_page=10, page=2)
    service.search(SearchType.REPOSITORIES, "octocat", per_page=10, page=1)

    k1 = _cache_key(SearchType.USERS, "octocat", 10, 1)
    k2 = _cache_key(SearchType.USERS, "octocat", 10, 2)
    k3 = _cache_key(SearchType.REPOSITORIES, "octocat", 10, 1)
    assert len({k1, k2, k3}) == 3
