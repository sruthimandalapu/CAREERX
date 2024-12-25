# Generated by Django 5.1.2 on 2024-11-14 23:03

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_number', models.BigIntegerField()),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.IntegerField(primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contact_number', models.BigIntegerField()),
                ('street_number', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='Untitled Event', max_length=100)),
                ('description', models.TextField(default='Description not provided')),
                ('date', models.DateField(default=datetime.date(2024, 1, 1))),
                ('location', models.CharField(default='TBD', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.IntegerField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('contact_number', models.BigIntegerField()),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(max_length=50)),
                ('r_number', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=100)),
                ('cgpa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('internship_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('internship_role', models.CharField(default='Software Intern', max_length=50)),
                ('description', models.TextField(default='Description not provided')),
                ('internship_type', models.CharField(choices=[('part_time', 'Part Time'), ('full_time', 'Full Time')], default='full_time', max_length=20)),
                ('location', models.CharField(choices=[('remote', 'Remote'), ('in_office', 'In Office'), ('hybrid', 'Hybrid')], default='remote', max_length=20)),
                ('stipend', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField(default=datetime.date(2024, 1, 1))),
                ('duration_months', models.PositiveIntegerField(default=3)),
                ('last_date_to_apply', models.DateField(default=datetime.date(2024, 12, 31))),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='internships', to='home.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_internships', to='home.admin')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('job_role', models.CharField(default='Job Role Not Specified', max_length=50)),
                ('description', models.TextField(default='Description not provided')),
                ('job_type', models.CharField(choices=[('part_time', 'Part Time'), ('full_time', 'Full Time')], default='full_time', max_length=20)),
                ('location', models.CharField(choices=[('remote', 'Remote'), ('in_office', 'In Office'), ('hybrid', 'Hybrid')], default='remote', max_length=20)),
                ('salary', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField(default=datetime.date(2024, 1, 1))),
                ('last_date_to_apply', models.DateField(default=datetime.date(2024, 12, 31))),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='home.company')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_jobs', to='home.admin')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('announcement_text', models.TextField(default='Announcement text not provided')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.admin')),
                ('recipient', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.student')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplications',
            fields=[
                ('job_application_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_applied', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=50)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='home.job')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_applications', to='home.student')),
            ],
        ),
        migrations.CreateModel(
            name='InternshipApplications',
            fields=[
                ('internship_application_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_applied', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=50)),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internship_applications', to='home.internship')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internship_applications', to='home.student')),
            ],
        ),
    ]
