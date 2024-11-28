from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "access_key": os.getenv("S3_ACCESS_KEY_ID"),
#             "secret_key": os.getenv("S3_SECRET_ACCESS_KEY"),
#             "region_name": os.getenv("S3_REGION"),
#             "bucket_name": os.getenv("S3_BUCKET_NAME"),
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "access_key": os.getenv("S3_ACCESS_KEY_ID"),
#             "secret_key": os.getenv("S3_SECRET_ACCESS_KEY"),
#             "region_name": os.getenv("S3_REGION"),
#             "bucket_name": os.getenv("S3_BUCKET_NAME"),
#             "location": "static",
#         },
#     },
# }

AWS_ACCESS_KEY_ID = "636ced63c862b8e11e2a6cdbfbe1aede"
AWS_SECRET_ACCESS_KEY = "9795377241c39a9692ed0e6e8b16853d"
AWS_STORAGE_BUCKET_NAME = "mystories"  # yoki Contabo'ning S3 bucket nomi
AWS_S3_ENDPOINT_URL = (
    "https://eu2.contabostorage.com/mystories"  # yoki Contabo S3 uchun maxsus endpoint
)
AWS_S3_REGION_NAME = "eu-central-1"  # yoki Contabo'ning S3 mintaqasi
# AWS_S3_SIGNATURE_VERSION = 's3v4'  # Imzo versiyasi


# Media fayllar uchun URLni sozlash (ixtiyoriy)
STATIC_URL = (
    "https://eu2.contabostorage.com/799cabf6462740dcb4b79fda130c1355:mystories/static/"
)
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

MEDIA_URL = (
    "https://eu2.contabostorage.com/799cabf6462740dcb4b79fda130c1355:mystories/media/"
)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
