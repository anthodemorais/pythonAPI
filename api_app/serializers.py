from .models import Student, Teacher, ProjectGroup, Project
from rest_framework import serializers


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['user']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['user']

class ProjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = ['usernames']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = ['group', 'name', 'description']