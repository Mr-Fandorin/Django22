from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок")
    description = models.TextField(
        null=True, blank=True, verbose_name="Содержимое"
    )
    image = models.ImageField(
        upload_to="blog/image", null=True, blank=True, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    views_counter = models.PositiveIntegerField(
        verbose_name = "Счетчик просмотров",
        help_text = "Укажите количество просмотров",
        db_default=0,
    )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = ["title"]
