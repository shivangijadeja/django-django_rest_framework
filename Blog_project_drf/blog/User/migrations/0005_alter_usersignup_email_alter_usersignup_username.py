# Generated by Django 5.0.7 on 2024-08-06 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_alter_usersignup_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersignup',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='usersignup',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
