from data_collector.models import (CpuData, DisksData, LogCategory, MemoryData,
                                   SensorsData)
from data_saver.email_alert import send_email_alert
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CpuData)
def create_profile(sender, instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)


@receiver(post_save, sender=MemoryData)
def create_profile(sender, instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)


@receiver(post_save, sender=SensorsData)
def create_profile(sender, instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)


@receiver(post_save, sender=DisksData)
def create_profile(instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)
