from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('registerPatient', views.registerPatient, name='registerPatient'),
    path('registerDoctor', views.registerDoctor, name='registerDoctor'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('aboutus', views.aboutus, name='aboutus'),
    path('doctors', views.doctors, name='doctors')
]
