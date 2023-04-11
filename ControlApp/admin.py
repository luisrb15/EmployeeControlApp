from django.contrib import admin
from .models import Attendance, Employee

# Register your models here.
admin.site.register(Employee)
admin.site.register(Attendance)
