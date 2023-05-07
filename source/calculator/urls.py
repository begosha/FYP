from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('cash-desk/', views.CashierView.as_view(), name='cashier'),
    path('positions/', views.PositionView.as_view(), name='positions'),
    path('transaction/', views.TransactionView.as_view(), name='transaction'),
]
