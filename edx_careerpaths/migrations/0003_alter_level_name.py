# Generated by Django 3.2.20 on 2023-08-26 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edx_careerpaths', '0002_level_pathcourses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
