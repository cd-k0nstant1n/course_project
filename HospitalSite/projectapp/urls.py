from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('registerPatient', views.registerPatient, name='registerPatient'),
    path('registerDoctor', views.registerDoctor, name='registerDoctor'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('appointments', views.appointments, name='appointments'),
    path('edit_appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('profile', views.profilePage, name='profile'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('news/', views.news, name='news'),
    
    ]
