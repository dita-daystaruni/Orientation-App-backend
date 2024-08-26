from django.contrib import admin

# Register your models here.
from .models import HOD
from .models import Course
admin.site.register(HOD)
admin.site.register(Course)