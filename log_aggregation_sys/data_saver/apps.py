from django.apps import AppConfig
import os


class DataSaverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'data_saver'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from data_saver.logs_data_saver import DataSaver
            DataSaver().start_scheduler()
