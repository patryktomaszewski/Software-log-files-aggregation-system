
import re
import pytest
from data_collector.data_aggregator import DataAggregator
from data_collector.models import MemoryData
from data_logger.templatetags.template_helpers import bytes_attribute_solver


@pytest.mark.django_db
class TestTemplateHelpers:
    def test_bytes_attribute_solver(self):
        memory_data_dict = DataAggregator().get_all_memory_data()
        assert MemoryData.objects.all().count() == 0
        memory_data_obj = MemoryData(**memory_data_dict)
        memory_data_obj.save()
        data_log = MemoryData.objects.first()
        template_data = bytes_attribute_solver(data_log.total_physical_memory)
        assert isinstance(template_data, str)
        split_str = re.split('([-+]?\d+\.\d+)|([-+]?\d+)', template_data)
        assert split_str[-1] == "G"
