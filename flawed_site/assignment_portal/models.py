from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=70, default = "")
    number = models.CharField(max_length = 8)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length = 70)
    code = models.CharField(max_length = 8, default="00000000")

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"