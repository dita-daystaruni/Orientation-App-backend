from django import forms
from .models import Account, Course

class StudentForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'gender', 'admission_number', 'course', 'phone_number', 'email', 'campus', 'accomodation', 'checked_in', 'parent']
        widgets = {
            'course': forms.Select(choices=[(course.name, course.name) for course in Course.objects.all()]),
            'gender': forms.RadioSelect(choices=Account.GENDER),
            'campus': forms.RadioSelect(choices=Account.CAMPUS_CHOICES),
            'accomodation': forms.RadioSelect(choices=Account.ACCOMODATION),
            'checked_in': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')]),
            'parent': forms.Select(choices=[(parent.id, f'{parent.first_name} {parent.last_name}') for parent in Account.objects.filter(user_type='parent')])
        }
