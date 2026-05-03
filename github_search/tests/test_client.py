import pytest

from github_search.choices import SearchType
from github_search.clients.github import GitHubAPIError, GitHubClient
from github_search.tests.fixtures import GITHUB_USER_ITEM, make_github_response


@pytest.fixture
def client():
    return GitHubClient(token="test-token")


def test_build_url(client):
    assert client._build_url(SearchType.USERS) == "https://api.github.com/search/users"
    assert client._build_url(SearchType.REPOSITORIES) == "https://api.github.com/search/repositories"
    assert client._build_url(SearchType.ISSUES) == "https://api.github.com/search/issues"


def test_build_url_invalid_type(client):
    with pytest.raises(ValueError, match="Unsupported search type"):
        client._build_url("invalid")


def test_get_headers_with_token(client):
    headers = client._get_headers()
    assert headers["Authorization"] == "Bearer test-token"
    assert headers["Accept"] == "application/vnd.github+json"


def test_get_headers_without_token():
    c = GitHubClient(token=None)
    c.token = None
    headers = c._get_headers()
    assert "Authorization" not in headers


def test_search_success(client, mocker):
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.json.return_value = make_github_response([GITHUB_USER_ITEM])
    mocker.patch("github_search.clients.github.requests.get", return_value=mock_response)

    result = client.search(SearchType.USERS, "octocat", per_page=10, page=1)

    assert result["total_count"] == 1
    assert result["items"][0]["login"] == "octocat"


def test_search_passes_correct_params(client, mocker):
    mock_response = mocker.Mock()
    mock_response.ok = True
    mock_response.json.return_value = make_github_response([])
    mock_get = mocker.patch("github_search.clients.github.requests.get", return_value=mock_response)

    client.search(SearchType.REPOSITORIES, "django", per_page=25, page=3)

    _, kwargs = mock_get.call_args
    assert kwargs["params"] == {"q": "django", "per_page": 25, "page": 3}


def test_search_raises_on_error(client, mocker):
    mock_response = mocker.Mock()
    mock_response.ok = False
    mock_response.status_code = 422
    mock_response.text = "Validation Failed"
    mocker.patch("github_search.clients.github.requests.get", return_value=mock_response)

    with pytest.raises(GitHubAPIError) as exc_info:
        client.search(SearchType.USERS, "octocat")

    assert exc_info.value.status_code == 422
