# Generated by Django 4.0.4 on 2022-05-29 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_issue_fine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='Stu_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stu_Id', to=settings.AUTH_USER_MODEL),
        ),
    ]
