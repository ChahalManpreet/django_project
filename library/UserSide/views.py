from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from student.models import User, students, branch, semester, section, category, book, issue
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def userLogin(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            if user.is_staff == 0:
                login(request, user)
                return HttpResponseRedirect(reverse("allBooks"))
            else:
                return render(request, "UserSide/userLogin.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "UserSide/userLogin.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "UserSide/userLogin.html")


def userRegister(request):
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

            a = students(userId=user, Reg_No=reg, branch_id=sel_branch, semester_id=sel_sem, section_id=sel_setion)
            a.save()

        except IntegrityError:
            return render(request, "UserSide/userRegister.html", {
                "message": "Username already taken."
            })
        return render(request, "UserSide/userRegister.html", {"message": 'Registered successfully.'})
    else:
        return render(request, "UserSide/userRegister.html", {'branches': branches, 'sections': sectios, 'sems': sems})


@login_required(login_url='userLogin')
def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userLogout'))


@login_required(login_url='userLogin')
def masterPage(request):
    return render(request, "UserSide/masterPage.html")


@login_required(login_url='userLogin')
def allBooks(request):
    if request.method == "POST":
        if request.POST.get("search") is not None:
            srh = request.POST["search"]
            bk = book.objects.filter(BookName__icontains=srh)
            headTitle = "Books"
            return render(request, "UserSide/allBooks.html", {"headTitle": headTitle, 'bk': bk})
        else:
            bk = book.objects.all()
            headTitle = "Books"
            return render(request, "UserSide/allBooks.html", {"headTitle": headTitle, 'bk': bk})
    else:
        bk = book.objects.all()
        headTitle = "Books"
        return render(request, "UserSide/allBooks.html", {"headTitle": headTitle, 'bk': bk})


@login_required(login_url='userLogin')
def booksCategory(request):
    if request.method == "POST":
        if request.POST.get("checks") is not None:
            srh = request.POST.getlist("checks")
            result = map(int, srh)
            results = list(map(int, result))
            print("Category List - ", results)
            bk = book.objects.filter(Category_Id_id__in=results)
            headTitle = "Books"
            ct = category.objects.all()
            return render(request, "UserSide/booksCategory.html", {"headTitle": headTitle, 'bk': bk, 'ct': ct})
        else:
            bk = book.objects.all()
            ct = category.objects.all()
            headTitle = "Books"
            return render(request, "UserSide/booksCategory.html", {"headTitle": headTitle, 'bk': bk, 'ct': ct})
    else:
        bk = book.objects.all()
        ct = category.objects.all()
        headTitle = "Books Category"
        return render(request, "UserSide/booksCategory.html", {"headTitle": headTitle, 'bk': bk, 'ct': ct})


@login_required(login_url='userLogin')
def requestIssueBook(request, pk):
    bookId = book.objects.get(id=pk)
    studentId = request.user
    print("Book Id - ", bookId)
    print("Student Id - ", studentId)
    bi = issue()
    bi.Book_Id = bookId
    bi.Stu_Id = studentId
    bi.save()
    print("Data - ", bi)
    return redirect(requestedBooks)


@login_required(login_url='userLogin')
def requestedBooks(request):
    if request.method == "POST":
        if request.POST.get("search") is not None:
            srh = request.POST["search"]
            issueBook = issue.objects.filter(Status__icontains=srh)
            headTitle = "Requested Books"
            return render(request, "UserSide/requestedBooks.html", {"headTitle": headTitle, "issueBook": issueBook})
        else:
            issueBook = issue.objects.filter(Stu_Id=request.user.id)
            headTitle = "Requested Books"
            return render(request, "UserSide/requestedBooks.html", {"headTitle": headTitle, "issueBook": issueBook})
    else:
        issueBook = issue.objects.filter(Stu_Id=request.user.id)
        headTitle = "Requested Books"
        return render(request, "UserSide/requestedBooks.html", {"headTitle": headTitle, "issueBook": issueBook})
