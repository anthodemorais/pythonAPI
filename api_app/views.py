from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from .serializers import StudentSerializer, TeacherSerializer, ProjectGroupSerializer, ProjectSerializer
from .models import Student, Teacher, ProjectGroup, Project
from django.contrib.auth.models import User
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.decorators import action


# def create_student(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         data["user"] = Student.objects.filter(username=data["username"])
#         serializer = StudentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# def create_teacher(request):
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         data["user"] = Teacher.objects.filter(username=data["username"])
#         serializer = TeacherSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

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
            return Project.objects.filter(owner=self.request.user)
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdmin]
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
            return ProjectGroup.objects.filter(owner=self.request.user)
    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=True, methods=['post'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        if request.data.teacher != None:
            teacher = Teacher(user=user)
            teacher.save()
        else:
            student = Student(user=user)
            student.save()
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
                        status=status.HTTP_201_CREATED,
                        headers=headers)