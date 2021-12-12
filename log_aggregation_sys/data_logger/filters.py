import django_filters
from data_collector.models import (CpuData, DisksData, LogCategory, MemoryData,
                                   SensorsData)
from django.forms.widgets import DateTimeInput


class BaseDataFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateTimeFilter(
        widget=DateTimeInput(
            attrs={"type": "datetime-local"},
        ),
        lookup_expr="gte",
        field_name="created_at",
        label="Logs after date: ",
    )
    created_at__lte = django_filters.DateTimeFilter(
        widget=DateTimeInput(
            attrs={"type": "datetime-local"},
        ),
        lookup_expr="lte",
        field_name="created_at",
        label="Logs before date: ",
    )

    category = django_filters.ChoiceFilter(choices=LogCategory.choices)


class CpuDataFilter(BaseDataFilter):
    class Meta:
        model = CpuData
        fields = ["category"]


class MemoryDataFilter(BaseDataFilter):
    class Meta:
        model = MemoryData
        fields = ["category"]


class SensorsDataFilter(BaseDataFilter):
    class Meta:
        model = SensorsData
        fields = ["category"]


class DiskDataFilter(BaseDataFilter):
    class Meta:
        model = DisksData
        fields = ["category"]
