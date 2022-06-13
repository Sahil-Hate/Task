import textwrap
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
            print(patient[0]['id'])
            if(username == patient[0]['username'] and password == patient[0]['password']):
                username = patient[0]['username']
                password = patient[0]['password']
                email = patient[0]['email']
                first_name = patient[0]['first_name']
                last_name = patient[0]['last_name']
                profile_picture = patient[0]['profile_picture']
                address = patient[0]['address']
                pat_id = int(patient[0]['id'])
                return render(request, 'patient.html',{"patient":patient,"pat_id":pat_id,"username":username,"first_name":first_name,
                "email":email,"last_name":last_name,"profile_picture":profile_picture,
                "address":address})
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


def addblog(request,id):
    if request.method == 'POST':
        if 'draft' in request.POST:
            if 'Yes' == request.POST.get('draft'):
                doc = Doctor.objects.get(id=id)
                title = request.POST['title']
                image = request.POST['image']
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
            image = request.POST['image']
            category = request.POST['category']
            summary = request.POST['summary']
            content = request.POST['content']
            blog = Blog.objects.create(title=title,image=image,category=category,
            summary=summary,content=content,doctor=doc,is_draft=True)
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
    return render(request,'readblog.html',{"blogs":blogs,"summary":summary})


