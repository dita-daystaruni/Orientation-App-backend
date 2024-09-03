from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render ,redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

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