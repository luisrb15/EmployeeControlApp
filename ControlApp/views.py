from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Employee, Attendance
from .forms import EmployeeForm

year = datetime.now().year

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ControlApp:dashboard')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'is_user': False,'error_message': error_message, 'year':year})
    else:
        return render(request, 'login.html', {'is_user': False,'year':year})

@login_required
def logout_view(request):
    logout(request)
    return redirect('ControlApp:login')

@login_required
def dashboard(request):
    name = f'{request.user.employee.name} {request.user.employee.last_name}'
    is_present = request.user.employee.is_present
    context = {'is_user': True,'name': name, 'is_present': is_present, 'year': year}
    return render(request, 'dashboard.html', context)

@login_required
def attendance(request):
    if request.method == 'POST':    
        employee_id = request.user.employee.id
        employee = Employee.objects.get(pk=employee_id)
        if request.user.employee.is_present:
            last_attendance = Attendance.objects.filter(employee=employee).last()
            if last_attendance:
                last_attendance.time_out = datetime.now()
                last_attendance.save()
            employee.is_present = False
            employee.save()
        else:     
            time_in = datetime.now()
            attendance = Attendance(employee=employee, time_in=time_in)
            employee.is_present = True
            employee.save()
            attendance.save()
        employee = Employee.objects.get(pk=employee_id)
        return redirect('ControlApp:thanks')
    else:
        employees = Employee.objects.all()
        context = {'is_user': True,'employees': employees, 'year':year}
        return render(request, 'attendance.html', context)

@login_required
def thanks(request):
    context = {'is_user': True,'present': request.user.employee.is_present, 'year':year}
    return render(request, 'thanks.html', context)

@staff_member_required
def employee_days(request, id):
    employee = Employee.objects.get(id=id)
    attendances = Attendance.objects.filter(employee=employee)
    context = {'is_user': True,'employee': employee, 'attendances': attendances, 'year': year}
    return render(request, 'employee_days.html', context)

@staff_member_required
def search_employee(request):
    employees = Employee.objects.all()
    context = {'is_user': True,'employees': employees, 'year': year}
    return render(request, 'search.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_form.save()
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
        
            return redirect('ControlApp:dashboard')
    else:
        form = UserCreationForm()
        employee_form = EmployeeForm()
    context={'form': form, 'employee_form': employee_form ,'year': year}
    return render(request, 'register.html', context)