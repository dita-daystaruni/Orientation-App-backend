from django import forms

class UploadFileForm(forms.Form):
    DATA_TYPE_CHOICES = [
        ('student', 'Account'),
        ('schedule', 'Activity'),
        ('notification', 'Notification'),
        ('hod', 'HOD'),
        ('faq', 'FAQ'),
    ]
    file = forms.FileField()
    data_type = forms.ChoiceField(choices=DATA_TYPE_CHOICES)
