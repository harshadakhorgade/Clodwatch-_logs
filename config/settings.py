import os
import sys
import json
import boto3
import logging
from pathlib import Path
from botocore.exceptions import ClientError

import logging
from boto3.session import Session


import watchtower



# Setup
BASE_DIR = Path(__file__).resolve().parent.parent
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper: Fetch secrets from AWS
def get_secret():
    secret_name = "django_app_secrets"
    region_name = "us-west-2"

    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response["SecretString"])
    except ClientError as e:
        logger.warning(f"Could not fetch secrets from AWS: {e}")

        return {}

# Only fetch secrets for commands that need them
if any(cmd in sys.argv for cmd in ['runserver', 'runserver_plus', 'collectstatic', 'shell']):
    secrets = get_secret()
else:
    secrets = {}

# Usage
SECRET_KEY = secrets.get('SECRET_KEY', 'fallback-secret-key-for-local-dev')


# Fetch secrets from AWS Secrets Manager
# Fetch secrets from AWS Secrets Manager
# secret_name = "django_app_secrets"

# # secret_name = os.environ.get("DJANGO_SECRET_NAME", "django_app_secrets")
# # if not secret_name:
# #     raise ValueError("Environment variable DJANGO_SECRET_NAME is not set.")
# secrets = get_secret(secret_name)


print(secrets) 

# Set Django settings from secrets
# Determine if secrets are required
SECRETS_REQUIRED = any(cmd in sys.argv for cmd in ['runserver', 'runserver_plus', 'collectstatic', 'shell'])

# Use fallback key if not running critical commands
# SECRET_KEY = secrets.get("SECRET_KEY", "fallback-secret-key-for-dev")

# Only raise error if SECRET_KEY is truly needed
if SECRETS_REQUIRED and not secrets.get("SECRET_KEY"):
    logger.error("SECRET_KEY is missing in the secrets.")
    raise ValueError("SECRET_KEY is missing in the secrets.")


# # Don't fetch secrets for certain management commands
# SKIP_SECRETS = any(cmd in sys.argv for cmd in ["collectstatic", "makemigrations", "migrate", "check"])
# secrets = {} if SKIP_SECRETS else get_secret("django_app_secrets")

# # Fallback values for local/dev/testing
# SECRET_KEY = secrets.get("SECRET_KEY", "fallback-dev-key")

DEBUG = secrets.get("DEBUG", "False").lower() == "true"

# ALLOWED_HOSTS = ['172.31.32.70', 'mydemo.us-west-2.elasticbeanstalk.com']
ALLOWED_HOSTS = ['*']



# # settings.py or any logging config file
# # settings.py
# import logging
# import watchtower
# import boto3

# from core.logging_handlers import SafeWatchtowerHandler

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '[%(levelname)s] %(asctime)s %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#             'level': 'DEBUG',  # This will capture DEBUG level and above messages for console
#         },
#         'watchtower': {
#             # '()': SafeWatchtowerHandler,  # ← this is the key
#             '()': 'core.logging_handlers.SafeWatchtowerHandler',
#             'log_group': 'MyLog',
#             'stream_name': 'MyStream',
#             'level': 'ERROR',  # This will capture ERROR level and above messages for CloudWatch
#             'region_name': 'us-west-2',  # <-- Specify the region here
#         },
#     },
#     'root': {
#         'handlers': ['console', 'watchtower'],
#         'level': 'DEBUG',  # Root logger will capture DEBUG level and above messages
#     },
# }





# # settings.py

import logging
import boto3
# from core.logging_handlers import SafeWatchtowerHandler

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '[%(levelname)s] %(asctime)s %(message)s',
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple',
#             'level': 'DEBUG',  # This captures all DEBUG level and above logs for the console
#         },
#         'watchtower': {
#             '()': 'core.logging_handlers.SafeWatchtowerHandler',  # Using your custom handler
#             'log_group': 'MyLog',  # CloudWatch Log Group name
#             'stream_name': 'MyStream',  # CloudWatch Stream name
#             'level': 'ERROR',  # Logs only ERROR level and above to CloudWatch
#             'region_name': 'us-west-2',  # Region for CloudWatch
#         },
#     },
#     'root': {
#         'handlers': ['console', 'watchtower'],  # Send logs to both console and CloudWatch
#         'level': 'DEBUG',  # Root logger will capture DEBUG level and above logs
#     },
# }

import boto3
import watchtower

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # Keeps the default logging behavior intact

    'handlers': {
        'watchtower': {
            'level': 'DEBUG',  # Log level for CloudWatch
            'class': 'watchtower.CloudWatchLogHandler',
            'log_group': 'MyLog',  # Log Group in CloudWatch
            'stream_name': 'MyStream',  # Log Stream in CloudWatch
            'create_log_group': True,  # Auto-create log group if not exists
            'create_log_stream': True,  # Auto-create log stream if not exists
            'boto3_client': boto3.client('logs', region_name='us-west-2'),  # Explicitly specify AWS region
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',  # Console handler for local logging
        },
    },

    'loggers': {
        'django': {
            'handlers': ['watchtower', 'console'],  # Add watchtower and console handler
            'level': 'DEBUG',  # Log level for Django
            'propagate': True,
        },
        'django.request': {
            'handlers': ['watchtower', 'console'],  # Add watchtower for request logging
            'level': 'DEBUG',  # Log errors for request logs
            'propagate': False,
        },

        'core.views': {  # 👈 Add this line
            'handlers': ['watchtower', 'console'],
            'level': 'DEBUG',
            'propagate': False,  # Prevent logs from propagating to 'django'
        },
    }
}




INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",  # For AWS S3 integration
    "core",
]

# Database (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Using SQLite
        "NAME": BASE_DIR / "db.sqlite3",  # SQLite file location
    }
}



# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Add this if you have custom templates
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]



MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # For static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]



# AWS Config only when not skipping secrets
if secrets:
    AWS_ACCESS_KEY_ID = secrets.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = secrets.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = secrets.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = secrets.get("AWS_S3_REGION_NAME")
    # AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None

    # NEW: Use CloudFront domain if available, otherwise fallback to S3 URL
    AWS_CLOUDFRONT_DOMAIN = secrets.get("AWS_CLOUDFRONT_DOMAIN")  # <-- added this line
    if AWS_CLOUDFRONT_DOMAIN:
        AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN
    else:
        AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

    

# # Ensure all required AWS credentials are available
# required_aws_keys = [AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME]
# for key in required_aws_keys:
#     if not key:
#         logger.error(f"Missing AWS credentials: {key}")
#         raise ValueError("Missing AWS credentials in secrets.")



# Validate AWS Keys
if SECRETS_REQUIRED:
    required_aws_keys = {
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        "AWS_STORAGE_BUCKET_NAME": AWS_STORAGE_BUCKET_NAME,
        "AWS_S3_REGION_NAME": AWS_S3_REGION_NAME,
        "AWS_S3_CUSTOM_DOMAIN": AWS_S3_CUSTOM_DOMAIN

    }

    for key_name, key_value in required_aws_keys.items():
        if not key_value:
            logger.error(f"Missing AWS credential: {key_name}")
            raise ValueError(f"Missing AWS credential: {key_name} in secrets.")


# Always define STATIC_ROOT regardless of environment
# STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Static/Media Setup
if secrets:
    STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/static/"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'
    STATICFILES_DIRS = [BASE_DIR / "static"]

# Root URL
ROOT_URLCONF = "config.urls"

# Django settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
