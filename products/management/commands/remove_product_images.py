import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, ProductImage

class Command(BaseCommand):
    help = 'Remove all images from products'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No products found.')
            )
            return

        # Count total images to be removed
        total_main_images = products.exclude(image='').count()
        total_additional_images = sum([p.images.count() for p in products])
        
        self.stdout.write(
            f'Found {total_main_images} main images and {total_additional_images} additional images to remove.'
        )

        # Remove main images from all products
        for product in products:
            if product.image:
                # Get the image path before removing it
                image_path = product.image.path if product.image else None
                
                # Remove the image reference
                product.image = None
                product.save()
                
                # Note: We don't delete the actual file from the filesystem
                # to avoid issues with other products that might use the same image
                self.stdout.write(
                    f'Removed main image from product: {product.name}'
                )
            
            # Remove all additional images
            additional_images = product.images.all()
            if additional_images.exists():
                count = additional_images.count()
                additional_images.delete()
                self.stdout.write(
                    f'Removed {count} additional images from product: {product.name}'
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully removed all images from {products.count()} products!')
        )
        self.stdout.write(
            'Note: Image files were not deleted from the filesystem to preserve shared images.'
        )