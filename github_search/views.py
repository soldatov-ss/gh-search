from django.core.cache import cache
from rest_framework import status, views
from rest_framework.response import Response

from github_search.clients.github import GitHubAPIError
from github_search.serializers import ITEM_SERIALIZERS, SearchResponseSerializer, SearchSerializer
from github_search.services import github_search_service


class SearchView(views.APIView):

    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = github_search_service.search(
                search_type=data["type"],
                query=data["text"],
                per_page=data["per_page"],
                page=data["page"],
            )
        except GitHubAPIError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        item_serializer = ITEM_SERIALIZERS[data["type"]](result["items"], many=True)

        response_serializer = SearchResponseSerializer({
            "total_count": result["total_count"],
            "page": data["page"],
            "per_page": data["per_page"],
            "items": item_serializer.data,
        })
        return Response(response_serializer.data)


class ClearCacheView(views.APIView):
    def post(self, request, *args, **kwargs):
        cache.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
