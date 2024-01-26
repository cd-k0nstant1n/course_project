from .models import CustomUser, Appointment
from django.contrib import messages

def add_user_profile(request):
    if request.user.is_authenticated:
        user_profile = CustomUser.objects.get(user=request.user)
        return {'user_profile': user_profile}
    return {}

def add_popup(request):
    if request.method == 'POST':
        patient_name = request.user
        doctor = request.POST['doctor']
        service = request.POST['service']        
        details = request.POST['symptoms']        
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        
        try:
            patient = CustomUser.objects.get(user=patient_name, role='patient')
            selected_doctor = CustomUser.objects.get(user__last_name=doctor, role='doctor')

            if not Appointment.objects.filter(doctor=selected_doctor, appointment_date=appointment_date, appointment_time=appointment_time).exists():
                Appointment.objects.create(patient=patient, doctor=selected_doctor, appointment_date=appointment_date, appointment_time=appointment_time, service=service, details=details)
            else:
                messages.info(request, 'This date and time are already taken.')

        except Exception as e:
            return messages.info(request, f'Error: {str(e)}')       
        

    doctors = CustomUser.objects.filter(role='doctor')
    doctor_info = [{'last_name' : profile.user.last_name} for profile in doctors]
    

    return {'doctor_info' : doctor_info}