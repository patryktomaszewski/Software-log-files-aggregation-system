from django import template
from psutil._common import bytes2human

register = template.Library()


@register.filter
def bytes_attribute_solver(item: float) -> str:
    return bytes2human(item)


def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)


@register.filter
def battery_sec_left_attribute_solver(item: int) -> str:
    return secs2hours(item)


@register.filter
def battery_power_plugged_attribute_solver(
        is_plugged: bool,
        battery_percent: int) -> str:
    if is_plugged:
        return (
            "plugged (charging)"
            if battery_percent < 100
            else "plugged (fully charged)"
        )
    else:
        return "not plugged"
