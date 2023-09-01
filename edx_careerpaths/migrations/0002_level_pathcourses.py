# Generated by Django 3.2.20 on 2023-08-26 04:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edx_careerpaths', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='PathCourses',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.CharField(max_length=250)),
                ('careerpath', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edx_careerpaths.careerpath')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edx_careerpaths.level')),
            ],
        ),
    ]
