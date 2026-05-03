from rest_framework import serializers

from github_search.choices import SearchType


class SearchSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255, allow_blank=True, trim_whitespace=True)
    type = serializers.ChoiceField(choices=SearchType.choices)
    per_page = serializers.IntegerField(default=10, min_value=1, max_value=100)
    page = serializers.IntegerField(default=1, min_value=1)


class UserItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    login = serializers.CharField()
    avatar_url = serializers.URLField()
    html_url = serializers.URLField()
    type = serializers.CharField()


class OwnerSerializer(serializers.Serializer):
    login = serializers.CharField()
    avatar_url = serializers.URLField()


class RepositoryItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    full_name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    html_url = serializers.URLField()
    stargazers_count = serializers.IntegerField()
    forks_count = serializers.IntegerField()
    language = serializers.CharField(allow_null=True)
    owner = OwnerSerializer()


class IssueItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.IntegerField()
    title = serializers.CharField()
    state = serializers.CharField()
    html_url = serializers.URLField()
    body = serializers.CharField(allow_null=True)
    user = UserItemSerializer()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


ITEM_SERIALIZERS = {
    SearchType.USERS: UserItemSerializer,
    SearchType.REPOSITORIES: RepositoryItemSerializer,
    SearchType.ISSUES: IssueItemSerializer,
}


class SearchResponseSerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    items = serializers.ListField()
