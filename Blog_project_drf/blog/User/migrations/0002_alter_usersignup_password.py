# Generated by Django 5.0.7 on 2024-08-02 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersignup',
            name='password',
            field=models.IntegerField(max_length=100),
        ),
    ]
