from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Course, Submission


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username = username,
            password = password
        )

        login(request, user)

        return redirect("index")

    return render(request, "assignment_portal/register.html")

@login_required
def index(request):
    courses = Course.objects.all()
    student = request.user
    submissions = Submission.objects.filter(
        student=request.user
    ).select_related("course")
    return render(request, "assignment_portal/index.html", {"courses": courses, "student": student, "submissions": submissions})

@login_required
def quiz(request, course_id):
    course = get_object_or_404(Course, id = course_id)

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
                    id = answer_id
                )

                if answer.is_correct:
                    points += 1

        Submission.objects.create(
            student = request.user,
            course = course,
            points = points
        )
        return redirect("index")

    return render(request, "assignment_portal/quiz.html", {"course": course, "questions": questions})

@login_required
def results(request, submission_id):
    submission = get_object_or_404(
        Submission,
        id = submission_id
        )

    return render(request,"assignment_portal/results.html", {"submission": submission})