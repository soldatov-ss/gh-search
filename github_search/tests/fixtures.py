GITHUB_USER_ITEM = {
    "id": 1,
    "login": "octocat",
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "html_url": "https://github.com/octocat",
    "type": "User",
}

GITHUB_REPO_ITEM = {
    "id": 1296269,
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "description": "This your first repo!",
    "html_url": "https://github.com/octocat/Hello-World",
    "stargazers_count": 80,
    "forks_count": 9,
    "language": "Python",
    "owner": {
        "login": "octocat",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    },
}

GITHUB_ISSUE_ITEM = {
    "id": 1,
    "number": 1347,
    "title": "Found a bug",
    "state": "open",
    "html_url": "https://github.com/octocat/Hello-World/issues/1347",
    "body": "I'm having a problem with this.",
    "user": GITHUB_USER_ITEM,
    "created_at": "2011-04-22T13:33:48Z",
    "updated_at": "2011-04-22T13:33:48Z",
}

def make_github_response(items: list) -> dict:
    return {
        "total_count": len(items),
        "incomplete_results": False,
        "items": items,
    }
