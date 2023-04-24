from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import UserList, UserDetail


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/users/', UserList.as_view(), name='users'),
    path('accounts/detail/<int:pk>/', UserDetail.as_view(), name="detail"),
]