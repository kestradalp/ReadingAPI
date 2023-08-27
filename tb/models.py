from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Create your models here.
class Rol(models.Model):
    name = models.CharField(max_length=10)


class UserManager(BaseUserManager):
    def create_user(self, fullname, email, password, **extra_fields):
        if not email:
            raise ValueError("Falta email")
        user = self.model(email=self.normalize_email(email))
        user = self.model(email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, fullname, email, password, **extra_fields):
        extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}
        user = self.create_user(fullname, email, password, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name="users", null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Student(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    cdi = models.CharField(max_length=13)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="student")

    def create(self, email, password, fullname, age, cdi):
        user = User.objects.create_user(fullname, email, password)
        user.rol = Rol.objects.get(name="Estudiante")
        user.save()
        self.fullname = fullname
        self.age = age
        self.cdi = cdi
        self.user = user
        self.save()
        return self


class Teacher(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField()
    cdi = models.CharField(max_length=13)
    title = models.CharField(max_length=150)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="teacher")

    def create(self, email, password, fullname, age, cdi, title):
        user = User.objects.create_user(fullname, email, password)
        user.rol = Rol.objects.get(name="Profesor")
        user.save()
        self.fullname = fullname
        self.age = age
        self.cdi = cdi
        self.title = title
        self.user = user
        self.save()
        return self


class Course(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=5, null=False, blank=False, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT, related_name="course")
    students = models.ManyToManyField(Student, related_name="courses", null=True)

    def create(self, name, teacher):
        self.code = str(uuid.uuid4())[:5]
        self.name = name
        self.teacher = teacher
        self.save()
        return self

    def add_student(self, student):
        self.students.add(student)
        self.save()
        return self


class Book(models.Model):
    name = models.CharField(max_length=150)
    student = models.OneToOneField(Student, on_delete=models.PROTECT, related_name="book")

    def create(self, name, student):
        self.name = name
        self.student = student


class Lecture(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT, related_name="lectures")
    time_lecture = models.DateTimeField()

    def create(self, book, time):
        self.book = book
        self.time_lecture = time
