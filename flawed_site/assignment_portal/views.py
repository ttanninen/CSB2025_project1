from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.db import connection

from .models import Course, Submission


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # FLAW A07 Identification and Authentication Failures
        
        user = User.objects.create_user(
            username=username,
            password=password
        )
        

        # FLAW A07 fix
        '''
        try:
            validate_password(password)

        except ValidationError as error:
            return render(request, "assignment_portal/register.html", {"error": error, "username": username})

        user = User.objects.create_user(
            username=username,
            password=password
        )
        '''
        login(request, user)

        return redirect("index")

    return render(request, "assignment_portal/register.html")


@login_required
def index(request):
    search = request.GET.get("search", "")
    if search:
        # FLAW A03 Injection
        with connection.cursor() as c:
            c.execute(
                "SELECT id, name FROM assignment_portal_course "
                "WHERE is_public = 1 AND name LIKE '%" + search + "%'"
            )
            rows = c.fetchall()

        courses = [{"id": row[0], "name": row[1]} for row in rows]

        # FLAW A03 fix
        '''
        courses = Course.objects.filter(
            name__icontains = search,
            is_public = True
        )
        '''

    else:
        courses = Course.objects.filter(is_public = True)

    student = request.user

    submissions = Submission.objects.filter(
        student=request.user
    ).select_related("course")

    return render(request, "assignment_portal/index.html",
                  {"courses": courses, "student": student, "submissions": submissions, "search": search})


@login_required
def quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if Submission.objects.filter(
        student=request.user,
        course=course
    ).exists():

        return redirect("index")

    questions = course.questions.all()

    if request.method == "POST":
        points = 0

        for question in questions:
            answer_id = request.POST.get(
                f"question_{question.id}"
            )

            if answer_id:
                answer = get_object_or_404(
                    question.answers,
                    id=answer_id
                )

                if answer.is_correct:
                    points += 1

        Submission.objects.create(
            student=request.user,
            course=course,
            points=points
        )
        return redirect("index")

    return render(request, "assignment_portal/quiz.html",
                  {"course": course, "questions": questions})


@login_required
def results(request, submission_id):
    
    # FLAW A01 Broken Access Control
    submission = get_object_or_404(
        Submission,
        id=submission_id
    )

    # FLAW A01 fix
    '''
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        student = request.user
    )
    '''

    return render(request, "assignment_portal/results.html",
                  {"submission": submission})


@login_required
def browse(request):
    courses = Course.objects.filter(is_public = True)
    return render(request, "assignment_portal/browse.html",
                  {"courses": courses})
