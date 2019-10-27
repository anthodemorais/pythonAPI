from django.contrib import admin
from .models import Student, Teacher, Project, ProjectGroup

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Project)
admin.site.register(ProjectGroup)