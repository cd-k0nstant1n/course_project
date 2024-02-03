from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import auth, User
from .models import CustomUser, Appointment
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.mail import send_mail
from .forms import *

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
    
    return render(request, 'index.html', {'form': form})



def register(request):
    if request.method == 'POST':
        role = request.POST['role']
        if role == 'patient':
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
        
            if pass1 == pass2:
                if User.objects.filter(email = email).exists():
                    messages.info(request, 'This email already exists')
                    return redirect('register')
                elif CustomUser.objects.filter(phone = phone).exists():
                    messages.info(request, 'Phone already used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=email, email=email, password=pass1, first_name=fname, last_name=lname)
                    CustomUser.objects.create(user=user, phone=phone, role=role, gender=gender, date_of_birth=birthday)
                    user.save();
                    return redirect('login')         
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('register')
        else:
            fname = request.POST['first_name']
            lname = request.POST['last_name']
            email = request.POST['email']
            phone = request.POST['phone']
            specialty = request.POST['specialty']
            pass1 = request.POST['pass1']
            pass2 = request.POST['pass2']
            gender = request.POST['gender']
            birthday = request.POST['birthday']
            # code = request.POST['code']
    
            if pass1 == pass2:
                if User.objects.filter(email = email).exists():
                    messages.info(request, 'This email already exists')
                    return redirect('register')
                elif CustomUser.objects.filter(phone = phone).exists():
                    messages.info(request, 'Phone already used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=email, email=email, password=pass1, first_name=fname, last_name=lname)
                    CustomUser.objects.create(user=user, phone=phone, role=role, specialty=specialty, gender=gender, date_of_birth=birthday)
                    user.save();
                    return redirect('login')         
            else:
                messages.info(request, 'Passwords do not match')
                return redirect('register')  
    else:
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

