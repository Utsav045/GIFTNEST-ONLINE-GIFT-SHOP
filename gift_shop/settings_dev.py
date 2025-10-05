from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# Use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email Backend
# Use console backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Debug Toolbar (enable only if installed)
try:
    import debug_toolbar  # noqa: F401
except Exception:
    # django-debug-toolbar is optional for local development; if it's not
    # installed we simply don't add it so tests and CI won't fail.
    pass
else:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']

# Stripe Settings
STRIPE_PUBLIC_KEY = 'your_test_public_key'
STRIPE_SECRET_KEY = 'your_test_secret_key'
STRIPE_WEBHOOK_SECRET = 'your_test_webhook_secret'
