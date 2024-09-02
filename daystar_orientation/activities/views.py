from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import ActivityForm

class ActivityList(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(ActivityList, self).get_permissions()

class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAdminOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticatedReadOnly]
        return super(ActivityDetail, self).get_permissions()

# Web views 
@login_required
def activities_view(request):
    today = timezone.now().date()

    activities = Activity.objects.filter(date=today).order_by('start_time')

    paginator = Paginator(activities, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'activities': page_obj,  
    }
    return render(request, 'schedule.html', context)

@login_required
def activitiesadd_view(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        duration = int(request.POST.get('duration'))
        event_type = request.POST.get('event_type') 
        title = request.POST.get('title')
        location = request.POST.get('location')
        description = request.POST.get('description')
        
        start_time_obj = timezone.datetime.strptime(start_time, '%H:%M').time()
        end_time_obj = (timezone.datetime.combine(timezone.now(), start_time_obj) + timezone.timedelta(hours=duration)).time()

        is_session = True if event_type == 'session' else False

        new_activity = Activity(
            date=date,
            start_time=start_time_obj,
            end_time=end_time_obj,
            title=title,
            location=location,
            description=description,
            is_session=is_session
        )
        new_activity.save()

        # Redirect to the schedule list page after adding the activity
        return redirect('activities')

    return render(request, 'schedule_add.html')

@login_required
def activitiesedit_view(request , activity_id):
    activity = get_object_or_404(Activity, id=activity_id)

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            # Calculate the end_time based on start_time and duration
            duration = form.cleaned_data['duration']
            start_time = form.cleaned_data['start_time']
            end_time = (timezone.datetime.combine(activity.date, start_time) + timezone.timedelta(hours=duration)).time()
            activity.end_time = end_time

            form.save()
            return redirect('schedule_list') 

    else:
        form = ActivityForm(instance=activity)

    context = {
        'activity': activity,
        'form': form,
    }
    return render(request, 'schedule_edit.html', context)
