from django.shortcuts import render, get_object_or_404, redirect

from .models import Course, Question

def index(request):
    return render(request, 'assignment_portal/index.html')
