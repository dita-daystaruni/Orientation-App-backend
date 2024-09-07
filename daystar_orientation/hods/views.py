from rest_framework import generics
from .models import HOD, Course
from .serializers import HODSearializer, CourseSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import HODForm
from django.contrib import messages
from account.models import Account

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
    hods_list = HOD.objects.all().order_by('id')
    paginator = Paginator(hods_list, 10)
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
        
        try:
            course = Course.objects.get(name=course_name)
            
            HOD.objects.create(
                first_name=first_name,
                last_name=last_name,
                title=title,
                course=course,
                phone_number=phone_number,
                email=email
            )
            messages.success(request, 'HOD added successfully.')
        except Course.DoesNotExist:
            messages.error(request, f"Course '{course_name}' does not exist.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return redirect('courses_details')
    
    courses = Course.objects.all()
    return render(request, 'course-details_add.html', {'courses': courses})

@login_required
def hodsedit_view(request, pk):
    hod = get_object_or_404(HOD, pk=pk)
    if request.method == 'POST':
        form = HODForm(request.POST, instance=hod)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'HOD updated successfully.')
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
            return redirect('courses_details')
    else:
        form = HODForm(instance=hod)
    return render(request, 'course-details_edit.html', {'form': form})

@login_required
def hod_delete(request, pk):
    hod = get_object_or_404(HOD, pk=pk)
    try:
        hod.delete()
        messages.success(request, 'HOD deleted successfully.')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return redirect('courses_details')

@login_required
def stats_view(request):
    selected_course = request.GET.get('course', 'Theology')
    course = Course.objects.get(name=selected_course)
    
    total_students = Account.objects.filter(course=course, user_type='regular').count()
    male_students = Account.objects.filter(course=course, user_type='regular', gender='Male').count()
    female_students = Account.objects.filter(course=course, user_type='regular', gender='Female').count()
    nairobi_campus = Account.objects.filter(course=course, user_type='regular', campus='Nairobi').count()
    athi_river_campus = Account.objects.filter(course=course, user_type='regular', campus='Athi river').count()
    dayscholars = Account.objects.filter(course=course, user_type='regular', accomodation='Dayscholar').count()
    boarders = Account.objects.filter(course=course, user_type='regular', accomodation='Boarder').count()

    context = {
        'courses': Course.objects.all(),
        'selected_course': selected_course,
        'total_students': total_students,
        'male_students': male_students,
        'female_students': female_students,
        'nairobi_campus': nairobi_campus,
        'athi_river_campus': athi_river_campus,
        'dayscholars': dayscholars,
        'boarders': boarders,
    }

    return render(request, 'course_stats.html', context)