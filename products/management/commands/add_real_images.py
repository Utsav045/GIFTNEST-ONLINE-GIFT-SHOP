import os
import shutil
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from products.models import Product, ProductImage
import random

class Command(BaseCommand):
    help = 'Add real images from static/images to products'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No products found. Please add some products first.')
            )
            return

        # Find available images in the static/images directory
        static_root = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.BASE_DIR / 'static'
        images_static_path = os.path.join(static_root, 'images')
        
        # Get all image files from the static/images directory
        image_files = []
        for root, dirs, files in os.walk(images_static_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    image_files.append(os.path.join(root, file))
        
        if not image_files:
            self.stdout.write(
                self.style.WARNING('No image files found in static/images directory.')
            )
            return

        self.stdout.write(
            f'Found {len(image_files)} image files to use for products.'
        )

        # Ensure media/products directory exists
        media_root = settings.MEDIA_ROOT
        media_products_path = os.path.join(media_root, 'products')
        os.makedirs(media_products_path, exist_ok=True)

        # For each product, add images
        for i, product in enumerate(products):
            self.stdout.write(
                f'Processing product: {product.name}'
            )
            
            # Select a random image for the main image if it doesn't have one
            if not product.image:
                # Get a random image file
                random_image_path = random.choice(image_files)
                
                # Copy the image to media directory
                image_filename = os.path.basename(random_image_path)
                media_image_path = os.path.join(media_products_path, image_filename)
                
                # Copy file from static to media
                shutil.copy2(random_image_path, media_image_path)
                
                # Set the relative path for the product image
                relative_path = os.path.join('products', image_filename)
                product.image.name = relative_path
                product.save()
                self.stdout.write(
                    f'  Set main image to: {image_filename}'
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
                    # Get a random image file (make sure it's different from main image)
                    random_image_path = random.choice(image_files)
                    image_filename = os.path.basename(random_image_path)
                    
                    # Create a unique filename for additional images
                    unique_filename = f"{product.id}_{j}_{image_filename}"
                    media_image_path = os.path.join(media_products_path, unique_filename)
                    
                    # Copy file from static to media
                    shutil.copy2(random_image_path, media_image_path)
                    
                    # Create ProductImage instance
                    product_image = ProductImage(
                        product=product,
                        alt_text=f'{product.name} - View {j+1}'
                    )
                    product_image.image.name = os.path.join('products', unique_filename)
                    product_image.save()
                    
                    self.stdout.write(
                        f'    Added additional image: {unique_filename}'
                    )
            else:
                self.stdout.write(
                    f'  Product already has {product.images.count()} additional images'
                )

        self.stdout.write(
            self.style.SUCCESS('Finished adding real images to products!')
        )