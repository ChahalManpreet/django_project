from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . models import User, students, branch, semester, section, category ,book
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
        reg_retrieved.branch_id.name =  user_branch
        reg_retrieved.semester_id.name = user_sem
        reg_retrieved.section_id.name = user_section
        
        reg_retrieved.save()
        
        return HttpResponseRedirect(reverse('students'))
    else:
        return render(request, "student/edit_student.html", {'student': reg_retrieved})


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
            return render(request, 'student/edit_branch.html', {'branch': sel_branch, 'message': 'try again'})
        return HttpResponseRedirect(reverse('branches'))

    else:
        return render(request, 'student/edit_branch.html', {'branch': sel_branch})

def all_semester(request):
    semesters = semester.objects.all()
    # print(semesters)
    return render(request, 'student/semester.html', {'semester': semesters})


def add_semester(request):
    if request.method == 'POST':
        name = request.POST['name']

        try:
            b = semester(name = name)
            b.save()
        except:
            return render(request, 'student/add_semester.html', {'message': 'Try Again'})
        return HttpResponseRedirect(reverse('semesters'))
    else:
        return render(request, 'student/add_semester.html')

def edit_semester(request, id):
    sel_semester = semester.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_semester.name = name
        try:
            sel_semester.save()
        except:
            return render(request, 'student/edit_semester.html', {'semester': sel_semester, 'message': 'try again'})
        return HttpResponseRedirect(reverse('semesters'))

    else:
        return render(request, 'student/edit_semester.html', {'semester': sel_semester})

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
    return render(request, 'student/section.html', {'section': sections})

def add_section(request):
    if request.method == 'POST':
        name = request.POST['name']

        try:
            b = section(name = name)
            b.save()
        except:
            return render(request, 'student/add_section.html', {'message': 'Try Again'})
        return HttpResponseRedirect(reverse('sections'))
    else:
        return render(request, 'student/add_section.html')

def edit_section(request, id):
    sel_section = section.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_section.name = name
        try:
            sel_section.save()
        except:
            return render(request, 'student/edit_section.html', {'section': sel_section, 'message': 'try again'})
        return HttpResponseRedirect(reverse('sections'))

    else:
        return render(request, 'student/edit_section.html', {'section': sel_section})

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
            
            a = students(userId = user, Reg_No = reg, branch_id = sel_branch, semester_id = sel_sem, section_id = sel_setion)
            a.save()

        except IntegrityError:
            return render(request, "student/register.html", {
                "message": "Username already taken."
            })
        return render(request, 'student/register.html', {"message": 'Registered successfully.'})
    else:
        return render(request, "student/register.html",  {'branches': branches, 'sections': sectios, 'sems': sems})

def all_books(request):
    books = book.objects.all()
    return render(request, 'student/all_books.html', {'book': books})

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
    #return render(request, 'student/add_book.html')


        try:
            a = book(BookName = bookname,Author =  author,Publication = publication, BookImage = image, No_Copies = copies ,Category_Id = sel_categori, No_Days_Issue = issuedays, Book_Fine = fine)
            a.save()
        except:
           return render(request, 'student/add_book.html', {'message': 'Try Again'})
        return HttpResponseRedirect(reverse('catgorys'))
    else:
        return render(request, 'student/add_book.html',{'category':categry})

def edit_book(request, id):
    book_retrieved = book.objects.get(id=id)
    if request.method == "POST":
        
        book_name = request.POST['name']
        book_author = request.POST['author']
        book_publication = request.POST['publication']
        book_image = request.POST['image']
        book_copies = request.POST['copies']
        book_category = request.POST['category']
        book_issuedays = request.POST['issuedays']
        book_fine = request.POST['fine']

        #book_retrieved.reg = user_reg

        book_retrieved.BookName = book_name
        book_retrieved.Author = book_author
        book_retrieved.Publication = book_publication
        book_retrieved.BookImage = book_image
        book_retrieved.No_Copies =  book_copies
        book_retrieved.Category_Id.name = book_category
        book_retrieved.No_Days_Issue = book_issuedays
        book_retrieved.Book_Fine = book_fine
        
        
        try:
            book_retrieved.save()
        except:
            return render(request, 'student/edit_category.html', {'book': book_retrieved, 'message': 'try again'})
        return HttpResponseRedirect(reverse('books'))
    else:
        return render(request, "student/edit_book.html", {'book':book_retrieved})


def all_category(request):
    categorys = category.objects.all()
    return render(request, 'student/category.html', {'category': categorys})

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']

        try:
            b = category(name = name)
            b.save()
        except:
            return render(request, 'student/add_category.html', {'message': 'Try Again'})
        return HttpResponseRedirect(reverse('catgorys'))
    else:
        return render(request, 'student/add_category.html')

def edit_category(request, id):
    sel_category = category.objects.get(id=id)
    if (request.method) == 'POST':
        name = request.POST['name']

        sel_category.name = name
        try:
            sel_category.save()
        except:
            return render(request, 'student/edit_category.html', {'category': sel_category, 'message': 'try again'})
        return HttpResponseRedirect(reverse('catgorys'))

    else:
        return render(request, 'student/edit_category.html', {'category': sel_category})

def delete_category(request, id):
    categry = category.objects.get(id=id)
    categorys = category.objects.all()
    try:
        categry.delete()
    except:
        return render(request, 'student/category.html', {'categorys': categorys, 'message': 'Please try again'})
    return HttpResponseRedirect(reverse('catgorys'))
