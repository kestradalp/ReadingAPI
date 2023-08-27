# Generated by Django 4.2.4 on 2023-08-27 15:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("fullname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Rol",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fullname", models.CharField(max_length=100)),
                ("age", models.PositiveSmallIntegerField()),
                ("cdi", models.CharField(max_length=13)),
                ("title", models.CharField(max_length=150)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="teacher",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fullname", models.CharField(max_length=100)),
                ("age", models.PositiveSmallIntegerField()),
                ("cdi", models.CharField(max_length=13)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="student",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("code", models.CharField(max_length=5)),
                (
                    "students",
                    models.ManyToManyField(related_name="courses", to="tb.student"),
                ),
                (
                    "teacher",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="course",
                        to="tb.teacher",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                (
                    "time_lecture",
                    models.DecimalField(
                        blank=True, decimal_places=2, default=0, max_digits=6, null=True
                    ),
                ),
                (
                    "student",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="book",
                        to="tb.student",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="rol",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="users",
                to="tb.rol",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]