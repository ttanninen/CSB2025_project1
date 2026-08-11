from django.contrib import admin
from .models import Course, Student, Enrollment

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Enrollment)