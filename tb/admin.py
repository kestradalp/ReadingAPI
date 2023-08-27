from django.contrib import admin
from tb.models import *

# Register your models here.

admin.site.register([Rol, User, Teacher, Student, Course])
