import logging
from django.core.management.base import BaseCommand

# Update to match the logger name in your settings
logger = logging.getLogger('watchtower-logger')

class Command(BaseCommand):
    help = "Sends test logs to AWS CloudWatch"

    def handle(self, *args, **kwargs):
        logger.info("Test log sent to CloudWatch!")
        self.stdout.write(self.style.SUCCESS("✅ Log sent to CloudWatch."))
# Test logs
logger.debug("This is a DEBUG message.")
logger.info("This is an INFO message.")
logger.warning("This is a WARNING message.")
logger.error("This is an ERROR message.")
logger.critical("This is a CRITICAL message.")