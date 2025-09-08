import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, ProductImage

class Command(BaseCommand):
    help = 'Assign appropriate images to products based on their names'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No products found.')
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

        # Define image assignments based on product names
        image_assignments = {
            'Aromatherapy Gift Set': 'aromatherapy',
            'Artistic Wall Clock': 'clock',
            'Bamboo Tea Set': 'tea',
            'Crystal Wine Glasses': 'wine',
            'Custom Name Necklace': 'necklace',
            'Gourmet Chocolate Collection': 'chocolate',
            'Handcrafted Wooden Box': 'box',
            'Leather Travel Journal': 'journal',
            'Personalized Photo Frame': 'frame',
            'Smart Plant Pot': 'plant',
            'Tushar Singh': 'tushar'
        }

        # For each product, assign appropriate images
        for product in products:
            self.stdout.write(
                f'Processing product: {product.name}'
            )
            
            # Get the keyword for this product
            keyword = image_assignments.get(product.name, '').lower()
            
            # Find images that match the product name or keyword
            matching_images = []
            for image_path in image_files:
                image_name = os.path.basename(image_path).lower()
                # Check if the image name contains the keyword or product name
                if keyword in image_name or product.name.lower().replace(' ', '_') in image_name:
                    matching_images.append(image_path)
            
            # If no matching images found, use any available images
            if not matching_images:
                matching_images = image_files[:3]  # Use first 3 images as fallback
                self.stdout.write(
                    f'  No matching images found, using fallback images'
                )
            else:
                self.stdout.write(
                    f'  Found {len(matching_images)} matching images'
                )
            
            # Assign main image (first matching image or first available image)
            if matching_images:
                main_image_path = matching_images[0]
                relative_path = os.path.relpath(main_image_path, media_root)
                product.image.name = relative_path
                product.save()
                self.stdout.write(
                    f'  Set main image to: {os.path.basename(main_image_path)}'
                )
            
            # Remove existing additional images
            product.images.all().delete()
            
            # Add additional images (up to 3)
            for i, image_path in enumerate(matching_images[1:4]):  # Skip first one (used as main)
                relative_path = os.path.relpath(image_path, media_root)
                
                # Create ProductImage instance
                product_image = ProductImage(
                    product=product,
                    alt_text=f'{product.name} - View {i+1}'
                )
                product_image.image.name = relative_path
                product_image.save()
                
                self.stdout.write(
                    f'    Added additional image: {os.path.basename(image_path)}'
                )

        self.stdout.write(
            self.style.SUCCESS('Finished assigning appropriate images to products!')
        )