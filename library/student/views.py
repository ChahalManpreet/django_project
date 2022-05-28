from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, students, branch, semester, section, category, book
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse


# Create your views here.
def adminIndex(request):
    st = section.objects.all().count()
    ct = category.objects.all().count()
    bk = book.objects.all().count()
    headTitle = "World of Reading"
    return render(request, "student/adminIndex.html", {"st": st, "ct": ct, "bk": bk, "headTitle": headTitle})


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
            login(request, user)
            return HttpResponseRedirect(reverse("adminIndex"))
        else:
            return render(request, "student/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "student/login.html")


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


def all_branch(request):
    branches = branch.objects.all()
    headTitle = "Branches"
    return render(request, 'student/branch.html', {'branch': branches, 'headTitle': headTitle})


def add_branch(request):
    if request.method == 'POST':
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


def delete_branch(request, id):
    branc = branch.objects.get(id=id)
    branches = branch.objects.all()
    try:
        branc.delete()
    except:
        return render(request, 'student/branch.html', {'branches': branches, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('branches'))


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


def all_semester(request):
    semesters = semester.objects.all()
    headTitle = "Semesters"
    return render(request, 'student/semester.html', {'semester': semesters, 'headTitle': headTitle})


def add_semester(request):
    if request.method == 'POST':
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


def delete_semester(request, id):
    semestr = semester.objects.get(id=id)
    semesters = semester.objects.all()
    try:
        semestr.delete()
    except:
        return render(request, 'student/all_branch.html', {'semesters': semesters, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('semesters'))


def all_section(request):
    sections = section.objects.all()
    headTitle = "Sections"
    return render(request, 'student/section.html', {'section': sections, 'headTitle': headTitle})


def add_section(request):
    if request.method == 'POST':
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


def delete_section(request, id):
    secton = section.objects.get(id=id)
    sections = section.objects.all()
    try:
        secton.delete()
    except:
        return render(request, 'student/all_section.html', {'sections': sections, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('sections'))


def all_students(request):
    student = students.objects.all()
    return render(request, 'student/all_student.html', {'students': student})


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


def all_books(request):
    books = book.objects.all()
    headTitle = "Books"
    return render(request, 'student/all_books.html', {'book': books, 'headTitle': headTitle})


def add_book(request):
    categry = category.objects.all()
    if request.method == 'POST':
        bookname = request.POST['name']
        author = request.POST['author']
        publication = request.POST['publication']
        image = request.POST['image']
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
            return render(request, 'student/add_book.html', {'message': 'Try Again','headTitle':headTitle})
        return HttpResponseRedirect(reverse('books'))
    else:
        headTitle = "Add BooK"
        return render(request, 'student/add_book.html', {'category': categry,'headTitle':headTitle})


def edit_book(request, id):
    book_retrieved = book.objects.get(id=id)
    categry = category.objects.all()
    if request.method == "POST":

        book_name = request.POST['name']
        book_author = request.POST['author']
        book_publication = request.POST['publication']
        book_image = request.POST['image']
        book_copies = request.POST['copies']
        book_category = request.POST['category']
        book_issuedays = request.POST['issuedays']
        book_fine = request.POST['fine']

        # book_retrieved.reg = user_reg

        book_retrieved.BookName = book_name
        book_retrieved.Author = book_author
        book_retrieved.Publication = book_publication
        book_retrieved.BookImage = book_image
        book_retrieved.No_Copies = book_copies
        book_retrieved.Category_Id.name = book_category
        book_retrieved.No_Days_Issue = book_issuedays
        book_retrieved.Book_Fine = book_fine

        try:
            book_retrieved.save()
        except:
            headTitle = "Update BooK"
            return render(request, 'student/edit_category.html', {'book': book_retrieved, 'message': 'try again','headTitle':headTitle,'category': categry})
        return HttpResponseRedirect(reverse('books'))
    else:
        headTitle = "Update BooK"
        return render(request, "student/edit_book.html", {'book': book_retrieved,'headTitle':headTitle,'category': categry})


def all_category(request):
    categorys = category.objects.all()
    headTitle = "Categories"
    return render(request, 'student/category.html', {'category': categorys, 'headTitle': headTitle})


def add_category(request):
    if request.method == 'POST':
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


def delete_category(request, id):
    categry = category.objects.get(id=id)
    categorys = category.objects.all()
    try:
        categry.delete()
    except:
        return render(request, 'student/category.html', {'categorys': categorys, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('catgorys'))
