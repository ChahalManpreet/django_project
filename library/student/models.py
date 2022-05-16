from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass


class librarian(models.Model):
    Username = models.CharField(max_length= 200)
    Password = models.CharField(max_length= 200)

class category(models.Model):
    Category_Name = models.CharField(max_length = 200)

class branch(models.Model):
    Branch_Name = models.CharField(max_length = 200)

class sem(models.Model):
    Sem = models.CharField(max_length= 200)

class section(models.Model):
    Sec = models.CharField(max_length=200)

class book(models.Model):
    BookName = models.CharField(max_length = 200)
    Author = models.CharField(max_length = 200)
    Publication = models.CharField(max_length = 200)
    subject = models.CharField(max_length = 200)
    BookImage = models.ImageField()
    No_Copies = models.IntegerField()
    Category_Id = models.ForeignKey(category, on_delete = models.CASCADE, related_name = "Category_Id")
    No_Days_Issue = models.IntegerField()
    Book_Fine = models.IntegerField()

class students(models.Model):
    userId = models.OneToOneField(User, on_delete=models.CASCADE)
    # Stu_Name = models.CharField(max_length = 200)
    Reg_No = models.IntegerField()
    Branch = models.ForeignKey(branch, on_delete = models.CASCADE, related_name = "Branch_Id")
    Semester = models.ForeignKey(sem, on_delete = models.CASCADE, related_name = "Sem_Id")
    Section = models.ForeignKey(section, on_delete = models.CASCADE, related_name = "Sec_Id")
    # Email = models.CharField(max_length = 200)
    # Username = models.CharField(max_length = 200)
    # Password = models.CharField(max_length = 200)

    

class issue(models.Model):
    Book_Id = models.ForeignKey(book,on_delete = models.CASCADE, related_name = "Book_Id")
    Stu_Id =models.ForeignKey(students,on_delete = models.CASCADE, related_name = "Stu_Id")
    Issue_Date = models.DateField()
    Return_Date = models.DateField()
    Fine = models.IntegerField()
    Status = models.CharField(max_length = 200)

# class notification(models.Model):
#     Student_Id =models.ForeignKey(students,on_delete = models.CASCADE, related_name = "Student_Id")
#     Created_Date = models.DateField()





    

