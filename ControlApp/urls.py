from django.urls import path
from . import views

app_name = 'ControlApp'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('attendance/', views.attendance, name='attendance'),
    path('thanks/', views.thanks, name='thanks'),
    path('search/', views.search_employee, name='search'),
    path('search/<int:id>/', views.employee_days, name='employee_days'),
    path('register/', views.register, name='register')
]
