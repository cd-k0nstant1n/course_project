from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import auth, User
from .models import CustomUser, Appointment, Code
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import *
import re, string, random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from datetime import datetime, timezone

# Create your views here.
def generate_code():
    characters = string.ascii_letters + string.digits + string.punctuation
    random_code = ''.join(random.choice(characters) for _ in range(50))
    Code.objects.update_or_create(id=1, defaults={'code': random_code})
    
def index(request):
    if request.method == 'POST':
        form = send_email_form(request.POST)
        
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            send_mail(subject, message,settings.EMAIL_HOST_USER,  [settings.EMAIL_HOST_USER], fail_silently=False)
            return redirect('index')
    else:
        form = send_email_form()
    
    if request.method == 'POST' and 'generate_code' in request.POST:
        generate_code()
        return redirect('index')

    code = Code.objects.get(id=1)

    context = {
        'form': form, 
        'code': code
    }
    
    return render(request, 'index.html', context)



def register(request):
    if request.method == 'POST':
        role = request.POST['role']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        gender = request.POST['gender']
        birthday = request.POST['birthday']
        regex_pass = re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
        regex_email = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        if not regex_pass.match(pass1):
            messages.info(request, 'Паролата трябва да е поне 8 символа дълга и да съдържа букви и цифри.')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Този имейл вече съществува')
            return redirect('register')
        elif not regex_email.match(email):
            messages.info(request, 'Този имейл е невалиден')
            return redirect('register')
        elif CustomUser.objects.filter(phone=phone).exists():
            messages.info(request, 'Този телефон вече се използва')
            return redirect('register')
        
        if role == 'doctor':
            code = request.POST['code']
            if not Code.objects.filter(code=code).exists():
                messages.info(request, 'Невалиден код за доктор.')
                return redirect('register')
            else:
                generate_code()
        
        user = User.objects.create_user(username=email, email=email, password=pass1, first_name=fname, last_name=lname)
        if role == 'patient':
            CustomUser.objects.create(user=user, phone=phone, role=role, gender=gender, date_of_birth=birthday)
            return redirect('login')
        else:
            specialty = request.POST['specialty']
            room = request.POST['room']
            if CustomUser.objects.filter(room_num=room).exists():
                CustomUser.objects.create(user=user, phone=phone, role=role, specialty=specialty, gender=gender, date_of_birth=birthday, room_num=room)
            else:
                messages.info(request, 'Tази стая вече е използвана.')
                return redirect('register')
              
            return redirect('login')

    return render(request, 'RegistrationForm.html')
        
def registerPatient(request):
    return render(request, 'registerPatient.html')

def registerDoctor(request):
    return render(request, 'registerDoctor.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            try:
                user = User.objects.get(username=email)
                if check_password(password, user.password):
                    auth.login(request, user)
                    return redirect('/')
                else:
                    messages.info(request, 'Невалидна информация')
                    return redirect('login')
            except User.DoesNotExist:
                messages.info(request, 'Невалидна информация')
                return redirect('login')
    else:
        return render(request, 'login.html')

 
def logout(request):
    auth.logout(request)
    return redirect('login')

def aboutus(request):
    return render(request,'aboutus.html')

def appointments(request):

    if request.method == 'POST':
        user_role = request.POST['role']
        appointment_id = request.POST['appointment_id']
        
        if user_role == 'admin':
            action = request.POST.get('action', '')
            
            appointment = get_object_or_404(Appointment, id=appointment_id) 
            
            if action == 'delete':
                appointment.delete()
            else:
                status = request.POST['status']
                appointment.status = status
                appointment.save()              
            return redirect('appointments')   
        elif user_role == 'doctor':    
            status = request.POST['status']
            Appointment.objects.filter(id=appointment_id).update(status=status)   
        elif user_role == 'patient':
            appointment_id = request.POST['appointment_id']
            appointment = get_object_or_404(Appointment, id=appointment_id)
            status = request.POST['status']
            
            if status == 'Преглежда се' and not Appointment.objects.filter(doctor=appointment.doctor, appointment_date=appointment.appointment_date, appointment_time=appointment.appointment_time).exclude(status='Отказан').exists():
                Appointment.objects.filter(id=appointment_id).update(status=status)
            elif status == 'Преглежда се' and Appointment.objects.filter(doctor=appointment.doctor, appointment_date=appointment.appointment_date, appointment_time=appointment.appointment_time).exists():
                messages.info(request, 'Часът вече е зает')
            else:
                Appointment.objects.filter(id=appointment_id).update(status=status)
        return redirect('appointments')
    
    if request.user.is_authenticated:
        user_email = request.user.email
        patient_appointments = Appointment.objects.filter(patient__user__email=user_email)
        doctor_appointments = Appointment.objects.filter(doctor__user__email=user_email)
        appointments = Appointment.objects.all()
        context = {
                   'appointments' : appointments,
                   'patient_appointments': patient_appointments,
                   'doctor_appointments' : doctor_appointments
                   }
        return render(request, 'appointments.html', context)
    else:
        html_content = """
            <br><br><br><br><br>
            <p><strong> Влезте или се регистирайте за да видите графика си.</strong></p>
            <br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
        """
    
    return render(request, 'appointments.html', {'html_content' : html_content})

def edit_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        # Handle the form submission to update appointment details
        changed_service = request.POST.get('changed_service')
        changed_appointment_date = request.POST.get('changed_appointment_date')
        changed_appointment_time = request.POST.get('changed_appointment_time')
        changed_details = request.POST.get('changed_details')

        # Check if any change is detected
        if (changed_service is not None or
            changed_appointment_date is not None or
            changed_appointment_time is not None or
            changed_details is not None):

            # Create a dictionary to hold the changes
            updates = {}

            # Check and process each change individually
            if changed_service is not None:
                updates['service'] = changed_service

            if changed_appointment_date is not None and changed_appointment_date != '':
                appointment_datetime = datetime.strptime(changed_appointment_date, "%Y-%m-%d")
                if appointment_datetime.date() < datetime.now().date():
                    messages.info(request, 'Датата не трябва да е минала.')
                    return redirect('edit_appointment', appointment_id=appointment_id)
                else:
                    updates['appointment_date'] = appointment_datetime

            if changed_appointment_time is not None:
                updates['appointment_time'] = changed_appointment_time

            if changed_details is not None:
                updates['details'] = changed_details

            # Check if the new appointment date, time, and doctor combination exists in another non-canceled appointment
            if 'appointment_date' in updates or 'appointment_time' in updates:
                existing_appointment = Appointment.objects.filter(
                    doctor=appointment.doctor,
                    appointment_date=updates.get('appointment_date', appointment.appointment_date),
                    appointment_time=updates.get('appointment_time', appointment.appointment_time),
                ).exclude(id=appointment_id).exclude(status='Отказан').exists()

                # If there's a conflict, display a message and redirect back to the edit page
                if existing_appointment:
                    messages.error(request, 'Час със същата дата и време вече съществуват.')
                    return redirect('edit_appointment', appointment_id=appointment_id)

            # Update the appointment with all the changes
            Appointment.objects.filter(id=appointment_id).update(**updates)

            return redirect('appointments')

    return render(request, 'edit_appointment.html', {'appointment': appointment})


@login_required
def profilePage(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = request.user
        regex_pass = re.compile('^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

        if not user.check_password(current_password):
            messages.info(request, 'Невалидна настояща парола.')
            return redirect('profile')    
        elif not regex_pass.match(new_password):
            messages.info(request, 'Новата парола трябва да е поне 8 символа дълга и да съдържа букви и цифри.')
            return redirect('profile')
        elif current_password == new_password:
            messages.info(request, "Новата парола не може да е същата като старата.")
            return redirect('profile')
        elif new_password != confirm_password:
            messages.info(request, "Паролите не съвпадат.")
            return redirect('profile')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.info(request, 'Успешно променихте паролата си.')
            return redirect('profile')
                 
    return render(request, 'profile.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
           return HttpResponse("Този имейл не същесвува.")

        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
        user.password = make_password(temp_password)
        user.save()

        send_mail(
            subject="Вашата временна парола",
            message=f"Това е вашата времената ви парола може да се смени при влизане в профила ви от профил страницата: {temp_password}",
            from_email="medicure.bg@gmail.com",
            recipient_list=[email],
        )            
        messages.info(request, 'Успешно променихте паролата си.')
        return redirect('login')
    
    return render(request, 'reset_password.html')


