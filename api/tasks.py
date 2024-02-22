from .sms import SMS
from celery import shared_task


@shared_task
def send_sms_notification(recepients, item):
    """Sends a message when an order has been submitted."""
    SMS().send(recepients, item)
