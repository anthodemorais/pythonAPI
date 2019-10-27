from rest_framework import routers
from django.urls import include, path
from . import views

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewset)
router.register(r'teachers', views.TeacherViewset)
router.register(r'groups', views.ProjectGroupViewset)
router.register(r'projects', views.ProjectViewset)

urlpatterns = [
    #path('users/', views.UserListView.as_view()),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/', include('rest_auth.urls')),
    path('', include(router.urls)),
]