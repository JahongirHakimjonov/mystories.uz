import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))


class MediaStorage:
    pass


AWS_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "mystories")
AWS_S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "https://eu2.contabostorage.com")
AWS_S3_REGION_NAME = os.getenv("S3_REGION", "eu-central-1")
AWS_S3_SIGNATURE_VERSION = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL = os.getenv(
    "MEDIA_URL",
    f"{AWS_S3_ENDPOINT_URL}",
)

AWS_S3_VERIFY = True
