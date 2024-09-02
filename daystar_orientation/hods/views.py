from rest_framework import generics
from .models import HOD, Course
from .serializers import HODSearializer, CourseSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .forms import HODForm 

class HODList(generics.ListCreateAPIView):
    queryset = HOD.objects.all()
    serializer_class = HODSearializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(HODList, self).get_permissions()

class HODDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = HOD.objects.all()
    serializer_class = HODSearializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(HODDetail, self).get_permissions()
    

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all() 
    serializer_class = CourseSerializer
    lookup_field = 'name'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super().get_permissions()
    
# Web views.
@login_required
def hodsdetails_view(request):
    hods_list = HOD.objects.all()
    paginator = Paginator(hods_list, 10)  # Show 10 HODs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'courses-details.html', {'hods': page_obj})

@login_required
def hodsadd_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST.get('last_name', '')
        title = request.POST['title']
        course_name = request.POST['course']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        
        course = Course.objects.get(name=course_name)
        
        HOD.objects.create(
            first_name=first_name,
            last_name=last_name,
            title=title,
            course=course,
            phone_number=phone_number,
            email=email
        )
        
        return redirect('course_details')
    
    courses = Course.objects.all()
    return render(request, 'course-details_add.html', {'courses': courses})


@login_required
def hodsedit_view(request, pk):
    hod = get_object_or_404(HOD, pk=pk)
    if request.method == 'POST':
        form = HODForm(request.POST, instance=hod)
        if form.is_valid():
            form.save()
            return redirect('courses_details')
    else:
        form = HODForm(instance=hod)
    return render(request, 'course-details_edit.html', {'form': form})

@login_required
def stats_view(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not authorized to view this page.")
    
    return render(request, 'course_stats.html')