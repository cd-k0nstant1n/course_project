from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Patient, Doctor
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, auth

# Create your views here.
def index(request):
    return render(request, 'index.html')

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
        
            if pass1 == pass2:
                if Patient.objects.filter(email = email).exists():
                    messages.info(request, 'This email already exists')
                    return redirect('register')
                elif Patient.objects.filter(phone = phone).exists():
                    messages.info(request, 'Phone already used')
                    return redirect('register')
                else:
                    pass1 = make_password(pass1)
                    patient = Patient.objects.create(fname=fname, lname=lname, phone=phone, email=email, password=pass1)
                    patient.save();
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
            # code = request.POST['code']
    
            if pass1 == pass2:
                if Doctor.objects.filter(email = email).exists():
                    messages.info(request, 'This email already exists')
                    return redirect('register')
                elif Doctor.objects.filter(phone = phone).exists():
                    messages.info(request, 'Phone already used')
                    return redirect('register')
                else:
                    pass1 = make_password(pass1)
                    doctor = Doctor.objects.create(fname=fname, lname=lname, phone=phone, email=email, specialty=specialty, password=pass1)
                    doctor.save();
                    return redirect('/')         
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
        user = auth.authenticate(request, email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')