from .models import Student, Teacher, ProjectGroup, Project
from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer

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
        fields = ['users']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['group', 'name', 'description']

class RegisterSerializer(RegisterSerializer):
    def save(self, request):
        user = super().save(request)
        if "teacher" in request.data:
            teacher = Teacher(user=user)
            teacher.save()
            print("c")
        else:
            student = Student(user=user)
            student.save()
            print("d")
        return user