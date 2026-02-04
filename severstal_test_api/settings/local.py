from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend', '0.0.0.0']

# CORS settings for frontend development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# =========================
# DATABASE
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'buildhub_dev'),
        'USER': os.getenv('DB_USER', 'developer'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'dev_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# =========================
# FILE STORAGE (MinIO)
# =========================

MINIO_INTERNAL_URL = os.getenv("MINIO_INTERNAL_URL", "http://localhost:9000")
MINIO_PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL", "http://localhost:9000")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "bucket_name": os.getenv('AWS_STORAGE_BUCKET_NAME'),
            "access_key": os.getenv('MINIO_ROOT_USER'),
            "secret_key": os.getenv('MINIO_ROOT_PASSWORD'),
            "endpoint_url": MINIO_INTERNAL_URL,
            "region_name": "us-east-1",
            "signature_version": "s3v4",
            "addressing_style": "path",
            "file_overwrite": False,
            "default_acl": None,
            "querystring_auth": False,
            "location": "",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


