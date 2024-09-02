from django import forms
from .models import Activity
from django.utils import timezone

class ActivityForm(forms.ModelForm):
    duration = forms.IntegerField(help_text="Duration in hours") 

    class Meta:
        model = Activity
        fields = ['date', 'start_time', 'title', 'location', 'description', 'is_session']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing an existing activity, calculate the duration
        if self.instance and self.instance.pk and self.instance.start_time and self.instance.end_time:
            start_time = self.instance.start_time
            end_time = self.instance.end_time
            duration = (timezone.datetime.combine(self.instance.date, end_time) - timezone.datetime.combine(self.instance.date, start_time)).total_seconds() / 3600
            self.fields['duration'].initial = int(duration)
