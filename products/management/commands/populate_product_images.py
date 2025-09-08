import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Product, ProductImage
import random

class Command(BaseCommand):
    help = 'Populate products with sample images'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No products found. Please add some products first.')
            )
            return

        # Find available images in the media directory
        media_root = settings.MEDIA_ROOT
        products_media_path = os.path.join(media_root, 'products')
        
        # Get all image files from the products directory
        image_files = []
        for root, dirs, files in os.walk(products_media_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_files.append(os.path.join(root, file))
        
        if not image_files:
            self.stdout.write(
                self.style.WARNING('No image files found in media/products directory.')
            )
            return

        self.stdout.write(
            f'Found {len(image_files)} image files to use for products.'
        )

        # For each product, add images
        for i, product in enumerate(products):
            self.stdout.write(
                f'Processing product: {product.name}'
            )
            
            # Select a random image for the main image if it doesn't have one
            if not product.image:
                random_image = random.choice(image_files)
                # For demo purposes, we'll just note which image we would use
                self.stdout.write(
                    f'  Would set main image to: {os.path.basename(random_image)}'
                )
            else:
                self.stdout.write(
                    f'  Product already has main image: {os.path.basename(product.image.name)}'
                )
            
            # Add additional images if product doesn't have any
            if product.images.count() == 0:
                # Add 2-3 additional images
                num_additional = random.randint(2, 3)
                self.stdout.write(
                    f'  Adding {num_additional} additional images'
                )
                
                for j in range(num_additional):
                    random_image = random.choice(image_files)
                    # For demo purposes, we'll just note which images we would use
                    self.stdout.write(
                        f'    Would add additional image: {os.path.basename(random_image)}'
                    )
            else:
                self.stdout.write(
                    f'  Product already has {product.images.count()} additional images'
                )

        self.stdout.write(
            self.style.SUCCESS('Finished populating product images (demo only)')
        )
        self.stdout.write(
            self.style.WARNING('This was a demo. To actually add images, you would need to:')
        )
        self.stdout.write(
            '1. Upload images through the admin interface at /admin/'
        )
        self.stdout.write(
            '2. Or upload images through the web interface when adding/editing products'
        )