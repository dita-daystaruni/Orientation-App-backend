from django.urls import path
from .views import FAQList, FAQDetail, faqs_view

urlpatterns = [
    path('faqs/', FAQList.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', FAQDetail.as_view(), name='faq-detail'),
    path('faqs_view/', faqs_view, name='faqs'),
]