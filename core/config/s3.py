import os

from django.conf import settings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

AWS_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "mystories")
AWS_S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "https://eu2.contabostorage.com")
AWS_S3_REGION_NAME = os.getenv("S3_REGION", "eu-central-1")
AWS_S3_SIGNATURE_VERSION = os.getenv("S3_SIGNATURE_VERSION", "s3v4")

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL = os.getenv(
    "MEDIA_URL",
    f"{AWS_S3_ENDPOINT_URL}/799cabf6462740dcb4b79fda130c1355:{AWS_STORAGE_BUCKET_NAME}/media/",
)

if settings.DEBUG:
    AWS_S3_VERIFY = False
