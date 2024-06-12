from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.forms import ArticleManagerForm
from blog.models import Article
from blog.services import get_articles_from_cache


class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleManagerForm
    success_url = reverse_lazy("blog:articles")


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleManagerForm
    permission_required = "article.change_article"
    success_url = reverse_lazy("blog:articles")

    def get_success_url(self):
        return reverse("blog:article_detail", args=[self.kwargs.get("pk")])


class ArticleDeleteView(PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = "article.delete_article"
    success_url = reverse_lazy("blog:articles")


class ArticleListView(ListView):
    model = Article
    template_name = "blog/articles_list.html"

    def get_queryset(self):
        return get_articles_from_cache()


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object
