from rest_framework import views
from rest_framework.response import Response

from github_search.clients import github_client
from github_search.serializers import SearchSerializer


class SearchView(views.APIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        results = github_client.search(
            search_type=serializer.validated_data["type"],
            query=serializer.validated_data["text"],
        )
        print(f"{results=}")
        return Response(results)
