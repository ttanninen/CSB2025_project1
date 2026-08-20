from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("quiz/<int:course_id>", views.quiz, name="quiz"),
    path("results/<int:submission_id>", views.results, name="results"),

]