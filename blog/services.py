from django.core.cache import cache

from blog.models import Article
from config.settings import CACHE_ENABLED


def get_articles_from_cache():
    if not CACHE_ENABLED:
        return Article.objects.all()
    key = "articles"
    articles = cache.get(key)
    if articles is not None:
        return articles
    articles = Article.objects.all()
    cache.set(key, articles)
    return articles
