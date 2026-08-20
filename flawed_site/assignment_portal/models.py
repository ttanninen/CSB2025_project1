from django.contrib.auth.models import User
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length = 70)

    def __str__(self):
        return self.name

class Question(models.Model):
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE,
        related_name="questions"
        )

    text = models.CharField(max_length=300, default="")

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    text = models.CharField(max_length=300, default="")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class Submission(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submissions"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.username} - {self.course.name}"