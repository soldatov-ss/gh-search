from django.urls import path

from github_search.views import SearchView

app_name = "github_search"

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
]
