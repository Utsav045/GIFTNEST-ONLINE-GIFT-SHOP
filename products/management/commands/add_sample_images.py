import os
from django.core.management.base import BaseCommand
from django.core.files import File
from products.models import Product, ProductImage
from django.conf import settings

class Command(BaseCommand):
    help = 'Add sample images to existing products'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No products found. Please add some products first.')
            )
            return

        # For each product, add some sample images if they don't exist
        for product in products:
            # Check if product already has additional images
            if product.images.count() == 0:
                self.stdout.write(
                    f'Adding sample images for product: {product.name}'
                )
                
                # If the product has a main image, we can use it as a reference
                if product.image:
                    # Create 2 additional images for demonstration
                    for i in range(2):
                        product_image = ProductImage(
                            product=product,
                            alt_text=f'{product.name} - View {i+1}'
                        )
                        # We'll just reference the same image file for demonstration
                        # In a real scenario, you would upload different images
                        product_image.image = product.image
                        product_image.save()
                        
                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully added 2 images to {product.name}')
                    )
                else:
                    self.stdout.write(
                        f'Product {product.name} has no main image. Please add a main image first.'
                    )
            else:
                self.stdout.write(
                    f'Product {product.name} already has {product.images.count()} additional images'
                )

        self.stdout.write(
            self.style.SUCCESS('Finished adding sample images to products')
        )