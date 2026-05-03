import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from github_search.clients.github import GitHubAPIError
from github_search.tests.fixtures import GITHUB_ISSUE_ITEM, GITHUB_REPO_ITEM, GITHUB_USER_ITEM, make_github_response


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def search_url():
    return reverse("github_search:search")


@pytest.fixture
def clear_cache_url():
    return reverse("clear-cache")


@pytest.mark.django_db
def test_search_users(api_client, search_url, mocker):
    mocker.patch(
        "github_search.services.github_client.search",
        return_value=make_github_response([GITHUB_USER_ITEM]),
    )

    response = api_client.post(search_url, {"text": "octocat", "type": "users"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_count"] == 1
    assert response.data["items"][0]["login"] == "octocat"


@pytest.mark.django_db
def test_search_repositories(api_client, search_url, mocker):
    mocker.patch(
        "github_search.services.github_client.search",
        return_value=make_github_response([GITHUB_REPO_ITEM]),
    )

    response = api_client.post(search_url, {"text": "django", "type": "repositories"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["items"][0]["full_name"] == "octocat/Hello-World"


@pytest.mark.django_db
def test_search_issues(api_client, search_url, mocker):
    mocker.patch(
        "github_search.services.github_client.search",
        return_value=make_github_response([GITHUB_ISSUE_ITEM]),
    )

    response = api_client.post(search_url, {"text": "bug", "type": "issues"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["items"][0]["number"] == 1347


@pytest.mark.django_db
def test_search_pagination_params(api_client, search_url, mocker):
    mock_search = mocker.patch(
        "github_search.services.github_client.search",
        return_value=make_github_response([]),
    )

    api_client.post(search_url, {"text": "django", "type": "repositories", "per_page": 25, "page": 2}, format="json")

    mock_search.assert_called_once_with(
        search_type="repositories", query="django", per_page=25, page=2
    )


@pytest.mark.django_db
def test_search_invalid_type(api_client, search_url):
    response = api_client.post(search_url, {"text": "octocat", "type": "invalid"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_search_per_page_out_of_range(api_client, search_url):
    response = api_client.post(search_url, {"text": "octocat", "type": "users", "per_page": 200}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_search_github_api_error_returns_502(api_client, search_url, mocker):
    mocker.patch(
        "github_search.services.github_client.search",
        side_effect=GitHubAPIError(503, "Service Unavailable"),
    )

    response = api_client.post(search_url, {"text": "octocat", "type": "users"}, format="json")

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert "detail" in response.data


@pytest.mark.django_db
def test_clear_cache(api_client, clear_cache_url, mocker):
    mocker.patch(
        "github_search.services.github_client.search",
        return_value=make_github_response([GITHUB_USER_ITEM]),
    )
    cache.set("some_key", "some_value")

    response = api_client.post(clear_cache_url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert cache.get("some_key") is None
