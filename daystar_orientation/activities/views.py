from rest_framework import generics
from .models import Activity
from .serializers import ActivitySerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedReadOnly
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from .forms import ActivityForm
from django.contrib import messages

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
        try:
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

            messages.success(request, 'Activity added successfully.')
            return redirect('activities')
        
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('activities_add')

    return render(request, 'schedule_add.html')

@login_required
def activitiesedit_view(request, id):
    activity = get_object_or_404(Activity, id=id)

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            try:
                # Calculate the end_time based on start_time and duration
                duration = form.cleaned_data['duration']
                start_time = form.cleaned_data['start_time']
                end_time = (timezone.datetime.combine(activity.date, start_time) + timezone.timedelta(hours=duration)).time()
                activity.end_time = end_time

                form.save()
                messages.success(request, 'Activity updated successfully.')
                return redirect('activities')
            
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ActivityForm(instance=activity)

        form.fields['date'].initial = activity.date
        form.fields['start_time'].initial = activity.start_time
        form.fields['duration'].initial = (timezone.datetime.combine(activity.date, activity.end_time) - timezone.datetime.combine(activity.date, activity.start_time)).total_seconds() / 3600
        form.fields['is_session'].initial = activity.is_session

    context = {
        'activity': activity,
        'form': form,
    }
    return render(request, 'schedule_edit.html', context)

@login_required
def activities_delete_view(request, id):
    activity = get_object_or_404(Activity, id=id)
    try:
        activity.delete()
        messages.success(request, 'Activity has been deleted successfully.')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
    return redirect('activities')
