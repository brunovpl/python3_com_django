# Generated by Django 2.0.1 on 2018-01-25 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_announcements_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcements',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='courses.Course', verbose_name='Curso'),
        ),
    ]
