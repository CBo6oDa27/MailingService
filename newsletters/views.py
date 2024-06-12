import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from blog.models import Article
from newsletters.forms import (ClientForm, MessageForm,
                               NewsletterForm, NewsletterManagerForm)
from newsletters.models import Client, Message, Newsletter


def index(request):
    return render(request, "newsletters/index.html")


class NewsletterListView(ListView):
    """Просмотр списка рассылок"""

    model = Newsletter


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей рассылки"""

    model = Newsletter


class NewsletterCreateView(LoginRequiredMixin, CreateView):
    """Создание новыой рассылки"""

    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("newsletter:newsletter_list")

    def form_valid(self, form):
        newsletter = form.save()
        user = self.request.user
        newsletter.owner = user
        newsletter.mail_datetime = timezone.now()
        newsletter.start_date = timezone.now()
        newsletter.save()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование данных рассылки"""

    model = Newsletter
    form_class = NewsletterForm
    success_url = reverse_lazy("newsletter:newsletter_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return NewsletterForm
        if user.has_perm("newsletters.can_manage_newsletter_status"):
            return NewsletterManagerForm
        raise PermissionDenied


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление рассылки"""

    model = Newsletter
    success_url = reverse_lazy("newsletter:newsletter_list")

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class ClientListView(LoginRequiredMixin, ListView):
    """Просмотр списка клиентов"""

    model = Client

    def get_queryset(self):
        user = self.request.user
        return Client.objects.filter(owner=user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Просмотр одного клиента"""

    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("newsletter:client_list")

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование данных клиента"""

    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("newsletter:client_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        raise PermissionDenied


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление клиента"""

    model = Client
    success_url = reverse_lazy("newsletter:client_list")

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class MessageListView(ListView):
    """Просмотр списка сообщений"""

    model = Message

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(owner=user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    """Просмотр деталей сообщения"""

    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    """Создание сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("newsletter:message_list")

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование сообщения"""

    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("newsletter:message_list")

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление сообщения"""

    model = Message
    success_url = reverse_lazy("newsletter:message_list")

    def get_context_data(self, **kwargs):
        """
        Права доступа владельца.
        """
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        if user == self.object.owner:
            return context_data
        raise PermissionDenied


class IndexPageView(TemplateView):
    template_name = "newsletters/index.html"

    def get_context_data(self, **kwargs):
        is_active = Newsletter.objects.filter(mail_active=True).count()
        count = Newsletter.objects.count()
        unique = Client.objects.distinct("email").count()
        article_list = list(Article.objects.all())
        random.shuffle(article_list)
        random_article_list = article_list[:3]
        context_data = {
            "count": count,
            "is_active": is_active,
            "unique": unique,
            "random_article_list": random_article_list,
        }
        return context_data
