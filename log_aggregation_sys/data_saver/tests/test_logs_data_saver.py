import os
import platform

import django
import pytest
from data_collector.models import CpuData, DisksData, MemoryData, SensorsData
from data_saver.logs_data_saver import DataSaver
from django.test import LiveServerTestCase
from pytest_mock import MockFixture
from time import sleep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "log_aggregation_sys.settings")

django.setup()


@pytest.mark.django_db
class TestDataSaver:
    def test_create_data_objects(self, mocker: MockFixture):
        mocker.patch(
            "data_collector.data_aggregator.DataAggregator.get_all_sensors_data",
            return_value={
                "battery_percent": 23.6,
                "is_power_plugged": True,
                "sec_left": 23,
            },
        )

        assert CpuData.objects.all().count() == 0
        assert MemoryData.objects.all().count() == 0
        assert SensorsData.objects.all().count() == 0
        assert DisksData.objects.all().count() == 0

        DataSaver().create_data_objects()

        assert CpuData.objects.all().count() == 1
        cpu_data = CpuData.objects.all().values()[0]
        if platform.machine() == "arm64":
            not_present_values = [
                "cpu_frequency_current",
                "cpu_frequency_min",
                "cpu_frequency_max"]
            for key in not_present_values:
                removed_value = cpu_data.pop(key)
                assert removed_value is None
        assert None not in list(cpu_data.values())

        assert MemoryData.objects.all().count() == 1
        memory_data = MemoryData.objects.all().values()[0]
        assert None not in list(memory_data.values())

        assert SensorsData.objects.all().count() == 1
        sensors_data = SensorsData.objects.all().values()[0]
        assert None not in list(sensors_data.values())

        assert DisksData.objects.all().count() > 1
        disk_data_qs = DisksData.objects.all().values()
        for disk_data in disk_data_qs:
            assert None not in list(disk_data.values())


@pytest.mark.django_db
class TestBackgroundTaskAggregatingData(LiveServerTestCase):
    @pytest.fixture(autouse=True)
    def __inject_fixtures(self, mocker):
        self.mocker = mocker

    def test_auto_data_aggregation(self):
        self.mocker.patch(
            "data_collector.data_aggregator.DataAggregator.get_all_sensors_data",
            return_value={
                "battery_percent": 23.6,
                "is_power_plugged": True,
                "sec_left": 23,
            },
        )

        assert CpuData.objects.all().count() == 0
        assert MemoryData.objects.all().count() == 0
        assert SensorsData.objects.all().count() == 0
        assert DisksData.objects.all().count() == 0

        sleep(20)
        assert CpuData.objects.all().count() == 1
        assert MemoryData.objects.all().count() == 1
        assert SensorsData.objects.all().count() == 1
        disk_data_objects = DisksData.objects.all().count()
        assert disk_data_objects > 1

        sleep(20)
        assert CpuData.objects.all().count() == 2
        assert MemoryData.objects.all().count() == 2
        assert SensorsData.objects.all().count() == 2
        assert DisksData.objects.all().count() > disk_data_objects
