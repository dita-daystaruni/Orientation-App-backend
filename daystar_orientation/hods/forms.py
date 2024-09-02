from django import forms
from .models import HOD, Course

class HODForm(forms.ModelForm):
    class Meta:
        model = HOD
        fields = ['first_name', 'last_name', 'title', 'course', 'phone_number', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()
