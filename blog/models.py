from django.db import models

NULLABLE = {"null": True, "blank": True}


class Article(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Заголовок", help_text="Введите название статьи"
    )
    content = models.TextField(
        verbose_name="Содержимое", help_text="Введите содержимое статьи"
    )
    preview = models.ImageField(
        upload_to="articles/", verbose_name="Изображение", **NULLABLE
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    view_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
