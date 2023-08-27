from django.urls import path
from .views import *

urlpatterns = [
    path("create/student/", StudentCreateView.as_view()),
    path("create/teacher/", TeacherCreateView.as_view()),
    path("list/roles/", RolListView.as_view()),
    path("user/", LoginView.as_view()),
    path("login/", CreateTokenView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("user/teacher/course/", TeacherCourseView.as_view()),
    path("user/student/course/", StudentCourseView.as_view())
    # Otras rutas y vistas aquí
]
