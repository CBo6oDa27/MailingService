from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from blog.apps import BlogConfig
from blog.views import (ArticleCreateView, ArticleDeleteView,
                        ArticleDetailView, ArticleListView, ArticleUpdateView)

app_name = BlogConfig.name

urlpatterns = [
    path(
        "articles/create/",
        never_cache(ArticleCreateView.as_view()),
        name="create_article",
    ),
    path(
        "articles/update/<int:pk>/",
        never_cache(ArticleUpdateView.as_view()),
        name="update_article",
    ),
    path("articles/", cache_page(60)(ArticleListView.as_view()), name="articles"),
    path(
        "articles/<int:pk>/",
        cache_page(60)(ArticleDetailView.as_view()),
        name="article_detail",
    ),
    path(
        "articles/delete/<int:pk>/", ArticleDeleteView.as_view(), name="delete_article"
    ),
]
