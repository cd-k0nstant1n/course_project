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

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = send_email_form(request.POST)
        
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(subject, message, email, ['medicure.bg@gmail.com'])
            return redirect('index')
    else:
        form = send_email_form()
    
    if request.method == 'POST' and 'generate_code' in request.POST:
        characters = string.ascii_letters + string.digits + string.punctuation
        random_code = ''.join(random.choice(characters) for _ in range(50))
        Code.objects.update_or_create(id=1, defaults={'code': random_code})
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

        user = User.objects.create_user(username=email, email=email, password=pass1, first_name=fname, last_name=lname)
        if role == 'patient':
            CustomUser.objects.create(user=user, phone=phone, role=role, gender=gender, date_of_birth=birthday)
            return redirect('login')
        else:
            specialty = request.POST['specialty']
            CustomUser.objects.create(user=user, phone=phone, role=role, specialty=specialty, gender=gender, date_of_birth=birthday)
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
                    messages.info(request, 'Credentials invalid')
                    return redirect('login')
            except User.DoesNotExist:
                messages.info(request, 'Credentials invalid')
                return redirect('login')
    else:
        return render(request, 'login.html')

 
def logout(request):
    auth.logout(request)
    return redirect('login')

def aboutus(request):
    return render(request,'aboutus.html')

def doctors(request):

    return render(request, 'doctors.html')

def profilePage(request):
    return render(request, 'profile.html')

