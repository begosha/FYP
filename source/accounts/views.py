from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import DetailView, ListView

from calculator import models
from . import forms


class UserList(LoginRequiredMixin, ListView):
    template_name = 'user_list.html'
    model = User
    paginate_by = 5
    context_object_name = 'user_objects'

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
            query = Q(first_name__icontains=self.search_value) | Q(last_name__icontains=self.search_value) | \
                    Q(username__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return forms.SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_related_by = 5
    paginate_related_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_paid_filter = self.request.GET.get('is_paid')

        transactions = models.Transaction.objects.filter(user=self.object)
        if is_paid_filter is not None:
            is_paid = is_paid_filter == 'true'
            transactions = transactions.filter(is_paid=is_paid)

        context['transactions'] = transactions
        return context
