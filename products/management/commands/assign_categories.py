from django.core.management.base import BaseCommand
from django.db.models import Q
from products.models import Product, Category
import random

class Command(BaseCommand):
    help = 'Assigns random categories to existing products'

    def handle(self, *args, **kwargs):
        # Get all products without a category
        products = Product.objects.filter(Q(category__isnull=True))
        categories = list(Category.objects.all())

        if not categories:
            self.stdout.write(
                self.style.ERROR('No categories found. Please run create_categories first.')
            )
            return

        for product in products:
            # Assign a random category
            category = random.choice(categories)
            product.category = category
            product.save()
            self.stdout.write(
                self.style.SUCCESS(f'Assigned category "{category.name}" to product "{product.name}"')
            )
