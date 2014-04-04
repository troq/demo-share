DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'db',                      # Or path to database file if using sqlite3.
    }
}

ALLOWED_HOSTS = []

STATIC_ROOT = ''

#custom settings
TSHIRT_SHOP_PAGINATION_PER_PAGE = 9
FIREBASE_URL = 'https://troq.firebaseio.com/'

#for django-storages
AWS_STORAGE_BUCKET_NAME = 'troq-test'

#for endless pagination
ENDLESS_PAGINATION_PER_PAGE = 4
