from django.contrib import admin
from .models import User, students, branch, semester, section
# Register your models here.

admin.site.register(students)
admin.site.register(User)
admin.site.register(branch)
admin.site.register(semester)
admin.site.register(section)