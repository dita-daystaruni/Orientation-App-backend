from django.urls import path
from . import views

urlpatterns = [
    path('faqs/', views.FAQList.as_view()),
    path('faqs/<int:pk>/', views.FAQDetail.as_view()),
]