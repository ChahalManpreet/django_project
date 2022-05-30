from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, students, branch, semester, section, category, book, issue
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
import os
from datetime import timedelta


# Create your views here.
@login_required(login_url='login')
def adminIndex(request):
    st = section.objects.all().count()
    ct = category.objects.all().count()
    bk = book.objects.all().count()
    headTitle = "World of Reading"
    return render(request, "student/adminIndex.html", {"st": st, "ct": ct, "bk": bk, "headTitle": headTitle})


@login_required(login_url='login')
def adminHome(request):
    return render(request, "student/admin_layout.html")


def log_in(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse("adminIndex"))
            else:
                return render(request, "student/login.html", {
                    "message": "Invalid username and/or password."
                })
        else:
            return render(request, "student/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "student/login.html")


@login_required(login_url='login')
def adminLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


# def register(request):
#     print('register')
#     branches = branch.objects.all()
#     sems = semester.objects.all()
#     sectios = section.objects.all()
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#         # password = request.POST['password']
#
#         reg = request.POST['reg']
#         branchs = request.POST['branch']
#         seme = request.POST['sem']
#         sectin = request.POST['section']
#
#         sel_branch = branch.objects.get(id=branchs)
#         sel_setion = section.objects.get(id=sectin)
#         sel_sem = semester.objects.get(id=seme)
#         print(username, email, reg, branchs, seme, sectin)
#
#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         # confirmation = request.POST["confirmation"]
#         # if password != confirmation:
#         #     return render(request, "student/register.html", {
#         #         "message": "Passwords must match."
#         #     })
#
#         # Attempt to create new user
#         try:
#             user = User.objects.create_user(username, email, password)
#             user.save()
#             print(user)
#
#             a = students(userId=user, Reg_No=reg, branch_id=sel_branch, semester_id=sel_sem, section_id=sel_setion)
#             a.save()
#
#         except IntegrityError:
#             return render(request, "student/register.html", {
#                 "message": "Username already taken."
#             })
#         return render(request, 'student/register.html', {"message": 'Registered successfully.'})
#     else:
#         return render(request, "student/register.html", {'branches': branches, 'sections': sectios, 'sems': sems})


@login_required(login_url='login')
def edit_student(request, id):
    reg_retrieved = students.objects.get(id=id)
    if request.method == "POST":

        user_name = request.POST['username']
        user_email = request.POST['email']
        # user_password = request.POST['password']
        user_reg = request.POST['reg']
        user_branch = request.POST['branch']
        user_sem = request.POST['sem']
        user_section = request.POST['section']

        reg_retrieved.userId.username = user_name
        reg_retrieved.userId.email = user_email
        # reg_retrieved.password = user_password
        reg_retrieved.reg = user_reg
        reg_retrieved.branch_id.name = user_branch
        reg_retrieved.semester_id.name = user_sem
        reg_retrieved.section_id.name = user_section

        reg_retrieved.save()

        return HttpResponseRedirect(reverse('students'))
    else:
        return render(request, "student/edit_student.html", {'student': reg_retrieved})


@login_required(login_url='login')
def all_branch(request):
    branches = branch.objects.all()
    headTitle = "Branches"
    return render(request, 'student/branch.html', {'branch': branches, 'headTitle': headTitle})


@login_required(login_url='login')
def add_branch(request):
    if request.method == 'POST':
        n = request.POST['name']
        print("New Branch Name - ", n)
        a = branch.objects.filter(name=n).first()
        print("Branch Data - ", a)
        if a:
            return render(request, 'student/add_branch.html', {'message': 'Branch already exists'})
        else:
            name = request.POST['name']

            try:
                b = branch(name=name)
                b.save()
            except:
                return render(request, 'student/add_branch.html', {'message': 'Try Again'})
            return HttpResponseRedirect(reverse('branches'))
    else:
        headTitle = "Add Branch"
        return render(request, 'student/add_branch.html', {'headTitle': headTitle})


@login_required(login_url='login')
def delete_branch(request, id):
    branc = branch.objects.get(id=id)
    branches = branch.objects.all()
    try:
        branc.delete()
    except:
        return render(request, 'student/branch.html', {'branches': branches, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('branches'))


@login_required(login_url='login')
def edit_branch(request, id):
    sel_branch = branch.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_branch.name = name
        try:
            sel_branch.save()
        except:
            headTitle = "Update Branch"
            return render(request, 'student/edit_branch.html',
                          {'branch': sel_branch, 'message': 'try again', 'headTitle': headTitle})
        return HttpResponseRedirect(reverse('branches'))

    else:
        headTitle = "Update Branch"
        return render(request, 'student/edit_branch.html', {'branch': sel_branch, 'headTitle': headTitle})


@login_required(login_url='login')
def all_semester(request):
    semesters = semester.objects.all()
    headTitle = "Semesters"
    return render(request, 'student/semester.html', {'semester': semesters, 'headTitle': headTitle})


@login_required(login_url='login')
def add_semester(request):
    if request.method == 'POST':
        n = request.POST['name']
        a = semester.objects.filter(name=n).first()
        if a:
            headTitle = "Add Semester"
            return render(request, 'student/add_semester.html', {'message': 'Semester already exists', 'headTitle': headTitle})
        else:
            name = request.POST['name']
            try:
                b = semester(name=name)
                b.save()
            except:
                headTitle = "Add Semester"
                return render(request, 'student/add_semester.html', {'message': 'Try Again', 'headTitle': headTitle})
            return HttpResponseRedirect(reverse('semesters'))
    else:
        headTitle = "Add Semester"
        return render(request, 'student/add_semester.html', {"headTitle": headTitle})


@login_required(login_url='login')
def edit_semester(request, id):
    sel_semester = semester.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_semester.name = name
        try:
            sel_semester.save()
        except:
            headTitle = "Update Semester"
            return render(request, 'student/edit_semester.html',
                          {'semester': sel_semester, 'message': 'try again', 'headTitle': headTitle})
        return HttpResponseRedirect(reverse('semesters'))

    else:
        headTitle = "Update Semester"
        return render(request, 'student/edit_semester.html', {'semester': sel_semester, 'headTitle': headTitle})


@login_required(login_url='login')
def delete_semester(request, id):
    semestr = semester.objects.get(id=id)
    semesters = semester.objects.all()
    try:
        semestr.delete()
    except:
        return render(request, 'student/all_branch.html', {'semesters': semesters, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('semesters'))


@login_required(login_url='login')
def all_section(request):
    sections = section.objects.all()
    headTitle = "Sections"
    return render(request, 'student/section.html', {'section': sections, 'headTitle': headTitle})


@login_required(login_url='login')
def add_section(request):
    if request.method == 'POST':
        n = request.POST['name']
        a = section.objects.filter(name=n).first()
        if a:
            headTitle = "Add Section"
            return render(request, 'student/add_section.html', {'message': 'Section Already Exists', 'headTitle': headTitle})
        else:
            name = request.POST['name']

            try:
                b = section(name=name)
                b.save()
            except:
                headTitle = "Add Section"
                return render(request, 'student/add_section.html', {'message': 'Try Again', 'headTitle': headTitle})
            return HttpResponseRedirect(reverse('sections'))
    else:
        headTitle = "Add Section"
        return render(request, 'student/add_section.html', {'headTitle': headTitle})


@login_required(login_url='login')
def edit_section(request, id):
    sel_section = section.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_section.name = name
        try:
            sel_section.save()
        except:
            headTitle = "Update Section"
            return render(request, 'student/edit_section.html',
                          {'section': sel_section, 'message': 'try again', 'headTitle': headTitle})
        return HttpResponseRedirect(reverse('sections'))

    else:
        headTitle = "Update Section"
        return render(request, 'student/edit_section.html', {'section': sel_section, 'headTitle': headTitle})


@login_required(login_url='login')
def delete_section(request, id):
    secton = section.objects.get(id=id)
    sections = section.objects.all()
    try:
        secton.delete()
    except:
        return render(request, 'student/all_section.html', {'sections': sections, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('sections'))


@login_required(login_url='login')
def all_students(request):
    student = students.objects.all()
    return render(request, 'student/all_student.html', {'students': student})


@login_required(login_url='login')
def add_student(request):
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
            return render(request, "student/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'student/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "student/register.html", {'branches': branches, 'sections': sectios, 'sems': sems})


@login_required(login_url='login')
def all_books(request):
    books = book.objects.all()
    headTitle = "Books"
    return render(request, 'student/all_books.html', {'book': books, 'headTitle': headTitle})


@login_required(login_url='login')
def add_book(request):
    categry = category.objects.all()
    if request.method == 'POST':
        n = request.POST['name']
        a = book.objects.filter(BookName=n).first()
        if a:
            headTitle = "Add BooK"
            return render(request, 'student/add_book.html', {'message': 'Book Already Exits', 'headTitle': headTitle})
        else:
            bookname = request.POST['name']
            author = request.POST['author']
            publication = request.POST['publication']
            image = request.FILES['image']
            copies = request.POST['copies']
            categori = request.POST['category']
            issuedays = request.POST['issuedays']
            fine = request.POST['fine']

            sel_categori = category.objects.get(id=categori)

            # print(bookname, author,publication,image,copies,category,issuedays,fine)
            # return render(request, 'student/add_book.html')

            try:
                a = book(BookName=bookname, Author=author, Publication=publication, BookImage=image, No_Copies=copies,
                         Category_Id=sel_categori, No_Days_Issue=issuedays, Book_Fine=fine)
                a.save()
            except:
                headTitle = "Add BooK"
                return render(request, 'student/add_book.html', {'message': 'Try Again', 'headTitle': headTitle})
            return HttpResponseRedirect(reverse('books'))
    else:
        headTitle = "Add BooK"
        return render(request, 'student/add_book.html', {'category': categry, 'headTitle': headTitle})


@login_required(login_url='login')
def edit_book(request, id):
    book_retrieved = book.objects.get(id=id)
    categry = category.objects.all()
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(book_retrieved.BookImage) > 0:
                os.remove(book_retrieved.BookImage.path)
            book_retrieved.BookImage = request.FILES['image']
        book_name = request.POST['name']
        book_author = request.POST['author']
        book_publication = request.POST['publication']
        book_copies = request.POST['copies']
        book_category = category.objects.get(id=request.POST['category'])
        book_issuedays = request.POST['issuedays']
        book_fine = request.POST['fine']

        # book_retrieved.reg = user_reg

        book_retrieved.BookName = book_name
        book_retrieved.Author = book_author
        book_retrieved.Publication = book_publication
        book_retrieved.No_Copies = book_copies
        book_retrieved.Category_Id = book_category
        book_retrieved.No_Days_Issue = book_issuedays
        book_retrieved.Book_Fine = book_fine

        try:
            book_retrieved.save()
        except:
            headTitle = "Update BooK"
            return render(request, 'student/edit_category.html',
                          {'book': book_retrieved, 'message': 'try again', 'headTitle': headTitle, 'category': categry})
        return HttpResponseRedirect(reverse('books'))
    else:
        headTitle = "Update BooK"
        return render(request, "student/edit_book.html",
                      {'book': book_retrieved, 'headTitle': headTitle, 'category': categry})


@login_required(login_url='login')
def all_category(request):
    categorys = category.objects.all()
    headTitle = "Categories"
    return render(request, 'student/category.html', {'category': categorys, 'headTitle': headTitle})


@login_required(login_url='login')
def add_category(request):
    if request.method == 'POST':
        n = request.POST['name']
        a = category.objects.filter(name=n).first()
        if a:
            headTitle = "Add Category"
            return render(request, 'student/add_category.html', {'message': 'Category Already Exists', 'headTitle': headTitle})
        else:
            name = request.POST['name']

            try:
                b = category(name=name)
                b.save()
            except:
                headTitle = "Add Category"
                return render(request, 'student/add_category.html', {'message': 'Try Again', 'headTitle': headTitle})
            return HttpResponseRedirect(reverse('catgorys'))
    else:
        headTitle = "Add Category"
        return render(request, 'student/add_category.html', {'headTitle': headTitle})


@login_required(login_url='login')
def edit_category(request, id):
    sel_category = category.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_category.name = name
        try:
            sel_category.save()
        except:
            headTitle = "Update Category"
            return render(request, 'student/edit_category.html',
                          {'category': sel_category, 'message': 'try again', 'headTitle': headTitle})
        return HttpResponseRedirect(reverse('catgorys'))

    else:
        headTitle = "Update Category"
        return render(request, 'student/edit_category.html', {'category': sel_category, 'headTitle': headTitle})


@login_required(login_url='login')
def delete_category(request, id):
    categry = category.objects.get(id=id)
    categorys = category.objects.all()
    try:
        categry.delete()
    except:
        return render(request, 'student/category.html', {'categorys': categorys, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('catgorys'))


@login_required(login_url='login')
def requestIssues(request):
    issueBook = issue.objects.all()
    for i in issueBook:
        print("Student Id - ", i.Stu_Id.id)
        st = students.objects.filter(userId_id=i.Stu_Id.id)
        headTitle = "Requested Books"
        return render(request, "student/requestedBooks.html",
                      {"headTitle": headTitle, "issueBook": issueBook, "st": st})


@login_required(login_url='login')
def changestatus(request):
    b = issue.objects.get(id=request.GET['id'])

    if request.GET['Status'] == "APPROVED":
        numberOfDays = request.GET['nDays']
        nD = int(numberOfDays)
        print("Number of days - ", nD, " Type - ", type(nD))

        # Get the current Date for issue book Date
        currentDate = datetime.date.today().strftime("%Y-%m-%d")
        formattedDate = datetime.datetime.strptime(currentDate, "%Y-%m-%d")
        print("Current Date - ", currentDate, " Type - ", type(currentDate))

        # Add days into the current date according to the book return days
        newDate = formattedDate + datetime.timedelta(days=nD)
        d = newDate.strftime("%Y-%m-%d")
        print("New Date - ", d, "Type - ", type(d))

        # Firstly change the return date from string to datetime format for comparison againts issue date
        returnDate = datetime.datetime.strptime(d,"%Y-%m-%d")
        if formattedDate > returnDate:
            d1 = returnDate
            d2 = formattedDate
            delta = d2 - d1
            print("Dates Difference - ", delta.days, 'Type of Days - ', type(delta.days))
            bookFine = request.GET['bFine']
            totalBookFine = int(bookFine) * int(delta.days)
            print("Total Book Fine - ", totalBookFine)

            b.Status = request.GET['Status']
            b.Issue_Date = formattedDate
            b.Return_Date = d
            b.Fine = totalBookFine
            b.save()
            return redirect(requestIssues)
        else:
            b.Status = request.GET['Status']
            b.Issue_Date = formattedDate
            b.Return_Date = d
            b.Fine = 0
            b.save()
            return redirect(requestIssues)
    else:
        b.Status = request.GET['Status']
        b.Issue_Date = None
        b.Return_Date = None
        b.Fine = 0
        b.save()
        return redirect(requestIssues)
