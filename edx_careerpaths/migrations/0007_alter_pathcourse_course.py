# Generated by Django 3.2.20 on 2023-08-27 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edx_careerpaths', '0006_alter_pathcourse_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathcourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edx_careerpaths.course'),
        ),
    ]
