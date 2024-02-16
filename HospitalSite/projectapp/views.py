from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import auth, User
from .models import CustomUser, Appointment, Code
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import *
import re, string, random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.conf import settings

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
    
    return render(request, 'index.html', {'form': form, 'code': code})



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
    user_email = request.user.email
    appointments = Appointment.objects.filter(patient__user__email=user_email)
    
    return render(request, 'appointments.html', {'appointments': appointments})

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
            message=f"Това е вашата времена парола може да се смени при влизане от профил страницата: {temp_password}",
            from_email="medicure.bg@gmail.com",
            recipient_list=[email],
        )            
        messages.info(request, 'Успешно променихте паролата си.')
        return redirect('login')
    
    return render(request, 'reset_password.html')


