# Generated by Django 3.2.20 on 2023-08-27 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edx_careerpaths', '0007_alter_pathcourse_course'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pathcourse',
            unique_together=set(),
        ),
    ]
