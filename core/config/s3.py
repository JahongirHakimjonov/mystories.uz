import os  # noqa

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "region_name": os.getenv("S3_REGION"),  # e.g., "us-east-1"
            "bucket_name": os.getenv("BUCKET_NAME"),
        },
    },
    "staticfiles": {  # For static files
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "region_name": os.getenv("S3_REGION"),  # e.g., "us-east-1"
            "bucket_name": os.getenv("BUCKET_NAME"),
            "location": "static",  # Specify a folder within your bucket
        },
    },
}

DEFAULT_FILE_STORAGE = "core.settings.storages.default"  # Replace "config.settings" with your actual settings path
STATICFILES_STORAGE = "core.settings.storages.staticfiles"
