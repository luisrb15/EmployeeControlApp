from django.shortcuts import render
from datetime import datetime
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Employee, Attendance

year = datetime.now().year

def home(request):
    return render(request, 'home.html', {'year': year})

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
            return render(request, 'login.html', {'error_message': error_message, 'year':year})
    else:
        return render(request, 'login.html', {'year':year})

@login_required
def logout_view(request):
    logout(request)
    return redirect('ControlApp:login')

@login_required
def dashboard(request):
    print('----------\n', 'estoy en dashboard\n', '---------')
    name = f'{request.user.employee.name} {request.user.employee.last_name}'
    is_present = request.user.employee.is_present
    context = {'name': name, 'is_present': is_present, 'year': year}
    return render(request, 'dashboard.html', context)

@login_required
def attendance(request):
    print('--------', '\n' ,request, '\n', '---------')
    if request.method == 'POST':
        print('--------\n', 'METHOD POST' ,request.POST, '\n', '---------')
        print('--------\n', 'employee id' ,request.user.employee.id, '\n', '---------')
        print('--------\n', 'employee date joined' ,request.user.employee.date_joined, '\n', '---------')
        print('--------\n', 'employee is present' ,request.user.employee.is_present, '\n', '---------')
        
        employee_id = request.user.employee.id
        employee = Employee.objects.get(pk=employee_id)
        if request.user.employee.is_present:
            last_attendance = Attendance.objects.filter(employee=employee).last()
            if last_attendance:
                last_attendance.time_out = datetime.now()
                last_attendance.save()
            employee.is_present = False
            employee.save()
            print('--------\n', 'employee',employee, '\n---------')
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
        context = {'employees': employees, 'year':year}
        return render(request, 'attendance.html', context)

@login_required
def thanks(request):
    print('--------\n is present?', request.user.employee.is_present, '\n---------')
    context = {'present': request.user.employee.is_present, 'year':year}
    return render(request, 'thanks.html', context)

@staff_member_required
def employee_days(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    attendances = Attendance.objects.filter(employee=employee)
    context = {'employee': employee, 'attendances': attendances, 'year': year}
    return render(request, 'employee_days.html', context)

@staff_member_required
def search_employee(request):
    employees = Employee.objects.all()
    context = {'employees': employees, 'year': year}
    return render(request, 'search.html', context)