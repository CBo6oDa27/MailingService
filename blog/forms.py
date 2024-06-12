from django import forms
from django.forms import BooleanField

from blog.models import Article


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class ArticleManagerForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        exclude = ("created_at", "view_count")
