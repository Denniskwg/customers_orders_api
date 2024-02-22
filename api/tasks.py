from .sms import SMS
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_sms_notification(recepients, item):
    """Sends a message when an order has been submitted."""
    try:
        SMS().send(recepients, item)
        logger.info("Task executed successfully")
    except Exception as e:
        logger.exception("An error occurred in the task: %s", e)
