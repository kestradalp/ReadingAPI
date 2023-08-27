from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Student, User, Teacher


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "fullname", "email", "password", "rol")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(email=validated_data["email"], rol=validated_data["rol"], fullname=validated_data["fullname"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ("id", "fullname", "age", "cdi", "user")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ("id", "fullname", "age", "cdi", "title", "user")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer().create(user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(request=self.context.get("request"), username=email, password=password)

        if not user:
            raise serializers.ValidationError("No se pudo autenticar", code="authorization")
        if user.is_superuser:
            raise serializers.ValidationError("No está permitido el acceso a superusuarios", code="authorization")

        data["user"] = user
        return data
