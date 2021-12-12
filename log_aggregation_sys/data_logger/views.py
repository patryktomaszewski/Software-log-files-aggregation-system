from data_collector.models import CpuData, DisksData, MemoryData, SensorsData
from data_logger.filters import (CpuDataFilter, DiskDataFilter,
                                 MemoryDataFilter, SensorsDataFilter)
from data_logger.forms import EmailForm
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView, MultipleObjectMixin

from django.conf import settings


def main_menu_view(request):
    return render(request, "main_menu/main_menu.html")


class BaseDataView(ListView, MultipleObjectMixin):
    formset_class = EmailForm

    def get_ordering(self):
        ordering = self.request.GET.get("ordering", "-created_at")
        return ordering

    def get_queryset(self):
        qs = super().get_queryset()
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs, self.filter

    def get(self, request, *args, **kwargs):
        self.object_list, filter = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data()
        context["data_filter"] = filter
        context["email_form"] = EmailForm

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        form = EmailForm(request.POST)
        if form.is_valid():
            settings.ALERT_EMAIL_ADDRESS = form.cleaned_data.get("email")
        return redirect(request.get_full_path())


class CpuDataView(BaseDataView):
    model = CpuData
    queryset = CpuData.objects.all()
    filterset_class = CpuDataFilter
    template_name = "data_logger/cpu_data.html"


class MemoryDataView(BaseDataView):
    model = MemoryData
    queryset = MemoryData.objects.all()
    filterset_class = MemoryDataFilter
    template_name = "data_logger/memory_data.html"


class SensorsDataView(BaseDataView):
    model = SensorsData
    queryset = SensorsData.objects.all()
    filterset_class = SensorsDataFilter
    template_name = "data_logger/sensors_data.html"


class DiskDataView(BaseDataView):
    model = DisksData
    queryset = DisksData.objects.all()
    filterset_class = DiskDataFilter
    template_name = "data_logger/disk_data.html"
