from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED

def get_product_from_cache():
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "products_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products

class ProductService:
    """Сервисный класс для работы с продуктами с кэшированием по ID категории."""

    @staticmethod
    def get_products_by_category(category_id, include_unpublished=False, ttl=300):
        """
        Возвращает список продуктов в указанной категории по ID с кэшированием.

        """
        cache_key = f"category_{category_id}"
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return cached_data

        try:
            category = Category.objects.get(id=category_id)
            all_products = get_product_from_cache()
            products = all_products.filter(category_name=category)
            products = products.select_related('category_name', 'owner')

            data = {
                'category': category,
                'products': list(products),
                'product_count': products.count()
            }

            cache.set(cache_key, data, timeout=ttl)
            return data

        except Category.DoesNotExist:
            return {
                'category': None,
                'products': [],
                'product_count': 0
            }

    @staticmethod
    def invalidate_category_cache(category_id):
        """Очищает кэш для конкретной категории."""
        cache.delete(f"category_{category_id}")