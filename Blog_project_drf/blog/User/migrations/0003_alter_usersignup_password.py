# Generated by Django 5.0.7 on 2024-08-02 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_usersignup_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersignup',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
