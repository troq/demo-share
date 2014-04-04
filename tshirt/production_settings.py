DATABASES = {}
# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

STATIC_ROOT = 'staticfiles'

#custom settings
TSHIRT_SHOP_PAGINATION_PER_PAGE = 9
FIREBASE_URL = 'https://troq.firebaseio.com/'

#for django-storages
AWS_STORAGE_BUCKET_NAME = 'troq-test'

#for endless pagination
ENDLESS_PAGINATION_PER_PAGE = 8

