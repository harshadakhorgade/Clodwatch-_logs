from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
import logging

logger = logging.getLogger(__name__)
logger.error("🔥 Test error from Django app at startup")
