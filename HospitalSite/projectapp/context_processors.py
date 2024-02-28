from .models import CustomUser, Appointment, Code
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

def add_user_profile(request):
    if request.user.is_authenticated:
        user_profile = CustomUser.objects.get(user=request.user)
        return {'user_profile': user_profile}
    return {}

def add_popup(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            patient_name = request.user
            doctor = request.POST.get('doctor')
            service = request.POST.get('service')       
            details = request.POST.get('symptoms')      
            appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')
        
            try:
                patient = CustomUser.objects.get(user=patient_name, role='patient')
                selected_doctor = CustomUser.objects.get(user__last_name=doctor, role='doctor')
            
                try:
                    appointment_datetime = datetime.strptime(appointment_date, "%Y-%m-%d") 
                except ValueError:
                    messages.info(request, 'Невалиден формат на дата.')
            
                if appointment_datetime.date() < datetime.now().date():
                    messages.info(request, 'Датата не трябва да е минала.')

                if not Appointment.objects.filter(doctor=selected_doctor, appointment_date=appointment_date, appointment_time=appointment_time).exclude(status='Отказан').exists():
                    Appointment.objects.create(patient=patient, doctor=selected_doctor, appointment_date=appointment_date, appointment_time=appointment_time, service=service, details=details)
                else:
                    messages.info(request, 'Час със същата дата и време вече съществуват.')

            except Exception as e:
                messages.info(request, f'Error: {str(e)}')       
        
    doctors = CustomUser.objects.filter(role='doctor')
    doctor_info = [{'last_name' : profile.user.last_name, 'specialty': profile.specialty} for profile in doctors]
    

    return {'doctor_info' : doctor_info}
