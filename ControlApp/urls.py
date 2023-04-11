from django.urls import path
from . import views

app_name = 'ControlApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance, name='attendance'),
    path('thanks/', views.thanks, name='thanks'),
    path('search/', views.search_employee, name='search'),
    path('search/<int:employee_id>/', views.employee_days, name='employee_days'),
]
