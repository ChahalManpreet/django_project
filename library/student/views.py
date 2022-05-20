from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . models import User, students, branch, semester, section
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse


# Create your views here.
def index(request):
    return render(request, "student/layout.html")

def demo(request):
    return render(request,"student/first.html")

def log_in(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("demo"))
        else:
            return render(request, "student/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
        return render(request, "student/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    print('register')
    branches = branch.objects.all()
    sems = semester.objects.all()
    sectios = section.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # password = request.POST['password']

        reg = request.POST['reg']
        branchs = request.POST['branch']
        seme = request.POST['sem']
        sectin = request.POST['section']

        sel_branch = branch.objects.get(id=branchs)
        sel_setion = section.objects.get(id=sectin)
        sel_sem = semester.objects.get(id=seme)
        print(username, email, reg, branchs, seme, sectin)

        # Ensure password matches confirmation
        password = request.POST["password"]
        # confirmation = request.POST["confirmation"]
        # if password != confirmation:
        #     return render(request, "student/register.html", {
        #         "message": "Passwords must match."
        #     })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            print(user)
            
            a = students(userId = user, Reg_No = reg, branch_id = sel_branch, semester_id = sel_sem, section_id = sel_setion)
            a.save()

        except IntegrityError:
            return render(request, "student/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'student/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "student/register.html",  {'branches': branches, 'sections': sectios, 'sems': sems})

def register_edit(request, id):
    reg_retrieved = students.objects.get(id=id)
    if request.method == "POST":
        
        user_name = request.POST['username']
        user_email = request.POST['email']
        user_password = request.POST['password']
        user_reg = request.POST['reg']
        user_branch = request.POST['branch']
        user_sem = request.POST['sem']
        user_section = request.POST['section']

        reg_retrieved.username = user_name
        reg_retrieved.email = user_email
        reg_retrieved.password = user_password
        reg_retrieved.reg = user_reg
        reg_retrieved.branch =  user_branch
        reg_retrieved.sem = user_sem
        reg_retrieved.section = user_section
        
        reg_retrieved.save()
        
        return HttpResponseRedirect(reverse('register'))
    else:
        return render(request, "student/register.html", {'register': reg_retrieved})


def all_branch(request):
    branches = branch.objects.all()
    return render(request, 'student/branch.html', {'branch': branches})

def add_branch(request):
    if request.method == 'POST':
        name = request.POST['name']

        try:
            b = branch(name = name)
            b.save()
        except:
            return render(request, 'student/add_branch.html', {'message': 'Try Again'})
        return HttpResponseRedirect(reverse('branches'))
    else:
        return render(request, 'student/add_branch.html')

def delete_branch(request, id):
    branc = branch.objects.get(id=id)
    branches = branch.objects.all()
    try:
        branc.delete()
    except:
        return render(request, 'student/all_branch.html', {'branches': branches, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('branches'))

def edit_branch(request, id):
    sel_branch = branch.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_branch.name = name
        try:
            sel_branch.save()
        except:
            return render(request, 'student/edit_branch.html', {'branch': sel_branch, 'message': 'try again'})
        return HttpResponseRedirect(reverse('branches'))

    else:
        return render(request, 'student/edit_branch.html', {'branch': sel_branch})

def add_branch(request):
    if request.method == 'POST':
        name = request.POST['name']

        try:
            b = branch(name = name)
            b.save()
        except:
            return render(request, 'student/add_branch.html', {'message': 'Try Again'})
        return HttpResponseRedirect(reverse('branches'))
    else:
        return render(request, 'student/add_branch.html')
