from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import viewsets, status
from .serializers import StudentSerializer, TeacherSerializer, ProjectGroupSerializer, ProjectSerializer
from .models import Student, Teacher, ProjectGroup, Project
from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class StudentViewset(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class TeacherViewset(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ProjectViewset(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        else:
            student = Student.objects.filter(user=self.request.user)
            groups = ProjectGroup.objects.filter(users__in=student)
            projects = Project.objects.filter(group__in=groups)
            return projects
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ProjectGroupViewset(viewsets.ModelViewSet):
    queryset = ProjectGroup.objects.all()
    serializer_class = ProjectGroupSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProjectGroup.objects.all()
        else:
            student = Student.objects.filter(user=self.request.user)
            return ProjectGroup.objects.filter(users__in=student)
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    def create(self, request):
        data = request.data
        group = ProjectGroup()
        group.save()
        if "users" not in request.data or len(request.data.users) == 0 or len(request.data) == 0:
            group.users.add(Student.objects.filter(user=request.user)[0])
        else:
            group.users.add(Student.objects.filter(user__in=request.data.users))
        serializer = ProjectGroupSerializer(group)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)