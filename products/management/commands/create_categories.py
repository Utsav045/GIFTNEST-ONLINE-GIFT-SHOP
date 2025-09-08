from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category

class Command(BaseCommand):
    help = 'Creates initial gift categories'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Birthday Gifts',
                'description': 'Perfect gifts for celebrating birthdays of your loved ones',
                'slug': 'birthday-gifts'
            },
            {
                'name': 'Anniversary Gifts',
                'description': 'Celebrate special moments with our anniversary collection',
                'slug': 'anniversary-gifts'
            },
            {
                'name': 'Wedding Gifts',
                'description': 'Beautiful gifts for the special day',
                'slug': 'wedding-gifts'
            },
            {
                'name': 'Valentine Gifts',
                'description': 'Express your love with our romantic collection',
                'slug': 'valentine-gifts'
            },
            {
                'name': 'Corporate Gifts',
                'description': 'Professional gifts for business occasions',
                'slug': 'corporate-gifts'
            },
            {
                'name': 'Personalized Gifts',
                'description': 'Make it special with customized gifts',
                'slug': 'personalized-gifts'
            }
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'slug': category_data['slug']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created category "{category_data["name"]}"')
            )
