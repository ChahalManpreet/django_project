from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from student. models import User, students, branch, semester, section, category ,book,issue
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
# Create your views here.


def log_in(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username,password=password)
        # Check if authentication successful
        if user is not None:
            if user.is_superuser:
              login(request, user)
              return HttpResponseRedirect(reverse("branches"))
            else:
                return render(request, "user/login.html", {
            "message": "User is not an Admin."})
        else:
            return render(request, "user/login.html", {
            "message": "Invalid username and/or password."
        })
    else:
        return render(request, "user/login.html")

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
            return render(request, "user/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'user/register.html', {"message": 'Registered Successfully.'})
    else:
        return render(request, "user/register.html",  {'branches': branches, 'sections': sectios, 'sems': sems})


