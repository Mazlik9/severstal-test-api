import os
import sys
from .base import *

# =========================
# GENERAL
# =========================
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'backend', '0.0.0.0']

# =========================
# CORS (frontend dev)
# =========================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# =========================
# DATABASE
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'severstal_dev'),
        'USER': os.getenv('DB_USER', 'developer'),
        'PASSWORD': os.getenv('DB_PASSWORD', '0904'),
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
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": os.getenv("MINIO_ROOT_USER", "minioadmin"),
            "secret_key": os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123"),
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME", "severstal-local-media"),
            "endpoint_url": os.getenv("MINIO_INTERNAL_URL", "http://localhost:9000"),
            "region_name": "us-east-1",
            "file_overwrite": False,
            "querystring_auth": False,
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

MEDIA_URL = f"{MINIO_PUBLIC_URL}/"
MEDIA_ROOT = None
