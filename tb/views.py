from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework import generics, status, authentication, permissions
from .serializers import StudentSerializer, TeacherSerializer, AuthTokenSerializer

from .models import Rol, Course


class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentSerializer


class TeacherCreateView(generics.CreateAPIView):
    serializer_class = TeacherSerializer


class RolListView(generics.ListAPIView):
    queryset = Rol.objects.all()

    def list(self, request, *args, **kwargs):
        roles = self.get_queryset()
        role_data = [{"id": role.id, "name": role.name} for role in roles]
        return Response(role_data, status=status.HTTP_200_OK)


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer


class LoginView(generics.RetrieveAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, "student"):
            serializer = StudentSerializer(user.student)
        elif hasattr(user, "teacher"):
            serializer = TeacherSerializer(user.teacher)
        else:
            return Response({"detail": "Login no permitido."}, status=404)

        return Response(serializer.data)


class LogoutView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            user.auth_token.delete()  # Elimina el token del usuario
            logout(request)  # Realiza el logout del usuario
            return Response({"message": "Logout exitoso."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)


class TeacherCourseView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "student"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            teacher = user.teacher
            course = Course()
            course.create(request.data["name"], teacher)
            return Response({"message": "Curso creado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)


class StudentCourseView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "teacher"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            student = user.student
            course = Course.objects.filter(code=request.data["code"]).get()
            course.add_student(student)
            return Response({"message": "Estudiante asignado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)
