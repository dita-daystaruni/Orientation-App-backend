from django.urls import path
from . import views

urlpatterns = [
    path('faqs/', views.FAQList.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', views.FAQDetail.as_view(), name='faq-detail'),
]