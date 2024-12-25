# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'), 
    path('home/', views.home, name='home'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('logout/', views.logout_view, name='logout'),
    
    # ADMIN
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    #student profile
    path('student_register/', views.student_register, name='student_register'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('view_student_profile/', views.view_student_profile, name='view_student_profile'),
    # path('view_students/', views.view_students, name='view_students'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('view_students/', views.view_students, name='view_students'),
    
    path('student/<int:student_id>/', views.view_particular_student, name='view_particular_student'),
    
    #internship related paths
    path('view_internships/', views.view_internships, name='view_internships'),
    path('apply-internship/<str:internship_id>/', views.apply_internship, name='apply_internship'),
    path('add_internship/', views.add_internship, name='add_internship'),
    path('update_internship/<str:internship_id>/', views.update_internship, name='update_internship'),
    path('delete_internship/<str:internship_id>/', views.delete_internship, name='delete_internship'),
    
    #job related paths
    path('company_register/', views.company_register, name='company_register'),
    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),
    path('view_jobs/', views.view_jobs, name='view_jobs'),
    path('apply-job/<str:job_id>/', views.apply_job, name='apply_job'),
    path('add_job/', views.add_job, name='add_job'),
    path('update_job/<str:job_id>/', views.update_job, name='update_job'),
    path('delete_job/<str:job_id>/', views.delete_job, name='delete_job'),
    
    #notice related paths
    path('view-notices/', views.view_notices, name='view_notices'),
    path('add_notice/', views.add_notice, name='add_notice'),
    path('update_notice/<int:notice_id>/', views.update_notice, name='update_notice'),
    path('delete_notice/<int:notice_id>/', views.delete_notice, name='delete_notice'),
    
   #company related path
    path('view_companies/', views.view_companies, name='view_companies'),
    path('company_profile/', views.company_profile, name='company_profile'),
    
    #event related paths
    path('view_events/', views.view_events, name='view_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update_event/<int:event_id>/', views.update_event, name='update_event'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    
    #to the top?
    path('dashboard/', views.dashboard, name='dashboard'),
    
    #applicants
    path('view_applicants/', views.view_applicants, name='view_applicants'),
]