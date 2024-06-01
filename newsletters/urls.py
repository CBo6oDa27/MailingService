from django.urls import path
from django.views.decorators.cache import never_cache

from newsletters.views import (ClientCreateView, ClientDeleteView,
                               ClientDetailView, ClientListView,
                               ClientUpdateView, IndexPageView,
                               MessageCreateView, MessageDeleteView,
                               MessageDetailView, MessageListView,
                               MessageUpdateView, NewsletterCreateView,
                               NewsletterDeleteView, NewsletterDetailView,
                               NewsletterListView, NewsletterUpdateView, index)

urlpatterns = [
    path("", never_cache(IndexPageView.as_view()), name="homepage"),
    path("", index),
    path("newsletter/", NewsletterListView.as_view(), name="newsletter_list"),
    path(
        "newsletter/<int:pk>/", NewsletterDetailView.as_view(), name="newsletter_detail"
    ),
    path(
        "newsletter/create/", NewsletterCreateView.as_view(), name="newsletter_create"
    ),
    path(
        "newsletter/update/<int:pk>/",
        NewsletterUpdateView.as_view(),
        name="newsletter_update",
    ),
    path(
        "newsletter/delete/<int:pk>/",
        NewsletterDeleteView.as_view(),
        name="newsletter_delete",
    ),
    path("client/", ClientListView.as_view(), name="client_list"),
    path("client/<int:pk>/", ClientDetailView.as_view(), name="client_detail"),
    path("client/create/", ClientCreateView.as_view(), name="client_create"),
    path("client/update/<int:pk>/", ClientUpdateView.as_view(), name="client_update"),
    path("client/delete/<int:pk>/", ClientDeleteView.as_view(), name="client_delete"),
    path("message/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", MessageDetailView.as_view(), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path(
        "message/update/<int:pk>/", MessageUpdateView.as_view(), name="message_update"
    ),
    path(
        "message/delete/<int:pk>/", MessageDeleteView.as_view(), name="message_delete"
    ),
]
