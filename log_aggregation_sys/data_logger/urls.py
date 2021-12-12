from data_logger.views import (CpuDataView, DiskDataView, MemoryDataView,
                               SensorsDataView, main_menu_view)
from django.urls import path

app_name = "data_logger"

urlpatterns = [
    path("", main_menu_view, name="main_menu"),
    path("cpu_data/", CpuDataView.as_view(), name="cpu_data"),
    path("memory_data/", MemoryDataView.as_view(), name="memory_data"),
    path("sensors_data/", SensorsDataView.as_view(), name="sensors_data"),
    path("disk_data/", DiskDataView.as_view(), name="disk_data"),
]
