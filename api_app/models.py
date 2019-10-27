from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ProjectGroup(models.Model):
    users = models.ManyToManyField(Student)

class Project(models.Model):
    group = models.ForeignKey(ProjectGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()