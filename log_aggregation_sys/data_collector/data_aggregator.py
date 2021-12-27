import os
import platform
import sys

import psutil
from data_collector.aggregation_constants import (
    CPU_DATA_ERROR_GREATER_THAN,
    CPU_DATA_WARNING_GREATER_THAN,
    CPU_DATA_WARNING_LESS_OR_EQUAL,
    DISK_DATA_ERROR_GREATER_THAN,
    DISK_DATA_WARNING_GREATER_THAN,
    DISK_DATA_WARNING_LESS_OR_EQUAL,
    MEMORY_DATA_ERROR_GREATER_THAN,
    MEMORY_DATA_WARNING_GREATER_THAN,
    MEMORY_DATA_WARNING_LESS_OR_EQUAL,
    SENSORS_BATTERY_DATA_ERROR_LESS_THAN,
    SENSORS_BATTERY_DATA_WARNING_GREATER_OR_EQUAL,
    SENSORS_BATTERY_DATA_WARNING_LESS_THAN,
)
from data_collector.models import LogCategory


class DataAggregator:
    @staticmethod
    def _get_cpu_times_data() -> dict:
        cpu_times = psutil.cpu_times()
        return {
            "user_time": cpu_times.user,
            "nice_time": cpu_times.nice,
            "system_time": cpu_times.system,
            "idle_time": cpu_times.idle,
        }

    @staticmethod
    def _get_cpu_percent_data() -> dict:
        return {
            "cpu_percent": psutil.cpu_percent(),
        }

    @staticmethod
    def _get_cpu_times_percent_data() -> dict:
        cpu_times_percent = psutil.cpu_times_percent()
        return {
            "cpu_time_percent_user": cpu_times_percent.user,
            "cpu_time_percent_nice": cpu_times_percent.nice,
            "cpu_time_percent_system": cpu_times_percent.system,
            "cpu_time_percent_idle": cpu_times_percent.idle,
        }

    @staticmethod
    def _get_cpu_count_data() -> dict:
        return {
            "cpu_count_logical": psutil.cpu_count(),
            "cpu_count_physical": psutil.cpu_count(logical=False),
        }

    @staticmethod
    def _get_cpu_stats_data() -> dict:
        cpu_stats = psutil.cpu_stats()
        return {
            "ctx_switches": cpu_stats.ctx_switches,
            "interrupts": cpu_stats.interrupts,
            "soft_interrupts": cpu_stats.soft_interrupts,
            "sys_calls": cpu_stats.syscalls,
        }

    @staticmethod
    def _get_cpu_freq_data() -> dict:
        cpu_freq = psutil.cpu_freq()
        return {
            "cpu_frequency_current": cpu_freq.current,
            "cpu_frequency_min": cpu_freq.min,
            "cpu_frequency_max": cpu_freq.max,
        }

    @staticmethod
    def _get_cpu_load_avg_data() -> dict:
        avg_1_min, avg_5_min, avg_15_min = psutil.getloadavg()
        return {
            "load_avg_1_min": avg_1_min,
            "load_avg_5_min": avg_5_min,
            "load_avg_15_min": avg_15_min,
        }

    @staticmethod
    def _get_physical_memory_data() -> dict:
        virtual_memory_data = psutil.virtual_memory()
        return {
            "total_physical_memory": virtual_memory_data.total,
            "available_physical_memory": virtual_memory_data.available,
            "used_physical_memory": virtual_memory_data.used,
            "use_percentage_physical_memory": virtual_memory_data.percent,
        }

    @staticmethod
    def _get_swap_memory_data() -> dict:
        swap_memory_data = psutil.swap_memory()
        return {
            "total_swap_memory": swap_memory_data.total,
            "free_swap_memory": swap_memory_data.free,
            "used_swap_memory": swap_memory_data.used,
            "use_percentage_swap_memory": swap_memory_data.percent,
            "sin_swap_memory": swap_memory_data.sin,
        }

    def get_all_cpu_data(self) -> dict:
        import logging
        logging.error(f"???????? machine: {platform.machine()}")
        sys.stdout.write(f"???????? machine: {platform.machine()}")

        if platform.machine() == "arm64":
            # Cpu freq not supported by M1 Apple silicon
            return (
                self._get_cpu_times_data() |
                self._get_cpu_percent_data() |
                self._get_cpu_times_percent_data() |
                self._get_cpu_count_data() |
                self._get_cpu_stats_data() |
                self._get_cpu_load_avg_data()
            )
        return (
            self._get_cpu_times_data() |
            self._get_cpu_percent_data() |
            self._get_cpu_times_percent_data() |
            self._get_cpu_count_data() |
            self._get_cpu_stats_data() |
            self._get_cpu_load_avg_data() |
            self._get_cpu_freq_data()
        )

    def get_all_memory_data(self) -> dict:
        return self._get_physical_memory_data() | self._get_swap_memory_data()

    @staticmethod
    def get_all_sensors_data() -> dict:
        sensors_battery_data = psutil.sensors_battery()
        return {
            "battery_percent": sensors_battery_data.percent,
            "is_power_plugged": sensors_battery_data.power_plugged,
            "sec_left": sensors_battery_data.secsleft,
        }

    @staticmethod
    def get_all_disk_data() -> list[dict]:
        disk_partitions_data = []
        for part in psutil.disk_partitions(all=False):
            if os.name == "nt":
                if "cdrom" in part.opts or part.fstype == "":
                    # skip cd-rom drives with no disk in it; they may raise
                    # ENOENT, pop-up a Windows GUI error for a non-ready
                    # partition or just hang.
                    continue
            usage = psutil.disk_usage(part.mountpoint)
            disk_partitions_data.append(
                {
                    "device": part.device,
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                    "type": part.fstype,
                    "mountpoint": part.mountpoint,
                }
            )
        return disk_partitions_data

    @staticmethod
    def _is_data_warning(
            data_list: list,
            gt: int, lt: int,
            is_sensor_data: bool = False
    ) -> bool:
        if is_sensor_data:
            return any(gt <= record < lt for record in data_list)
        return any(gt < record <= lt for record in data_list)

    @staticmethod
    def _is_data_error(
            data_list: list, gt: int,
            is_sensor_data: bool = False
    ) -> bool:
        if is_sensor_data:
            return any(gt > record for record in data_list)
        return any(gt < record for record in data_list)

    def assign_cpu_data_category(self, cpu_data: dict) -> dict:
        cpu_data_category_keys = [
            cpu_data["cpu_percent"],
            cpu_data["cpu_time_percent_user"],
            cpu_data["cpu_time_percent_nice"],
            cpu_data["cpu_time_percent_system"],
            cpu_data["cpu_time_percent_idle"],
        ]
        if self._is_data_error(
                cpu_data_category_keys,
                CPU_DATA_ERROR_GREATER_THAN
        ):
            cpu_data["category"] = LogCategory.ERROR
            return cpu_data

        if self._is_data_warning(
            cpu_data_category_keys,
            CPU_DATA_WARNING_GREATER_THAN,
            CPU_DATA_WARNING_LESS_OR_EQUAL,
        ):
            cpu_data["category"] = LogCategory.WARNING
            return cpu_data

        cpu_data["category"] = LogCategory.INFORMATION
        return cpu_data

    def assign_memory_data_category(self, memory_data: dict) -> dict:
        memory_data_category_keys = [
            memory_data["use_percentage_physical_memory"],
            memory_data["use_percentage_swap_memory"],
        ]

        if self._is_data_error(
                memory_data_category_keys,
                MEMORY_DATA_ERROR_GREATER_THAN
        ):
            memory_data["category"] = LogCategory.ERROR
            return memory_data

        if self._is_data_warning(
            memory_data_category_keys,
            MEMORY_DATA_WARNING_GREATER_THAN,
            MEMORY_DATA_WARNING_LESS_OR_EQUAL,
        ):
            memory_data["category"] = LogCategory.WARNING
            return memory_data

        memory_data["category"] = LogCategory.INFORMATION
        return memory_data

    def assign_sensors_data_category(self, sensors_data: dict) -> dict:
        if self._is_data_error(
            [sensors_data["battery_percent"]],
            SENSORS_BATTERY_DATA_ERROR_LESS_THAN,
            is_sensor_data=True,
        ):
            sensors_data["category"] = LogCategory.ERROR
            return sensors_data

        if self._is_data_warning(
            [sensors_data["battery_percent"]],
            SENSORS_BATTERY_DATA_WARNING_GREATER_OR_EQUAL,
            SENSORS_BATTERY_DATA_WARNING_LESS_THAN,
            is_sensor_data=True,
        ):
            sensors_data["category"] = LogCategory.WARNING
            return sensors_data

        sensors_data["category"] = LogCategory.INFORMATION
        return sensors_data

    def assign_disk_data_category(self, disk_data: dict) -> dict:
        if self._is_data_error(
            [disk_data["percent"]],
            DISK_DATA_ERROR_GREATER_THAN,
        ):
            return disk_data
        if self._is_data_warning(
            [disk_data["percent"]],
                DISK_DATA_WARNING_GREATER_THAN,
                DISK_DATA_WARNING_LESS_OR_EQUAL
        ):
            disk_data["category"] = LogCategory.WARNING
            return disk_data

        disk_data["category"] = LogCategory.INFORMATION
        return disk_data
