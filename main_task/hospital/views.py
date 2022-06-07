from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        doc = Doctor.objects.filter(username=username).values()
        patient = Patient.objects.filter(username=username).values()
        print(doc)
        print(patient)
        if(doc.exists()):
            if(username == doc[0]['username'] and password == doc[0]['password']):
                username = doc[0]['username']
                password = doc[0]['password']
                email = doc[0]['email']
                first_name = doc[0]['first_name']
                last_name = doc[0]['last_name']
                profile_picture = doc[0]['profile_picture']
                address = doc[0]['address']
                return render(request, 'index.html',{"username":username,"password":password,
                "email":email,"first_name":first_name,"last_name":last_name,"profile_picture":profile_picture,
                "address":address})

        if(patient.exists()):
            if(username == patient[0]['username'] and password == patient[0]['password']):
                username = patient[0]['username']
                password = patient[0]['password']
                email = patient[0]['email']
                first_name = patient[0]['first_name']
                last_name = patient[0]['last_name']
                profile_picture = patient[0]['profile_picture']
                address = patient[0]['address']
                return render(request, 'index.html',{"username":username,"first_name":first_name,
                "email":email,"last_name":last_name,"profile_picture":profile_picture,
                "address":address})

        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    
    else:
        return render(request,'login.html')


def dr_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname'].strip()
        last_name = request.POST['lastname'].strip()
        profile_picture = request.POST['ProfilePicture'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()
        address = request.POST['address'].strip()

        if password == confirm_password:
            if Doctor.objects.filter(username=username).exists():
                messages.info(request,'Username already taken!')
                return redirect('dr_signup')
            elif Doctor.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('dr_signup')
            else:
                doctor = Doctor.objects.create(first_name=first_name,
                last_name=last_name,profile_picture=profile_picture,
                username=username,email=email,password=password,
                address=address)
                doctor.save()
                messages.info(request,'Doctor User Created!')
                return render(request,'index.html')
        else:
            messages.info(request,'Passwords do not match')
            return render(request,'dr_signup.html')

    else:  
        return render(request,'dr_signup.html')


def patient_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname'].strip()
        last_name = request.POST['lastname'].strip()
        profile_picture = request.POST['ProfilePicture'].strip()
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        confirm_password = request.POST['confirm_password'].strip()
        address = request.POST['address'].strip()

        if password == confirm_password:
            if Patient.objects.filter(username=username).exists():
                messages.info(request,'Username already taken!')
                return redirect('patient_signup')
            elif Patient.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('patient_signup')
            else:
                patient = Patient.objects.create(first_name=first_name,
                last_name=last_name,profile_picture=profile_picture,
                username=username,email=email,password=password,
                address=address)
                patient.save()
                messages.info(request,'Patient User Created!')
                return render(request,'index.html')
        else:
            messages.info(request,'Passwords do not match')
            return render(request,'patient_signup.html')

    else:  
        return render(request,'patient_signup.html')