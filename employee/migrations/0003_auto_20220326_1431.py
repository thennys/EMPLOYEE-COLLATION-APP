# Generated by Django 3.1.4 on 2022-03-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_uploadlogs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeerecords',
            name='supervisors',
            field=models.ManyToManyField(blank=True, null=True, to='employee.Supervisors'),
        ),
    ]
