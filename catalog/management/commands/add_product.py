from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()
        category, _ = Category.objects.get_or_create(
            category_name="Телефоны", description="Мобильные телефоны"
        )
        products = [
            {
                "product_name": "Samsung Galaxy S25",
                "description": "Топовая модель S-серии",
                "photo": "",
                "category_name": category,
                "product_cost": 50000.00,
            },
            {
                "product_name": "Iphone 16 Pro",
                "description": "Топовая модель 16-серии",
                "photo": "",
                "category_name": category,
                "product_cost": 100000.00,
            },
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added product: {product.product_name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Product already exists: {product.product_name}"
                    )
                )
