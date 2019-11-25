from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *
from recruit import views
from recruit.views import (base_of_applicants, CreateJobInterview,
                           EditJobInterview, DelJobInterview,
                           recruit_chat, get_messages, send_message,
                           chat_update, check_mes, recruit_main_page,
                           favorites, check_favor,
                           recruit_base, RecruitProfile,
                           RecruitEditMain, RecruitEditExperience,
                           RecruitEditSkills, RecruitEditPhoto,
                           RecruitEditEducation, RecruitShowSkills,
                           RecruitShowEducation, RecruitShowExperience)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """

urlpatterns = [
    # TeamPoland ##################################################

    path('', views.recruit_main_page, name='recruiter_url'),
    # There is of recruiter's main page
    path('base/', views.recruiter_base, name='base_url'),
    path('base/base_of_clients/', views.base_of_applicants,
         name='base_of_clients'),
    path('base/base_of_clients/<id_a>/', views.ApplicantDet.as_view(),
         name='applicant_url'),
    path('base/base_of_clients/<id_a>/tasks/',
         views.CreateJobInterview.as_view(), name='applicant_tasks_url'),
    path('base/base_of_clients/<id_a>/edit_job_interview/',
         views.EditJobInterview.as_view(),
         name='applicant_edit_interviews_url'),
    path('base/base_of_clients/<id_a>/del_job_interview/',
         views.DelJobInterview.as_view(), name='applicant_del_interviews_url'),

    path('base/vacancies/', views.Vacancies.as_view(), name='vacancies_url'),
    path('base/vacancies/<id_v>/', views.VacancyDet.as_view(), name='vacancy_recr_url'),
    path('base/vacancies/<id_v>/del_vacancy/', views.DelVacancy.as_view(), name='vacancy_del_recr_url'),
    path('reports/', reports, name='reports_url'),
    path('reports/employed_clients/', EmployedClients.as_view(), name='employed_clients_url'),
    path('base/vacancies/<id_v>/', views.VacancyDet.as_view(),
         name='vacancy_recr_url'),
    path('base/vacancies/<id_v>/del_vacancy/', views.DelVacancy.as_view(),
         name='vacancy_del_recr_url'),

    # End TeamPoland ###############################################

    path('chat/', login_required(recruit_chat), name='contact_with_clients'),
    path('get_messages/', get_messages, name='get_messages'),
    path('send_message/', send_message, name='send_message'),
    path('chat_update/', chat_update, name='chat_update'),
    path('check_mes/', check_mes, name='check_mes'),
    path('base/base_of_clients/<id_a>/client_add_task/', views.client_task_adding.as_view(), name='client_task_adding_url'),
    path(r'favorites/', views.favorites, name='favorites'),
    path(r'checkfavor/', views.check_favor, name='check_favor'),
    path(r'client_filtration/', views.client_filtration, name='client_filtration'),
    path('change_task/<id_t>', views.change_task.as_view(), name='change_task_url'),
    path('pattern_task/', views.pattern_task.as_view(), name='pattern_task_url'),
    path('pattern_use/', views.use_as_pattern, name='use_as_pattern_url'),


    # Team Rome (start)
    path('profile/', RecruitProfile.as_view(), name='recruit_profile'),
    path('edit/', RecruitEditMain.as_view(), name='recruit_edit'),
    path('edit/experience/', RecruitEditExperience.as_view(),
         name='recruit_edit_experience'),
    path('edit/skills/', RecruitEditSkills.as_view(),
         name='recruit_edit_skills'),
    path('edit/photo/', RecruitEditPhoto.as_view(), name='recruit_edit_photo'),
    path('edit/education/', RecruitEditEducation.as_view(),
         name='recruit_edit_education'),
    path('show_skills', RecruitShowSkills.as_view(),
         name='recruit_show_skills'),
    path('show_education', RecruitShowEducation.as_view(),
         name='recruit_show_education'),
    path('show_experience', RecruitShowExperience.as_view(),
         name='recruit_show_experience'),
    # Team Rome (end)
]
