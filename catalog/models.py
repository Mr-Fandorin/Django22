from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=200, verbose_name="Название категории")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание категории"
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["category_name"]


class Product(models.Model):
    product_name = models.CharField(max_length=150, verbose_name="Название продукта")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание продукта"
    )
    photo = models.ImageField(
        upload_to="product/photo", null=True, blank=True, verbose_name="Изображение"
    )
    category_name = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name="Название категории",
        related_name="product_name",
        null=True,
        blank=True,
    )
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    views_counter = models.PositiveIntegerField(
        verbose_name = "Счетчик просмотров",
        help_text = "Укажите количество просмотров",
        db_default=0,
    )


    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["product_name", "category_name", "product_cost"]
