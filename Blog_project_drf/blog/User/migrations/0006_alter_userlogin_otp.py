# Generated by Django 5.0.7 on 2024-08-06 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0005_alter_usersignup_email_alter_usersignup_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogin',
            name='otp',
            field=models.CharField(max_length=6),
        ),
    ]
