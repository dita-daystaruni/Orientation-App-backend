from django.core.management.base import BaseCommand
from hods.models import Course
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Load courses from a text file into the Course model'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'courses.txt')

        try:
            with open(file_path, 'r') as file:
                for line in file:
                    course_name = line.strip()
                    if course_name:
                        Course.objects.get_or_create(name=course_name)
            self.stdout.write(self.style.SUCCESS('Courses loaded successfully.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please check the file path.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
