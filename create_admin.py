import os
import django
from django.contrib.auth import get_user_model

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gift_shop.settings')
django.setup()

# Create superuser
User = get_user_model()

# Check if superuser already exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created successfully with password 'admin123'")
else:
    print("Superuser 'admin' already exists")