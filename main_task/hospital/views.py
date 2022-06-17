from datetime import datetime
from datetime import timedelta
import textwrap
from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path

# Create your views here.


def index(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def dr_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        doc = Doctor.objects.filter(username=username).values()
        if(doc.exists()):
            if(username == doc[0]['username'] and password == doc[0]['password']):
                username = doc[0]['username']
                password = doc[0]['password']
                email = doc[0]['email']
                first_name = doc[0]['first_name']
                last_name = doc[0]['last_name']
                profile_picture = doc[0]['profile_picture']
                address = doc[0]['address']
                doc_id = str(doc[0]['id'])
                return redirect("doctor_main/" + doc_id )
            else:
                messages.info(request,'Invalid credentials')
                return render(request,'dr_login.html')

        else:
            messages.info(request,'Invalid credentials')
            return render(request,'dr_login.html')
    
    else:
        return render(request,'dr_login.html')


def patient_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        patient = Patient.objects.filter(username=username).values()
        if(patient.exists()):
            if(username == patient[0]['username'] and password == patient[0]['password']):
                username = patient[0]['username']
                password = patient[0]['password']
                email = patient[0]['email']
                first_name = patient[0]['first_name']
                last_name = patient[0]['last_name']
                profile_picture = patient[0]['profile_picture']
                address = patient[0]['address']
                pat_id = str(patient[0]['id'])
                return redirect("patient_main/" + pat_id )
            else:
                messages.info(request,'Invalid credentials')
                return render(request,'patient_login.html')
        else:
            messages.info(request,'Invalid credentials')
            return render(request,'patient_login.html')

    else:
        return render(request,'patient_login.html')


def dr_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname'].strip()
        last_name = request.POST['lastname'].strip()
        profile_picture = request.POST.get('ProfilePicture')
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
                return render(request,'dr.html')
        else:
            messages.info(request,'Passwords do not match')
            return render(request,'dr_signup.html')

    else:  
        return render(request,'dr_signup.html')


def patient_signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname'].strip()
        last_name = request.POST['lastname'].strip()
        profile_picture = request.POST.get('ProfilePicture')
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
                return render(request,'patient.html')
        else:
            messages.info(request,'Passwords do not match')
            return render(request,'patient_signup.html')

    else:  
        return render(request,'patient_signup.html')


def doctor(request):
    return render(request, 'dr.html')


def patient(request):
    return render(request, 'patient.html')

def doctor_main(request, id):
    if request.method == 'POST':
        doc = Doctor.objects.get(id=id)
        if(doc.exists()):
            username = doc[0]['username']
            password = doc[0]['password']
            email = doc[0]['email']
            first_name = doc[0]['first_name']
            last_name = doc[0]['last_name']
            profile_picture = doc[0]['profile_picture']
            address = doc[0]['address']
            doc_id = int(doc[0]['id'])
            return render(request, 'dr_main.html',{"doc":doc,"doc_id":doc_id,"username":username,"password":password,
            "email":email,"first_name":first_name,"last_name":last_name,"profile_picture":profile_picture,
            "address":address})
        else:
            return render(request, 'dr_login.html')
    else:
        doc = Doctor.objects.get(id=id) 
        return render(request, 'dr_main.html',{"doc":doc})

def patient_main(request,id):
    if request.method == 'POST':
        patient = Patient.objects.get(id=id)
        if(patient.exists()):
            username = patient[0]['username']
            password = patient[0]['password']
            email = patient[0]['email']
            first_name = patient[0]['first_name']
            last_name = patient[0]['last_name']
            profile_picture = patient[0]['profile_picture']
            address = patient[0]['address']
            patient_id = int(patient[0]['id'])
            return render(request, 'patient_main.html',{"patient":patient,"patient_id":patient_id,"username":username,"password":password,
            "email":email,"first_name":first_name,"last_name":last_name,"profile_picture":profile_picture,
            "address":address})
        else:
            return render(request, 'patient_login.html')
    else:
        patient = Patient.objects.get(id=id)
        return render(request, 'patient_main.html',{"patient":patient})


def addblog(request,id):
    if request.method == 'POST':
        if 'draft' in request.POST:
            doc = Doctor.objects.get(id=id)
            title = request.POST['title']
            image = request.POST.get('image')
            category = request.POST['category']
            summary = request.POST['summary']
            content = request.POST['content']
            blog = Blog.objects.create(title=title,image=image,category=category,
            summary=summary,content=content,doctor=doc,is_draft=True)
            blog.save()
            messages.info(request,'Draft saved')
            return render(request,'addblog.html',{"doc":doc})
        else:
            doc = Doctor.objects.get(id=id)
            title = request.POST['title']
            image = request.POST.get('image')
            category = request.POST['category']
            summary = request.POST['summary']
            content = request.POST['content']
            blog = Blog.objects.create(title=title,image=image,category=category,
            summary=summary,content=content,doctor=doc,is_draft=False)
            blog.save()
            messages.info(request,'Blog Uploaded Successfully!')
            return render(request,'addblog.html',{"doc":doc})

    else:
        doc = Doctor.objects.get(id=id)
        return render(request,'addblog.html',{"doc":doc})

def draftblog(request,id):
    doc = Doctor.objects.get(id=id)
    blogs = Blog.objects.filter(doctor=doc)
    draft_blog = blogs.filter(is_draft=True)
    print(draft_blog)
    for i in draft_blog:
        print(i.title)
        print(i.id)
    return render(request,'draftblog.html',{"draft_blog":draft_blog,"doc":doc})

def readblog(request):
    blogs = Blog.objects.all()
    print(blogs)
    for i in blogs:
        s = i.summary
        words = s.split()
        summary1 = " ".join(words[:15])
        summary = summary1 + "..."
        i.summary = summary
    return render(request,'readblog.html',{"blogs":blogs})

def doctorlist(request,user):
    doctors = Doctor.objects.all()
    patient = Patient.objects.get(username=user)
    print(doctors)
    return render(request,'drlist.html',{"doctors":doctors,"patient":patient})


SCOPES = ["https://www.googleapis.com/auth/calendar"]
service_account_email = "task-service-account@calender-api-353319.iam.gserviceaccount.com"
credentials = service_account.Credentials.from_service_account_file('client_secret-final.json', scopes=SCOPES)
scoped_credentials = credentials.with_scopes(SCOPES)

def build_service():
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


def bookdoctor(request,user,id):
    doctor = Doctor.objects.get(id=id)
    patient = Patient.objects.get(username=user)

    calendarId = "c_classroom7b5889f1@group.calendar.google.com"
    if request.method == 'POST':
        speciality = request.POST['speciality']
        appointment_date = request.POST['appointment_date']
        appointment_time = request.POST['appointment_time']
        n=45
        date_format_str = '%H:%M'
        given_time = datetime.strptime(appointment_time, date_format_str)
        final_time = given_time + timedelta(minutes=n)
        final_time = final_time.strftime("%H:%M")
        
        # service = build_service()
        # event = (
        #     service.events().insert(
        #         calendarId=calendarId,
        #         body={
        #             "summary": "Appointment for DR. doctor.username",
        #             "start": {"dateTime": appointment_time.isoformat()},
        #             "end": {"dateTime": final_time.isoformat()},
        #         },
        #     ).execute()
        # )
        # print(event)
        
        appointment = Appointment.objects.create(doctor=doctor,patient=patient,
        speciality=speciality,appointment_date=appointment_date,appointment_time=appointment_time)
        appointment.save()
        messages.info(request,'Appointment Successfull')
        return render(request,'confirmation.html',{"doctor":doctor,"patient":patient,"speciality":speciality,
        "appointment_date":appointment_date,"appointment_time":appointment_time, "final_time":final_time})
    else:
        return render(request,'bookdoctor.html',{"doctor":doctor,"patient":patient})

def confirmation(request,user,id):
    doctor = Doctor.objects.get(id=id)
    patient = Patient.objects.get(username=user)
    return render(request,'confirmation.html',{"doctor":doctor,"patient":patient})

