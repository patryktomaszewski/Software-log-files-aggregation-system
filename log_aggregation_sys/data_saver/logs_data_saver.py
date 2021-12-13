import threading
import time

from data_collector.data_aggregator import DataAggregator
from data_collector.models import CpuData, DisksData, MemoryData, SensorsData
from schedule import Scheduler
import logging


def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run


Scheduler.run_continuously = run_continuously


class DataSaver:
    @staticmethod
    def _create_cpu_data_object():
        cpu_data_dict = DataAggregator().get_all_cpu_data()
        cpu_data_with_category = DataAggregator().\
            assign_cpu_data_category(cpu_data_dict)
        cpu_data_obj = CpuData(**cpu_data_with_category)
        cpu_data_obj.save()
        logging.info("Cpu data object created")

    @staticmethod
    def _create_memory_data_object():
        memory_data_dict = DataAggregator().get_all_memory_data()
        memory_data_with_category = DataAggregator().\
            assign_memory_data_category(memory_data_dict)
        memory_data_obj = MemoryData(**memory_data_with_category)
        memory_data_obj.save()
        logging.info("Memory data object created")

    @staticmethod
    def _create_sensors_data_object():
        sensors_data_dict = DataAggregator().get_all_sensors_data()
        sensors_data_with_category = DataAggregator().\
            assign_sensors_data_category(sensors_data_dict)
        sensors_data_obj = SensorsData(**sensors_data_with_category)
        sensors_data_obj.save()
        logging.info("Sensors data object created")

    @staticmethod
    def _create_disk_data_object():
        disk_data_list = DataAggregator().get_all_disk_data()
        disk_data_list_with_category = [
            DataAggregator().assign_disk_data_category(disk_data_dict)
            for disk_data_dict in disk_data_list
        ]
        disk_data_obj_list = [
            DisksData(**disk_data_dict)
            for disk_data_dict in disk_data_list_with_category
        ]
        DisksData.objects.bulk_create(disk_data_obj_list)
        logging.info("Disk data object created")

    def create_data_objects(self):
        self._create_cpu_data_object()
        self._create_memory_data_object()
        self._create_sensors_data_object()
        self._create_disk_data_object()

    def start_scheduler(self):
        scheduler = Scheduler()
        scheduler.every(15).seconds.do(self.create_data_objects)
        scheduler.run_continuously()
