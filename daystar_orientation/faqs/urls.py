from django.urls import path
from .views import FAQList, FAQDetail, faqs_view, add_faq, edit_faq, delete_faq, upload_file

urlpatterns = [
    path('faqs/', FAQList.as_view(), name='faq-list'),
    path('faqs/<int:pk>/', FAQDetail.as_view(), name='faq-detail'),
    path('faqs_view/', faqs_view, name='faqs'),
    path('faqs_view/add/', add_faq, name='add_faq'),
    path('faqs_view/edit/<int:id>/', edit_faq, name='edit_faq'),
    path('faqs_view/delete/<int:id>/', delete_faq, name='delete_faq'),
    path('upload/', upload_file, name='data_upload'),
]