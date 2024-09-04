from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
import pandas as pd
from django.db import transaction
from .forms import UploadFileForm
from activities.models import Activity
from account.models import Account
from notifications.models import Notification
from hods.models import HOD
from hods.models import Course

class FAQList(generics.ListCreateAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(FAQList, self).get_permissions()

class FAQDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(FAQDetail, self).get_permissions()

# Web views 
@login_required
def faqs_view(request):
    faqs = FAQ.objects.all().order_by('-id')
    paginator = Paginator(faqs, 10) 
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'faqs.html', {'page_obj': page_obj})


def add_faq(request):
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        try:
            FAQ.objects.create(question=question, answer=answer)
            messages.success(request, 'FAQ added successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('faqs')

def edit_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    if request.method == 'POST':
        try:
            faq.question = request.POST['question']
            faq.answer = request.POST['answer']
            faq.save()
            messages.success(request, 'FAQ updated successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('faqs')
    
    return render(request, 'faqs.html', {'faq': faq})

def delete_faq(request, id):
    faq = get_object_or_404(FAQ, id=id)
    try:
        faq.delete()
        messages.success(request, 'FAQ deleted successfully.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    return redirect('faqs')

def handle_uploaded_file(f, data_type):
    if f.name.endswith('.xlsx'):
        df = pd.read_excel(f)
    else:
        df = pd.read_csv(f)

    try:
        with transaction.atomic():
            if data_type == 'student':
                for _, row in df.iterrows():
                    course_name = row['course']
                    course_instance = Course.objects.get(name=course_name)

                    if not Account.objects.filter(admission_number=row['admission_number'], email=row['email']).exists():
                        Account.objects.create(
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            email=row['email'],
                            gender=row['gender'],
                            phone_number=row['phone_number'],
                            admission_number=row['admission_number'],
                            course=course_instance, 
                            campus=row['campus'],
                            accomodation=row['accomodation'],
                        )
            elif data_type == 'schedule':
                for _, row in df.iterrows():
                    if not Activity.objects.filter(title=row['title'], description=row['description']).exists():
                        Activity.objects.create(
                            title=row['title'],
                            description=row['description'],
                            date=row['date'],
                            location=row['location'],
                            start_time=row['start_time'],
                            end_time=row['end_time'],
                            is_session=row['is_session'],
                        )
            elif data_type == 'notification':
                for _, row in df.iterrows():
                    if not Notification.objects.filter(title=row['title'], description=row['description']).exists():
                        Notification.objects.create(
                            title=row['title'],
                            description=row['description'],
                            is_admin_viewer=row['is_admin_viewer'],
                            is_parent_viewer=row['is_parent_viewer'],
                            is_regular_viewer=row['is_regular_viewer'],
                        )
            elif data_type == 'hod':
                for _, row in df.iterrows():
                    course_name = row['course']
                    course_instance = Course.objects.get(name=course_name)

                    if not HOD.objects.filter(email=row['email']).exists():
                        HOD.objects.create(
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            course=course_instance, 
                            phone_number=row['phone_number'],
                            email=row['email'],
                        )
            elif data_type == 'faq':
                for _, row in df.iterrows():
                    if not FAQ.objects.filter(question=row['question']).exists():
                        FAQ.objects.create(
                            question=row['question'],
                            answer=row['answer'],
                        )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['file'], form.cleaned_data['data_type'])
                messages.success(request, 'File uploaded and processed successfully!')
                return render(request, 'data_upload')
            except Exception as e:
                messages.error(request, f"An error occurred during file processing: {e}")
                return render(request, 'data_upload')
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})
