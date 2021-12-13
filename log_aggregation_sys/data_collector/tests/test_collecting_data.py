import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_aggregation_sys.settings")
import django

django.setup()

import pytest
from data_collector.data_aggregator import DataAggregator
from data_collector.models import (CpuData, DisksData, LogCategory, MemoryData,
                                   SensorsData)


@pytest.mark.django_db
class TestDataAggregator:
    def test_collect_cpu_data(self):
        cpu_data_dict = DataAggregator().get_all_cpu_data()
        assert CpuData.objects.all().count() == 0
        cpu_data_obj = CpuData(**cpu_data_dict)
        cpu_data_obj.save()
        assert CpuData.objects.all().count() == 1

    def test_collect_memory_data(self):
        memory_data_dict = DataAggregator().get_all_memory_data()
        assert MemoryData.objects.all().count() == 0
        memory_data_obj = MemoryData(**memory_data_dict)
        memory_data_obj.save()
        assert MemoryData.objects.all().count() == 1

    def test_collect_sensors_data(self):
        sensors_data_dict = DataAggregator().get_all_sensors_data()
        assert SensorsData.objects.all().count() == 0
        sensors_data_obj = SensorsData(**sensors_data_dict)
        sensors_data_obj.save()
        assert SensorsData.objects.all().count() == 1

    def test_collect_disk_data(self):
        disk_data_list = DataAggregator().get_all_disk_data()
        assert DisksData.objects.all().count() == 0
        disk_data_obj_list = [DisksData(**disk_data_dict) for disk_data_dict in disk_data_list]
        DisksData.objects.bulk_create(disk_data_obj_list)
        assert DisksData.objects.all().count() > 1


class TestCategories:
    @pytest.mark.parametrize(
        ("sensors_data", "category"),
        [
            ({"sec_left": 20000, "battery_percent": 20.4}, LogCategory.WARNING),
            ({"sec_left": 600, "battery_percent": 20.4}, LogCategory.WARNING),
            ({"sec_left": 599, "battery_percent": 20.4}, LogCategory.ERROR),
            ({"sec_left": 600, "battery_percent": 19.9}, LogCategory.ERROR),
            ({"sec_left": 1200, "battery_percent": 80.9}, LogCategory.INFORMATION),
            ({"sec_left": 1199, "battery_percent": 80.9}, LogCategory.WARNING),
            ({"sec_left": 1200, "battery_percent": 30}, LogCategory.INFORMATION),
            ({"sec_left": 1200, "battery_percent": 29.0}, LogCategory.WARNING),
        ],
    )
    def test_assign_sensors_data_category(self, sensors_data: dict, category: LogCategory):
        data_with_category = DataAggregator().assign_sensors_data_category(sensors_data)
        sensors_data["category"] = category
        assert data_with_category == sensors_data


    @pytest.mark.parametrize(
        ("memory_data", "category"),
        [
            (
                {"use_percentage_physical_memory": 30.4, "use_percentage_swap_memory": 60.4},
                LogCategory.INFORMATION,
            ),
            (
                {"use_percentage_physical_memory": 80.4, "use_percentage_swap_memory": 60.4},
                LogCategory.WARNING,
            ),
            (
                {"use_percentage_physical_memory": 80.4, "use_percentage_swap_memory": 80.4},
                LogCategory.WARNING,
            ),
            (
                {"use_percentage_physical_memory": 60.4, "use_percentage_swap_memory": 80.4},
                LogCategory.WARNING,
            ),
            (
                {"use_percentage_physical_memory": 90.4, "use_percentage_swap_memory": 60.4},
                LogCategory.ERROR,
            ),
            (
                {"use_percentage_physical_memory": 80.4, "use_percentage_swap_memory": 90.4},
                LogCategory.ERROR,
            ),
            (
                {"use_percentage_physical_memory": 30.4, "use_percentage_swap_memory": 90.4},
                LogCategory.ERROR,
            ),
            (
                {"use_percentage_physical_memory": 90.4, "use_percentage_swap_memory": 60.4},
                LogCategory.ERROR,
            ),
        ],
    )
    def test_assign_memory_data_category(
            self,
            memory_data: dict,
            category: LogCategory
    ):
        data_with_category = DataAggregator().\
            assign_memory_data_category(memory_data)
        memory_data["category"] = category
        assert data_with_category == memory_data

    @pytest.mark.parametrize(
        ("cpu_data", "category"),
        [
            (
                {
                    "cpu_percent": 30.1,
                    "cpu_time_percent_user": 20.4,
                    "cpu_time_percent_nice": 40.2,
                    "cpu_time_percent_system": 20.5,
                    "cpu_time_percent_idle": 40.2,
                },
                LogCategory.INFORMATION,
            ),
            (
                {
                    "cpu_percent": 80.1,
                    "cpu_time_percent_user": 20.4,
                    "cpu_time_percent_nice": 40.2,
                    "cpu_time_percent_system": 80.5,
                    "cpu_time_percent_idle": 40.2,
                },
                LogCategory.WARNING,
            ),
            (
                {
                    "cpu_percent": 80.1,
                    "cpu_time_percent_user": 20.4,
                    "cpu_time_percent_nice": 40.2,
                    "cpu_time_percent_system": 80.5,
                    "cpu_time_percent_idle": 90.2,
                },
                LogCategory.ERROR,
            ),
            (
                {
                    "cpu_percent": 30.1,
                    "cpu_time_percent_user": 20.4,
                    "cpu_time_percent_nice": 40.2,
                    "cpu_time_percent_system": 50.5,
                    "cpu_time_percent_idle": 90.2,
                },
                LogCategory.ERROR,
            ),
        ],
    )
    def test_assign_cpu_data_category(
            self,
            cpu_data: dict,
            category: LogCategory
    ):
        data_with_category = DataAggregator().\
            assign_cpu_data_category(cpu_data)
        cpu_data["category"] = category
        assert data_with_category == cpu_data

    @pytest.mark.parametrize(
        ("disk_data", "category"),
        [
            ({"percent": 30.4}, LogCategory.INFORMATION),
            ({"percent": 80}, LogCategory.INFORMATION),
            ({"percent": 81.0}, LogCategory.WARNING),
            ({"percent": 90.0}, LogCategory.WARNING),
            ({"percent": 91.0}, LogCategory.ERROR),
        ],
    )
    def test_assign_disk_data_category(
            self, disk_data: dict,
            category: LogCategory
    ):
        data_with_category = DataAggregator().\
            assign_disk_data_category(disk_data)
        disk_data["category"] = category
        assert data_with_category == disk_data
