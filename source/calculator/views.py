from pathlib import Path
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, FormView

from object_classification.detect_and_classify import detect_and_classify
from . import models, forms
from .models import User


DETECTION_MODEL_PATH = Path('object_detection') / 'weights' / 'model_200.pt'
CLASSIFICATION_MODEL_PATH = Path('object_classification') / 'weights' / 'resnet50_food.pt'
CLASSES_FILE_PATH = Path('object_classification') / 'classes.txt'


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


class CashierView(LoginRequiredMixin, CreateView):
    template_name = 'cash_register.html'
    form_class = forms.FileForm
    model = models.File
    success_url = reverse_lazy('transaction')

    def form_valid(self, form):
        image_data = form.cleaned_data.get("file")
        if not image_data:
            messages.warning(self.request, 'Please resubmit the file.')
            return redirect('cashier')
        image_file = form.save(commit=False)
        scan = models.Scan.objects.create(image=image_file)
        image_file.save()
        scan.save()
        response = super().form_valid(form)
        response.set_cookie('file_name', image_data)
        return response

    def get_success_url(self):
        return reverse('transaction')


class PositionView(LoginRequiredMixin, ListView):
    template_name = 'positions.html'
    model = models.Position
    paginate_by = 8
    paginate_orphans = 3
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


class TransactionView(LoginRequiredMixin, CreateView):
    template_name = 'transaction.html'
    form_class = forms.TransactionForm
    model = models.Transaction
    success_url = reverse_lazy('cashier')

    def get_classification_results(self, request):
        file_name = request.COOKIES.get('file_name')
        if file_name is not None:
            FILE_PATH = Path('media') / f'{file_name}'
            with open(CLASSES_FILE_PATH, 'r') as f:
                classes = f.read().split()
            return detect_and_classify(
                FILE_PATH,
                file_name,
                yolov5_model_file=DETECTION_MODEL_PATH,
                classifier_model_file=CLASSIFICATION_MODEL_PATH,
                classes=classes,
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        results, img = self.get_classification_results(self.request)

        if not results:
            self.render_to_response(context)
        position_names = [position['class_label'] for position in results]

        # Fetch positions using a single query
        position_queryset = models.Position.objects.filter(name__in=position_names).values('name', 'price')

        # Fetch all positions using a single query
        all_positions = models.Position.objects.all()

        # Fetch all users using a single query
        all_users = User.objects.all().prefetch_related('transactions')

        context['positions_classified'] = position_queryset
        context['positions'] = all_positions
        context['users'] = all_users
        context['image_url'] = img
        return context


    def form_valid(self, form):
        # Save the transaction instance without committing to the database
        transaction = form.save(commit=False)

        # Get the user from the form
        transaction.user = form.cleaned_data['user']

        # Update positions field
        position_ids = self.request.POST.getlist('positions')
        positions = []
        for position_id in position_ids:
            position = models.Position.objects.get(pk=position_id)
            positions.append({
                'name': position.name,
                'price': position.price
            })
        transaction.positions = positions

        # Get the total check from the form
        transaction.total_check = form.cleaned_data['total_check']

        # Save the transaction instance to the database
        transaction.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cashier')
