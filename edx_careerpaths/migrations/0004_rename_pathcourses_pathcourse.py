# Generated by Django 3.2.20 on 2023-08-26 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edx_careerpaths', '0003_alter_level_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PathCourses',
            new_name='PathCourse',
        ),
    ]
