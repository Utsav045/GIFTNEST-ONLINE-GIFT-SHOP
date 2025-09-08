import os
import random
from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = 'Rename products based on their associated image filenames with descriptive names'

    def handle(self, *args, **options):
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(
                self.style.WARNING('No products found.')
            )
            return

        # Define some descriptive product name templates
        gift_categories = [
            "Luxury {}", "Premium {}", "Handcrafted {}", "Artisan {}", 
            "Elegant {}", "Exclusive {}", "Designer {}", "Custom {}",
            "Unique {}", "Special {}", "Vintage {}", "Modern {}"
        ]
        
        product_types = [
            "Gift Set", "Collection", "Box", "Basket", "Hamper", 
            "Package", "Bundle", "Assortment", "Kit", "Pack"
        ]
        
        item_types = [
            "Jewelry", "Watch", "Perfume", "Candle", "Soap", 
            "Tea", "Coffee", "Chocolate", "Wine", "Flowers",
            "Frame", "Clock", "Vase", "Book", "Game", 
            "Blanket", "Pillow", "Towel", "Bath Set", "Skincare Set",
            "Stationery Set", "Tool Kit", "Plant Pot", "Photo Album", 
            "Wallet", "Scarf", "Gloves", "Hat", "Sunglasses"
        ]

        # For each product, rename it with a more descriptive name
        for i, product in enumerate(products):
            if product.image:
                # Get the image filename without extension
                image_filename = os.path.basename(product.image.name)
                name_without_extension = os.path.splitext(image_filename)[0]
                
                # Generate a more descriptive product name
                if name_without_extension == 'GIFTNEST':
                    new_name = "GiftNest Premium Collection"
                else:
                    # Create a random but descriptive product name
                    category = random.choice(gift_categories)
                    product_type = random.choice(product_types)
                    item_type = random.choice(item_types)
                    new_name = f"{category.format(item_type)} {product_type}"
                
                # Ensure name uniqueness by adding a number if needed
                original_name = new_name
                counter = 1
                while Product.objects.filter(name=new_name).exists() and new_name != product.name:
                    new_name = f"{original_name} #{counter}"
                    counter += 1
                
                # Update the product name
                old_name = product.name
                product.name = new_name
                product.save()
                
                self.stdout.write(
                    f'Renamed "{old_name}" to "{new_name}"'
                )
            else:
                self.stdout.write(
                    f'Product "{product.name}" has no image assigned'
                )

        self.stdout.write(
            self.style.SUCCESS('Finished renaming products with descriptive names!')
        )