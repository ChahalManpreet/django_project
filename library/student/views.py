from django.shortcuts import render
from django.http import HttpResponse
from . models import User, students, branch, sem, section
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError


# Create your views here.
def index(request):
    return render(request, "student/layout.html")

def log_in(request):
    #if request.method == "POST":
        # Attempt to sign user in
       # username = request.POST["username"]
        #password = request.POST["password"]
        # user = (request, username=username,
        # password=/password)
    return render(request, "student/login.html")

def register(request):
    branches = branch.objects.all()
    sems = sem.objects.all()
    sectios = section.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        reg = request.POST['reg']
        branch = request.POST['branch']
        seme = request.POST['sem']
        sectin = request.POST['section']

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "student/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            a = students(userId = user, Reg_No = reg, Branch = branch, Semester = seme, Section = sectin)
            a.save()

        except IntegrityError:
            return render(request, "student/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'student/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "student/register.html", {'sems': sems, 'sections': sectios, 'branch': branches})

