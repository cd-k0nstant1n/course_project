from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import auth, User
from .models import CustomUser

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
                if User.objects.filter(email = email).exists():
                    messages.info(request, 'This email already exists')
                    return redirect('register')
                elif CustomUser.objects.filter(phone = phone).exists():
                    messages.info(request, 'Phone already used')
                    return redirect('register')
                else:
                    pass1 = make_password(pass1)
                    user = User.objects.create_user(username=email, email=email, password=pass1, first_name=fname, last_name=lname)
                    CustomUser.objects.create(user=user, phone=phone, role=role)
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
            # code = request.POST['code']
    
            if pass1 == pass2:
                if User.objects.filter(email = email).exists():
                    messages.info(request, 'This email already exists')
                    return redirect('register')
                elif CustomUser.objects.filter(phone = phone).exists():
                    messages.info(request, 'Phone already used')
                    return redirect('register')
                else:
                    pass1 = make_password(pass1)
                    user = User.objects.create_user(username=email, email=email, password=pass1, first_name=fname, last_name=lname)
                    CustomUser.objects.create(user=user, phone=phone, role=role, specialty=specialty)
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
        user = auth.authenticate(request, email=email, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')