from django.urls import path
from . import views

urlpatterns = [
    path('accounts/', views.AccountList.as_view(), name='account-list'),
    path('accounts/<int:pk>/', views.AccountDetail.as_view(), name='account-detail'),
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('confirm-email/<uidb64>/<token>/', views.EmailConfirmationView.as_view(), name='email-confirmation'),
]