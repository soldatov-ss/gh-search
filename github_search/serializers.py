from rest_framework import serializers

from github_search.choices import SearchType


class SearchSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=255, allow_blank=True, trim_whitespace=True)
    type = serializers.ChoiceField(choices=SearchType.choices)
