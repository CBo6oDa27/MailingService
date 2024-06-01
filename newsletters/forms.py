from django import forms

from newsletters.models import Client, Message, Newsletter
from users.forms import StyleFormMixin


class NewsletterForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        exclude = ("mail_status", "owner", "mail_datetime", "start_date")


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"


class NewsletterManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ("mail_active",)
