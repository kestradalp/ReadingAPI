# Generated by Django 4.2.4 on 2023-08-27 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tb", "0002_alter_course_students"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="code",
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
