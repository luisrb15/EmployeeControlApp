from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20)
    date_joined = models.DateField(default='2020-01-01')
    is_present = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ' ' + self.last_name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_in = models.DateTimeField(null=True, blank=True)
    time_out = models.DateTimeField(null=True, blank=True)
    is_backup = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id) + '-' + str(self.employee)
