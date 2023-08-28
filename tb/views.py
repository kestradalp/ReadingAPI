from datetime import datetime
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework import generics, status, authentication, permissions
from .serializers import StudentSerializer, TeacherSerializer, AuthTokenSerializer

from .models import Rol, Course, Book, Lecture
import pytz


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

    def get(self, request, course_id=None):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "student"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)

            if course_id is None:
                courses = user.teacher.course.all()
                data_course = [
                    {"id": course.id, "name": course.name, "code": course.code, "students": course.students.all().count()} for course in courses
                ]
                return Response({"courses": data_course}, status=status.HTTP_200_OK)
            else:
                try:
                    course = user.teacher.course.get(pk=course_id)
                    data_course = {"id": course.id, "name": course.name, "code": course.code, "students": course.students.all().count()}
                    return Response({"course": data_course}, status=status.HTTP_200_OK)
                except Course.DoesNotExist:
                    return Response({"message": "El curso no existe."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)


class StudentCourseView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "teacher"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            student = user.student
            courser_student = [{"id": course.id, "name": course.name, "code": course.code} for course in student.courses.all()]
            return Response({"course": courser_student}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

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


class StudentBookView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id=None):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "teacher"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            student = user.student
            if not book_id:
                book_student = [
                    {"id": book.id, "name": book.name, "percentage": book.percentage, "pdf_url": book.pdf_url, "sound_url": book.sound_url}
                    for book in student.books.all()
                ]
                return Response({"books": book_student}, status=status.HTTP_200_OK)
            else:
                book = student.books.get(pk=book_id)
                book_student = {"id": book.id, "name": book.name, "percentage": book.percentage, "pdf_url": book.pdf_url, "sound_url": book.sound_url}
                return Response({"book": book_student}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "teacher"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            student = user.student
            book = Book()
            book.create(request.data["name"], student, request.data["percentage"])
            return Response({"message": "Libro creado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)


class StudenLectureView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "teacher"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            book = user.student.books.get(pk=book_id)
            lecture_book = [{"id": lecture.id, "time_lecture": lecture.time_lecture} for lecture in book.lectures.all()]
            return Response({"lecture": lecture_book}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, book_id):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, "teacher"):
                return Response({"message": "Usuario no autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
            book = user.student.books.get(pk=book_id)
            lecture = Lecture()
            datetime_ec = datetime.now(pytz.timezone("America/Guayaquil"))
            lecture.create(book, datetime_ec)
            return Response({"message": "Registro"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Usuario no autenticado."}, status=status.HTTP_401_UNAUTHORIZED)
