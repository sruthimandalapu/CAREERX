from django.contrib.auth.models import User
from django.db import models
from datetime import * #date class

class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)  #custom primary key
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    contact_number = models.BigIntegerField()
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=50)
    r_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.full_name

class Company(models.Model):
    company_id = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.BigIntegerField()
    street_number = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.company_name

class Admin(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.BigIntegerField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.full_name

class Internship(models.Model):
    internship_id = models.CharField(max_length=25, primary_key=True)
    internship_role = models.CharField(max_length=50, default="Software Intern")
    description = models.TextField(default="Description not provided")
    internship_type = models.CharField(
        max_length=20,
        choices=[('part_time', 'Part Time'), ('full_time', 'Full Time')],
        default='full_time',
    )
    location = models.CharField(
        max_length=20,
        choices=[('remote', 'Remote'), ('in_office', 'In Office'), ('hybrid', 'Hybrid')],
        default='remote',
    )
    stipend = models.PositiveIntegerField(default=0)
    start_date = models.DateField(default=date(2024, 1, 1))
    duration_months = models.PositiveIntegerField(default=3)
    last_date_to_apply = models.DateField(default=date(2024, 12, 31))
    posted_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="internships", null=True, blank=True
    )
    created_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_internships"
    )
    def save(self, *args, **kwargs):
        if not self.internship_id:  #auto-generate internship_id if not provided
            self.internship_id = f"INT-{self.company_id}-{int(date.today().strftime('%Y%m%d%H%M%S'))}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.internship_role} at {self.company.company_name if self.company else 'Unknown'}"

class InternshipApplications(models.Model):
    internship_application_id = models.AutoField(primary_key=True)
    internship = models.ForeignKey(
        Internship, on_delete=models.CASCADE, related_name='internship_applications'
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='internship_applications'
    )
    date_of_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending',
    )

    def __str__(self):
        return f"{self.student.full_name} applied for {self.internship.internship_role}"

class Job(models.Model):
    job_id = models.CharField(max_length=25, primary_key=True)
    job_role = models.CharField(max_length=50, default="Job Role Not Specified")
    description = models.TextField(default="Description not provided")
    job_type = models.CharField(
        max_length=20,
        choices=[('part_time', 'Part Time'), ('full_time', 'Full Time')],
        default='full_time',
    )
    location = models.CharField(
        max_length=20,
        choices=[('remote', 'Remote'), ('in_office', 'In Office'), ('hybrid', 'Hybrid')],
        default='remote',
    )
    salary = models.PositiveIntegerField(default=0)
    start_date = models.DateField(default=date(2024, 1, 1))
    last_date_to_apply = models.DateField(default=date(2024, 12, 31))
    posted_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="jobs", null=True, blank=True
    )
    
    created_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_jobs"
    )
    def save(self, *args, **kwargs):
        if not self.job_id:  #auto-generate job_id if not provided
            self.job_id = f"JOB-{self.company_id}-{int(date.today().strftime('%Y%m%d%H%M%S'))}"
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.job_role} at {self.company.company_name if self.company else 'Unknown'}"

class JobApplications(models.Model):
    job_application_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='job_applications'
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='job_applications'
    )
    date_of_applied = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')],
        default='Pending',
    )

    def __str__(self):
        return f"{self.student.full_name} applied for {self.job.job_role}"

class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    announcement_text = models.TextField(default="Announcement text not provided")
    created_by = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, blank=True
    )
    recipient = models.ForeignKey(
        Student, to_field='student_id', on_delete=models.CASCADE, default=1
    )  #reference `student_id`
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notice: {self.announcement_text[:50]}"

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="Untitled Event")  #default added
    description = models.TextField(default="Description not provided")  #default added
    date = models.DateField(default=date(2024, 1, 1))  #default added
    location = models.CharField(max_length=100, default="TBD")

#Login
def login_student():
    students = Student.objects.all()
    lst=[]
    for student in students:
    	lst.append([student.email,student.password])
    return lst

def login_company():
    companies = Company.objects.all()
    lst=[]
    for company in companies:
    	lst.append([company.email,company.password])
    return lst

def login_admin():
    admins = Admin.objects.all()
    lst=[]
    for admin in admins:
    	lst.append([admin.email,admin.password])
    return lst

def student_regsiter_emails():
    students = Student.objects.all()
    lst=[]
    for student in students:
        lst.append(student.email)
    return lst

def company_regsiter_emails():
    companies = Company.objects.all()
    lst=[]
    for company in companies:
        lst.append(company.email)
    return lst

def admin_regsiter_emails():
    admins = Admin.objects.all()
    lst=[]
    for admin in admins:
        lst.append(admin.email)
    return lst

#Register
def register_student(r_number,full_name,email,contact_number,date_of_birth,gender,department,cgpa,password):
    student_count = Student.objects.count()
    new_student=Student(
        student_id=student_count+1,
        full_name=full_name,
        email=email,
        contact_number=contact_number,
        date_of_birth=date_of_birth,
        gender=gender,
        r_number=r_number,
        department=department,
        cgpa=cgpa,
        password=password
        )
    new_student.save()

def register_company(company_name,email,contact_number,street_number,city,state,country,pincode,password):
    company_count = Company.objects.count()
    new_company=Company(
        company_id=company_count+1,
        company_name=company_name,
        email=email,
        contact_number=contact_number,
        street_number=street_number,
        city=city,
        state=state,
        country=country,
        pincode=pincode,
        password=password
        )
    new_company.save()