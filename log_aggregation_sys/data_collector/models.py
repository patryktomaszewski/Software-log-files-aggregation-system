from django.db import models
from django.utils.translation import gettext_lazy as _


class LogCategory(models.TextChoices):
    INFORMATION = "INFO", _("Information")
    ERROR = "ERR", _("Error")
    WARNING = "WRN", _("Warning")


class CpuData(models.Model):
    user_time = models.FloatField(_("User Time"))
    nice_time = models.FloatField(_("Nice Time"))
    system_time = models.FloatField(_("System Time"))
    idle_time = models.FloatField(_("Idle Time"))
    cpu_percent = models.FloatField(_("%CPU"))
    cpu_time_percent_user = models.FloatField(_("%CPU User Time"))
    cpu_time_percent_nice = models.FloatField(_("%CPU Nice Time"))
    cpu_time_percent_system = models.FloatField(_("%CPU System Time"))
    cpu_time_percent_idle = models.FloatField(_("%CPU Idle Time"))
    cpu_count_logical = models.IntegerField(_("CPU Count Logical"), null=True)
    cpu_count_physical = models.IntegerField(_("CPU Count Physical"), null=True)
    ctx_switches = models.IntegerField(_("Context Switches"))
    interrupts = models.IntegerField(_("Interrupts"))
    soft_interrupts = models.IntegerField(_("Soft Interrupts"))
    sys_calls = models.IntegerField(_("System Calls"))
    cpu_frequency_current = models.FloatField(_("CPU Current Frequency"), blank=True, null=True)
    cpu_frequency_min = models.FloatField(_("CPU Min Frequency"), blank=True, null=True)
    cpu_frequency_max = models.FloatField(_("CPU Max Frequency"), blank=True, null=True)
    load_avg_1_min = models.FloatField(_("Average System Load 1 Minute"))
    load_avg_5_min = models.FloatField(_("Average System Load 5 Minutes"))
    load_avg_15_min = models.FloatField(_("Average System Load 15 Minutes"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=6, choices=LogCategory.choices, default=LogCategory.INFORMATION
    )


class MemoryData(models.Model):
    total_physical_memory = models.FloatField(_("Total Physical Memory"))
    available_physical_memory = models.FloatField(_("Available Physical Memory"))
    used_physical_memory = models.FloatField(_("Used Physical Memory"))
    use_percentage_physical_memory = models.FloatField(_("Use Percentage Physical Memory"))
    total_swap_memory = models.FloatField(_("Total Swap Memory"))
    free_swap_memory = models.FloatField(_("Free Swap Memory"))
    used_swap_memory = models.FloatField(_("Used Swap Memory"))
    use_percentage_swap_memory = models.FloatField(_("Use Percentage Swap Memory"))
    sin_swap_memory = models.FloatField(_("Number of Bytes The System Has Swapped In From Disk"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=6, choices=LogCategory.choices, default=LogCategory.INFORMATION
    )


class SensorsData(models.Model):
    battery_percent = models.IntegerField(_("Battery Percentage"))
    is_power_plugged = models.BooleanField(_("Is Power Plugged"))
    sec_left = models.IntegerField(
        _("Approximation of how many seconds are left before the battery runs out of power")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=6, choices=LogCategory.choices, default=LogCategory.INFORMATION
    )


class DisksData(models.Model):
    device = models.CharField(_('Device'), max_length=255)
    total = models.BigIntegerField(_('Total disk size'))
    used = models.BigIntegerField(_("Used disk size"))
    free = models.BigIntegerField(_("Free disk size"))
    percent = models.FloatField(_("Percent of used disk"))
    type = models.CharField(_("Type of disk"), max_length=255)
    mountpoint = models.CharField(_("Mountpoint"), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(
        max_length=6, choices=LogCategory.choices, default=LogCategory.INFORMATION
    )
