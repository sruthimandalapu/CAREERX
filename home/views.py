from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Case, When, Value, BooleanField, Exists, OuterRef

from django.views.decorators.csrf import csrf_exempt
from .models import *
TEMPLATE_DIRS=(
    'os.path.join(BASE_DIR,"templates")'
)

def index(request):
    return render(request, "index.html")

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        radio_option = request.POST.get('radio_options')
        user_authenticated = False
        
        if radio_option == "student":
            student = Student.objects.filter(email=email).first()
            if student and student.password == password:
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.set_password(password)
                    user.save()
                login(request, user)
                request.session['user_type'] = 'student'
                request.session['user_email'] = email
                user_authenticated = True

        elif radio_option == "company":
            company = Company.objects.filter(email=email).first()
            if company and company.password == password:
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.set_password(password)
                    user.save()
                login(request, user)
                request.session['user_type'] = 'company'
                request.session['user_email'] = email
                user_authenticated = True

        elif radio_option == "admin":
            admin = Admin.objects.filter(email=email).first()
            if admin and admin.password == password:
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.set_password(password)
                    user.save()
                login(request, user)
                request.session['user_type'] = 'admin'
                request.session['user_email'] = email
                user_authenticated = True
        #redirect based on user type
        if user_authenticated:
            if request.session['user_type'] == 'student':
                return redirect('student_dashboard')
            elif request.session['user_type'] == 'company':
                return redirect('company_dashboard')
            elif request.session['user_type'] == 'admin':
                return redirect('admin_dashboard')
        else:
            return HttpResponse("Invalid credentials!")

    return render(request, "login.html")

def password_reset(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        #confirm_password = request.POST.get('confirm_password')
        radio_option = request.POST.get('radio_options')
        if radio_option=="option1":
            lst=student_regsiter_emails()
            if email in lst:
                update_student_password(email,password)
            else:
                return HttpResponse("Email is not registered")
        elif radio_option=="option2":
            lst=company_regsiter_emails()
            if email in lst:
                update_company_password(email,password)
            else:
                return HttpResponse("Email is not registered")
        else:
            lst=admin_regsiter_emails()
            if email in lst:
                update_admin_password(email,password)
            else:
                return HttpResponse("Email is not registered")
    return render(request, 'password_reset.html')

def home(request):
    jobs = Job.objects.all()
    internships = Internship.objects.all()
    return render(request, 'jobboard.html', {'jobs': jobs, 'internships': internships})

def logout_view(request):
    #logs out the user and clears the session
    logout(request)
    request.session.flush()  #completely clears the session
    return redirect('index')  #redirect to the index page

# ADMIN
@login_required
def admin_dashboard(request):
    admin = get_object_or_404(Admin, email=request.session.get('user_email'))
    return render(request, 'admin_dashboard.html',{'admin':admin})


#fetch a particular admin by ID
def fetch_admin_details(admin_id):
    admin=Admin.objects.get(admin_id=admin_id)
    lst = [
        admin.full_name,
        admin.email,
        admin.contact_number,
        admin.age,
        admin.gender,
    ]
    return lst

#update deatils of a particular admin by ID
def update_admin_details(admin_id,full_name,email,contact_number,age,gender):
    admin=Admin.objects.get(admin_id=admin_id)
    admin.full_name=full_name
    admin.email=email
    admin.contact_number=contact_number
    admin.age=age
    admin.gender=gender
    admin.save()

# STUDENT
def student_register(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        date_of_birth = request.POST.get('dob')
        print(date_of_birth)
        gender = request.POST.get('gender')
        r_number = request.POST.get('r_number')
        department = request.POST.get('department')
        cgpa = request.POST.get('cgpa')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if email in student_regsiter_emails():
            return HttpResponse("Mail-id already registered")
        else:
            register_student(r_number,full_name,email,contact_number,date_of_birth,gender,department,cgpa,password)
            return render(request,"login.html")
    return render(request, 'student_register.html')

#creates a new student record in the DB
def create_student_record(full_name,email,contact_number,date_of_birth,gender,r_number,department,cgpa,password):
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

def update_student_password(email,password):
    student=Student.objects.get(email=email)
    student.password=password
    student.save()

def update_admin_password(email,password):
    admin=Admin.objects.get(email=email)
    admin.password=password
    admin.save()
    
#updates details of a particular student by ID
def update_student_record(student_id,full_name,email,contact_number,date_of_birth,gender,r_number,department,cgpa):
    student=Student.objects.get(student_id=student_id)
    student.full_name=full_name
    student.email=email
    student.contact_number=contact_number
    student.date_of_birth=date_of_birth
    student.gender=gender
    student.r_number=r_number
    student.department=department
    student.cgpa=cgpa
    #student.password=password
    student.save()
    
def view_particular_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    context = {
        'student': student
    }
    return render(request, 'view_particular_student.html', context)

#fetch details of all studnets as a list of lists
def fetch_all_students():
    students = Student.objects.all()
    result = [
        [
            student.student_id,
            student.full_name,
            student.email,
            student.contact_number,
            student.date_of_birth,
            student.gender,
            student.r_number,
            student.department,
            student.cgpa,
        ]
        for student in students
    ]
    return result
    
def delete_student(student_id):
    student=Student.objects.get(student_id=student_id)
    student.delete()
@login_required
def student_dashboard(request):
    student = get_object_or_404(Student, email=request.session.get('user_email'))
    return render(request, 'student_dashboard.html', {'student': student})

@login_required
def view_student_profile(request):
    if request.session.get('user_type') == 'student':
        student = get_object_or_404(Student, email=request.session.get('user_email'))
        return render(request, 'view_student_profile.html', {'student': student})
    return HttpResponse("Unauthorized access", status=401)

@login_required
def profile_update(request):
    student = get_object_or_404(Student, email=request.session.get('user_email'))
    
    if request.method == "POST":
        #update student profile with the submitted form data
        student.full_name = request.POST.get("full_name", student.full_name)
        student.contact_number = request.POST.get("contact_number", student.contact_number)
        student.date_of_birth = request.POST.get("date_of_birth", student.date_of_birth)
        student.gender = request.POST.get("gender", student.gender)
        student.r_number = request.POST.get("r_number", student.r_number)
        student.department = request.POST.get("department", student.department)
        student.cgpa = request.POST.get("cgpa", student.cgpa)
        
        student.save()  #saving changes to the database
        return redirect('student_dashboard')  #redirect to the student's dashboard after saving
    return render(request, 'view_student_profile.html', {'student': student})

# COMPANY
def company_register(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        street_number = request.POST.get('street_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pincode = request.POST.get('pincode')
        password = request.POST.get('password')
        if email in company_regsiter_emails():
            return HttpResponse("Mail-id already registered")
        else:
            register_company(company_name,email,contact_number,street_number,city,state,country,pincode,password)
            return render(request,"login.html")
    return render(request, 'company_register.html')

#creates a new company record in DB
def create_company_record(company_name,email,contact_number,street_number,city,state,country,pincode):
    company_count = Company.objects.count()
    new_company = Company(
        company_id=company_count + 1,
        company_name=company_name,
        email=email,
        contact_number=contact_number,
        street_number=street_number,
        city=city,
        state=state,
        country=country,
        pincode=pincode,
    )
    new_company.save()
    
def update_company_password(email,password):
    company=Company.objects.get(email=email)
    company.password=password
    company.save()
    
#update details of a particular company by ID
def update_company_record(company_id,company_name,email,contact_number,street_number,city,state,country,pincode):
    company = Company.objects.get(company_id=company_id)
    company.company_name = company_name
    company.email = email
    company.contact_number = contact_number
    company.street_number = street_number
    company.city = city
    company.state = state
    company.country = country
    company.pincode = pincode
    company.save()
    
def delete_company(company_id):
    company=Company.objects.get(company_id=company_id)
    company.delete()
    
def view_particular_company(company_id):
    company=Company.objects.get(company_id=company_id)
    lst=[]
    lst.append(company.company_name)
    lst.append(company.email)
    lst.append(company.contact_number)
    lst.append(company.street_number)
    lst.append(company.city)
    lst.append(company.state)
    lst.append(company.country)
    lst.append(company.pincode)
    return lst

#fetches all company details as a list of lists
def fetch_all_companies():
    companies = Company.objects.all()
    e=[]
    for company in companies:
        lst=[]
        lst.append(company.company_id)
        lst.append(company.company_name)
        lst.append(company.email)
        lst.append(company.contact_number)
        lst.append(company.street_number)
        lst.append(company.city)
        lst.append(company.state)
        lst.append(company.country)
        lst.append(company.pincode)
        e.append(lst)
    return e
@login_required
def company_dashboard(request):
    company =  Company.objects.filter(email=request.session.get('user_email')).first()
    return render(request, 'company_dashboard.html',{'company' : company})

@login_required
def company_profile(request):
    if request.session.get('user_type') != 'company':
        return redirect('login')

    company = Company.objects.filter(email=request.session.get('user_email')).first()
    if request.method == "POST":
        company.company_name = request.POST.get("company_name")
        company.contact_number = request.POST.get("contact_number")
        company.street_number = request.POST.get("street_number")
        company.city = request.POST.get("city")
        company.state = request.POST.get("state")
        company.country = request.POST.get("country")
        company.pincode = request.POST.get("pincode")
        company.save()
        messages.success(request, "Profile updated successfully!")
    return render(request, "company_profile.html", {"company": company})

def view_companies(request):
    companies = Company.objects.all()
    user_type = request.session.get('user_type')  #ftch the user type from the session
    return render(request, 'view_companies.html', {'companies': companies, 'user_type': user_type})

def view_students(request):
    students = Student.objects.all()
    user_type = request.session.get('user_type')  #ftch the user type from the session
    return render(request, 'view_students.html', {'students': students, 'user_type': user_type})
#INTERNSHIP
@login_required
def add_internship(request):
    if request.method == "POST":
        internship_role = request.POST.get("internship_role")
        description = request.POST.get("description")
        internship_type = request.POST.get("internship_type")
        location = request.POST.get("location")
        stipend = request.POST.get("stipend")
        start_date = request.POST.get("start_date")
        duration_months = request.POST.get("duration_months")
        last_date_to_apply = request.POST.get("last_date_to_apply")
        
        company = None
        admin = None
        #check the type of logged-in user
        if request.session.get('user_type') == 'company':
            company = Company.objects.filter(email=request.session.get('user_email')).first()
        elif request.session.get('user_type') == 'admin':
            admin = Admin.objects.filter(email=request.session.get('user_email')).first()
            company_id = request.POST.get("company_id")  #ensure company_id is submitted in the form
            company = Company.objects.filter(company_id=company_id).first()

        #create the internship with the relevant company or admin
        internship = Internship.objects.create(
            internship_role=internship_role,
            description=description,
            internship_type=internship_type,
            location=location,
            stipend=stipend,
            start_date=start_date,
            duration_months=duration_months,
            last_date_to_apply=last_date_to_apply,
            company=company,
            created_by=admin
        )
        messages.success(request, "Internship added successfully.")
        return redirect("view_internships")
    return render(request, "add_internship.html")



#creates a new internship record in DB
def create_internship_record(internship_id,role,description,duration,type,location,stiphend,company,created_by,posted_date):
    internship_count = Internship.objects.count()
    new_internship=Internship(
        internship_id=internship_count+1,
        role=role,
        description=description,
        duration=duration,
        type=type,
        location=location,
        stiphend=stiphend,
        company=company,
        created_by=created_by,
        posted_date=posted_date
        )
    new_internship.save()

#updates internship details in the database by ID
# CRUD for backend internship record
# def update_internship_record(internship_id,role,description,duration,type,location,stiphend,company,created_by,posted_date):
#     internship=Internship.objects.get(internship_id=internship_id)
#     internship.role=role
#     internship.description=description
#     internship.duration=duration
#     internship.type=type
#     internship.location=location
#     internship.stiphend=stiphend
#     internship.company=company
#     internship.created_by=created_by
#     internship.posted_date=posted_date
#     internship.save()
    
@login_required
def update_internship(request, internship_id):
    internship = get_object_or_404(Internship, internship_id=internship_id)
    if request.method == "POST":
        internship.internship_role = request.POST.get("internship_role")
        internship.description = request.POST.get("description")
        internship.internship_type = request.POST.get("internship_type")
        internship.location = request.POST.get("location")
        internship.stipend = request.POST.get("stipend")
        internship.start_date = request.POST.get("start_date")
        internship.duration_months = request.POST.get("duration_months")
        internship.last_date_to_apply = request.POST.get("last_date_to_apply")
        internship.save()
        messages.success(request, "Internship updated successfully.")
        return redirect('view_internships')
    return render(request, 'update_internship.html', {'internship': internship})

def view_internships(request):
    student = None
    company_user = None
    user_email = request.session.get('user_email')
    if request.session.get('user_type') == 'student':
        student = Student.objects.filter(email=user_email).first()
    elif request.session.get('user_type') == 'company':
        company_user = Company.objects.filter(email=user_email).first()

    today = date.today()
    internships = Internship.objects.annotate(
        student_applied=Exists(
            InternshipApplications.objects.filter(internship=OuterRef('pk'), student=student)
        ),
        is_owner=Case(
            When(company=company_user, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        is_expired=Case(
            When(last_date_to_apply__lt=today, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    ).prefetch_related('internship_applications')
    return render(request, 'view_internships.html', {
        'internships': internships,
        'can_manage_internships': request.session.get('user_type') == 'company',
        'is_student': request.session.get('user_type') == 'student',
        'user_type': request.session.get('user_type'),
        'user_email': user_email
    })

@login_required
def delete_internship(request, internship_id):
    internship = get_object_or_404(Internship, internship_id=internship_id)
    if request.method == "POST":
        internship.delete()
        messages.success(request, "Internship deleted successfully.")
        return redirect('view_internships')
    return HttpResponse("Invalid request", status=400)

def view_particular_internship(internship_id):
    internship=Internship.objects.get(internship_id=internship_id)
    lst=[]
    lst.append(internship.role)
    lst.append(internship.description)
    lst.append(internship.duration)
    lst.append(internship.type)
    lst.append(internship.location)
    lst.append(internship.stiphend)
    lst.append(internship.company)
    lst.append(internship.created_by)
    lst.append(internship.posted_date)
    return lst

#fetches all internship details as a list of lists
def fetch_all_internships():
    internships = Internship.objects.all()
    e=[]
    for internship in internships:
        lst=[]
        lst.append(internship.intership_id)
        lst.append(internship.role)
        lst.append(internship.description)
        lst.append(internship.duration)
        lst.append(internship.type)
        lst.append(internship.location)
        lst.append(internship.stiphend)
        lst.append(internship.company)
        lst.append(internship.created_by)
        lst.append(internship.posted_date)
        e.append(lst)
    return e

@login_required
def apply_internship(request, internship_id):
    if request.method == "POST" and request.session.get('user_type') == 'student':
        student = get_object_or_404(Student, email=request.session.get('user_email'))
        internship = get_object_or_404(Internship, internship_id=internship_id)
        #check if the student has already applied
        if InternshipApplications.objects.filter(student=student, internship=internship).exists():
            return JsonResponse({"message": "You have already applied for this internship!"}, status=400)
        #create the application
        InternshipApplications.objects.create(student=student, internship=internship)
        return JsonResponse({"message": "Successfully applied to the internship!"}, status=200)
    return JsonResponse({"message": "Unauthorized access"}, status=403)

# JOB
@login_required
def add_job(request):
    if request.method == "POST":
        job_role = request.POST.get("job_role")
        description = request.POST.get("description")
        job_type = request.POST.get("job_type")
        location = request.POST.get("location")
        salary = request.POST.get("salary")
        start_date = request.POST.get("start_date")
        last_date_to_apply = request.POST.get("last_date_to_apply")
        
        company = None
        admin = None
        #check the type of logged-in user
        if request.session.get('user_type') == 'company':
            company = Company.objects.filter(email=request.session.get('user_email')).first()
        elif request.session.get('user_type') == 'admin':
            admin = Admin.objects.filter(email=request.session.get('user_email')).first()
            company_id = request.POST.get("company_id")
            company = Company.objects.filter(company_id=company_id).first()
        #create the job with the relevant company or admin
        job = Job(
            job_role=job_role,
            description=description,
            job_type=job_type,
            location=location,
            salary=salary,
            start_date=start_date,
            last_date_to_apply=last_date_to_apply,
            company=company,
            created_by=admin
        )
        job.save()
        messages.success(request, "Job added successfully.")
        return redirect("view_jobs")
    return render(request, "add_job.html")

#creates a new job record in DB
def create_job_record(job_id,name,description,company,created_by,posted_date):
    job_count = Job.objects.count()
    new_job=Job(
        job_id=job_count+1,
        name=name,
        description=description,
        company=company,
        created_by=created_by,
        posted_date=posted_date
        )
    new_job.save()
    
#updates job details in the database by ID
def update_job_record(job_id,name,description,company,created_by,posted_date):
    job=Job.objects.get(job_id=job_id)
    job.name=name
    job.description=description
    job.company=company
    job.created_by=created_by
    job.posted_date=posted_date
    job.save()
    
@login_required
def update_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == "POST":
        job.job_role = request.POST.get("job_role")
        job.description = request.POST.get("description")
        job.location = request.POST.get("location")
        job.salary = request.POST.get("salary")
        job.start_date = request.POST.get("start_date")
        job.last_date_to_apply = request.POST.get("last_date_to_apply")
        job.save()
        return redirect('view_jobs')
    return render(request, 'update_job.html', {'job': job})
    
def delete_job(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('view_jobs')
    return HttpResponse("Invalid request", status=400)
    
def view_particular_job(job_id):
    job=Job.objects.get(job_id=job_id)
    lst=[]
    lst.append(job.name)
    lst.append(job.description)
    lst.append(job.company)
    lst.append(job.created_by)
    lst.append(job.posted_date)
    return lst

#fetches all job details as a list of lists
def fetch_all_jobs():
    jobs = Job.objects.all()
    e=[]
    for job in jobs:
        lst=[]
        lst.append(job.name)
        lst.append(job.description)
        lst.append(job.company)
        lst.append(job.created_by)
        lst.append(job.posted_date)
        e.append(lst)
    return e

@login_required
def view_jobs(request):
    student = None
    company_user = None
    user_email = request.session.get('user_email')
    #identify whether the user is a student or a company
    if request.session.get('user_type') == 'student':
        student = Student.objects.filter(email=user_email).first()
    elif request.session.get('user_type') == 'company':
        company_user = Company.objects.filter(email=user_email).first()
    
    today = date.today()
    jobs = Job.objects.prefetch_related('job_applications__student').annotate(
        student_applied=Exists(
            JobApplications.objects.filter(job=OuterRef('pk'), student=student)
        ),
        is_owner=Case(
            When(company=company_user, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        ),
        is_expired=Case(
            When(last_date_to_apply__lt=today, then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    )
    return render(request, 'view_jobs.html', {
        'jobs': jobs,
        'can_manage_jobs': request.session.get('user_type') == 'company',
        'is_student': request.session.get('user_type') == 'student',
        'user_type': request.session.get('user_type'),
        'user_email': user_email  # Pass the user's email to the template
    })

@login_required
def apply_job(request, job_id):
    if request.method == "POST" and request.session.get('user_type') == 'student':
        #get the student associated with the logged-in session
        student = get_object_or_404(Student, email=request.session.get('user_email'))
        #get the job using the provided `job_id`
        job = get_object_or_404(Job, job_id=job_id)
        #check if the student has already applied for the job
        if JobApplications.objects.filter(student=student, job=job).exists():
            return JsonResponse({"message": "You have already applied for this job!"}, status=400)
        #create the job application
        JobApplications.objects.create(student=student, job=job)
        return JsonResponse({"message": "Successfully applied to the job!"}, status=200)
    #return unauthorized access for invalid requests
    return JsonResponse({"message": "Unauthorized access"}, status=403)

# EVENT
@login_required
def add_event(request):
    if request.method == "POST":
        #rtrieve form data
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        location = request.POST.get("location")
        #save the new event
        Event.objects.create(
            title=title,
            description=description,
            date=date,
            location=location
        )
        return redirect("view_events")  #redirect to the events listing page
    return render(request, "add_event.html")

#creates a new event record in DB
def create_event_record(event_id,title,description,date,location):
    event_count = Event.objects.count()
    new_event=Event(
        event_id=event_count+1,
        title=title,
        description=description,
        date=date,
        location=location
        )
    new_event.save()
    
#updates event details in the database by ID
def update_event_record(event_id,title,description,date,location):
    event=Event.objects.get(event_id=event_id)
    event.title=title
    event.description=description
    event.date=date
    event.location=location
    event.save()
    
@login_required
def update_event(request, event_id):
    #event by ID
    event = get_object_or_404(Event, event_id=event_id)
    if request.method == "POST":
        #update the event with POST data
        event.title = request.POST.get("event_name")
        event.description = request.POST.get("description")
        event.date = request.POST.get("date")
        event.location = request.POST.get("location")
        event.save()
        #redirect to the events list page after updating
        return redirect("view_events")
    #render the update form with pre-filled event data
    return render(request, "update_event.html", {"event": event})
    
def view_events(request):
    events = Event.objects.all()
    user_type = request.session.get('user_type', None)
    can_manage_events = user_type in ['admin']
    return render(request, 'view_events.html', {'events': events, 'can_manage_events': can_manage_events})

#fetches all event details as a list of lists
def fetch_all_events():
    events = Event.objects.all()
    e=[]
    for event in events:
        lst=[]
        lst.append(event.event_id)
        lst.append(event.title)
        lst.append(event.description)
        lst.append(event.date)
        lst.append(event.location)
        e.append(lst)
    return e

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.session.get('user_type') not in ['admin']:
        return HttpResponse("Unauthorized", status=401)

    if request.method == "POST":
        event.delete()
        return redirect('view_events')
    return redirect('view_events')

@login_required
def dashboard(request):
    user_type = request.session.get('user_type')
    if user_type == 'student':
        return redirect('student_dashboard')
    elif user_type == 'company':
        return redirect('company_dashboard')
    elif user_type == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('home')

# NOTICE
@login_required
def add_notice(request):
    admins = Admin.objects.all()
    students = Student.objects.all()

    if request.method == "POST":
        announcement_text = request.POST.get("announcement_text")
        #recipient_id = request.POST.get("recipient_id")
        try:
            created_by = Admin.objects.get(email=request.session.get('user_email'))
            #recipient = Student.objects.get(pk=recipient_id)

            notice = Notice(
                announcement_text=announcement_text,
                created_by=created_by,
                #recipient=recipient
            )
            notice.save()

            messages.success(request, "Notice added successfully.")
            return redirect('view_notices')
        except Student.DoesNotExist:
            messages.error(request, "Invalid student ID.")
        except Admin.DoesNotExist:
            messages.error(request, "Invalid admin or not logged in as admin.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    #pass admins and students to the template
    return render(request, 'add_notice.html', {'admins': admins, 'students': students})

@login_required
def view_notices(request):
    notices = Notice.objects.all()
    user_type = request.session.get('user_type', None)
    can_manage_notices = user_type == 'admin'
    return render(request, 'view_notices.html', {'notices': notices, 'can_manage_notices': can_manage_notices})

#fetches all notice details as a list of lists
def fetch_all_notices():
    notices = Notice.objects.all()
    e=[]
    for notice in notices:
        lst=[]
        lst.append(notice.announcement_text)
        lst.append(notice.created_by)
        lst.append(notice.recipient)
        lst.append(notice.created_by)
        e.append(lst)
    return e

#updates notice details in the database by ID
def update_notice_record(notice_id,announcement_text,created_by,recipient,date_created):
    notice=Notice.objects.get(notice_id=notice_id)
    notice.announcement_text=announcement_text
    notice.created_by=created_by
    notice.recipient=recipient
    notice.date_created=date_created
    notice.save()

@login_required
def update_notice(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == "POST":
        notice.announcement_text = request.POST.get("announcement_text")
        notice.save()
        messages.success(request, "Notice updated successfully!")
        return redirect("view_notices")
    return render(request, "update_notice.html", {"notice": notice})
    
@login_required
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, notice_id=notice_id)
    if request.method == "POST":
        notice.delete()
        messages.success(request, "Notice deleted successfully.")
        return redirect('view_notices')
    return HttpResponse("Invalid request", status=400)
 
def view_particular_notice(notice_id):
    notice=Notice.objects.get(notice_id=notice_id)
    lst=[]
    lst.append(notice.announcement_text)
    lst.append(notice.created_by)
    lst.append(notice.recipient)
    lst.append(notice.created_by)
    return lst

#APPLICANTS
@login_required
def view_applicants(request):
    user_email = request.session.get('user_email')
    company = Company.objects.filter(email=user_email).first()
    if not company:
        return render(request, 'error.html', {
            'message': "You are not associated with any company. Please contact support."
        })
    jobs = Job.objects.filter(company=company)
    internships = Internship.objects.filter(company=company)
    job_applicants = JobApplications.objects.filter(job__in=jobs)
    internship_applicants = InternshipApplications.objects.filter(internship__in=internships)
    if request.method == "POST":
        #processing status update
        application_id = request.POST.get("application_id")
        application_type = request.POST.get("application_type")
        new_status = request.POST.get("status")
        #application type and process
        if application_type == "job":
            application = get_object_or_404(JobApplications, pk=application_id, job__company=company)
        elif application_type == "internship":
            application = get_object_or_404(InternshipApplications, pk=application_id, internship__company=company)
        else:
            return HttpResponseBadRequest("Invalid application type.")
        #updating the status
        application.status = new_status
        application.save()
        return redirect("view_applicants")
    return render(request, 'view_applicants.html', {
        'job_applicants': job_applicants,
        'internship_applicants': internship_applicants,
    })
