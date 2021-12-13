from data_collector.models import (CpuData, DisksData, LogCategory, MemoryData,
                                   SensorsData)
from data_saver.email_alert import send_email_alert
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=CpuData)
def create_cpu_data(sender, instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)


@receiver(post_save, sender=MemoryData)
def create_memory_data(sender, instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)


@receiver(post_save, sender=SensorsData)
def create_sensors_data(sender, instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)


@receiver(post_save, sender=DisksData)
def create_disk_data(instance, created, **kwargs):  # noqa: F811
    if instance.category == LogCategory.ERROR and settings.ALERT_EMAIL_ADDRESS:
        send_email_alert(instance)
