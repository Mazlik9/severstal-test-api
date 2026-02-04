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
USE_S3 = os.getenv("USE_S3", "true").lower() == "true"

MINIO_INTERNAL_URL = os.getenv("MINIO_INTERNAL_URL", "http://minio:9000")
MINIO_PUBLIC_URL = os.getenv("MINIO_PUBLIC_URL", "http://localhost:9000")

if USE_S3:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME", "severstal-local-media"),
                "access_key": os.getenv("MINIO_ROOT_USER", "minioadmin"),
                "secret_key": os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123"),
                "endpoint_url": MINIO_INTERNAL_URL,
                "region_name": os.getenv("AWS_S3_REGION_NAME", "us-east-1"),
                "signature_version": "s3v4",
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
else:
    # Локальное хранение файлов
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# =========================
# MEDIA
# =========================
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# =========================
# STATIC
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
