# Create your views here.
import base64
import os
import subprocess
import uuid
from pathlib import Path
from urllib.parse import urlencode

import torch
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, FormView

from object_detection.detect import run
from object_detection.yolov5 import detect
from . import models, forms


weights_path = 'object_detection/weights/model_200.pt'


class MainView(FormView):

    template_name = 'index.html'
    form_class = forms.MailForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        recipients = ['begoshaaaa@gmail.com']
        send_mail(
            subject=form.cleaned_data.get('subject'),
            message=f"{form.cleaned_data.get('message')}"
                    f"\nfrom: {form.cleaned_data.get('name')} {form.cleaned_data.get('email')}",
            from_email=recipients[0],
            recipient_list=recipients,
            fail_silently=False,
        )
        return super().form_valid(form)


class CashierView(CreateView):
    template_name = 'cash_register.html'
    form_class = forms.FileForm
    model = models.File
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        file = form.save(commit=False)
        scan = models.Scan.objects.create(image=file)
        file.save()
        scan.save()
        weights_path = Path('object_detection') / 'weights' / 'model_200.pt'
        file_path = Path('uploads') / f'{form.cleaned_data["file"]}'
        output_path = Path('object_detection') / 'static' / 'output'
        run(weights=weights_path, source=file_path, project=output_path, save_crop=True, save_txt=True)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cashier')


class PositionView(ListView):
    template_name = 'positions.html'
    model = models.Position
    paginate_by = 5
    context_object_name = 'positions'

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            queryset = queryset.filter(name__icontains=self.search_value)
        return queryset

    def get_search_form(self):
        return forms.SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None

