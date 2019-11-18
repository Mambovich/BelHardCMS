from django.contrib.auth.decorators import login_required
from django.urls import path

from client.edit.load_data_list import (SkillsDataList, InstitutionDataList, CvPositionDataList)
from client.views import (ClientProfile, client_main_page, ClientEditMain, ClientEditSkills, ClientEditPhoto,
                          ClientEditCv, ClientEditEducation, ClientEditExperience, ClientShowSkills,
                          ClientShowEducation, ClientShowExperience, ClientShowCv, MessagesView, opinion_list,
                          OpinionCreate, opinion_detail, answer_create, OpinionDelete, client_login, client_logout,
                          tasks, checktask, checknotifications, settings_menu, set_settings, ResumesList, ResumeDetail,
                          AcceptedVacancies, RejectedVacancies, VacancyDetail, accept_reject, help_list, viewed,
                          admin_jobinterviews, interviews_list, checkinterviews, upload, chat_update)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """

urlpatterns = [
    path('', client_main_page, name='client'),  # main client page

    # Team Rome (start) - Edit Forms URLs
    path('profile', ClientProfile.as_view(), name='client_profile'),
    path('edit/', ClientEditMain.as_view(), name='client_edit'),
    path('edit/skills/', ClientEditSkills.as_view(), name='client_edit_skills'),
    path('edit/photo/', ClientEditPhoto.as_view(), name='client_edit_photo'),
    path('edit/cv/', ClientEditCv.as_view(), name='client_edit_cv'),
    path('edit/education/', ClientEditEducation.as_view(), name='client_edit_education'),
    path('edit/experience/', ClientEditExperience.as_view(), name='client_edit_experience'),
    path('edit/skills_data_list/', SkillsDataList.as_view(), name='skills_data_list'),
    path('edit/institution_data_list/', InstitutionDataList.as_view(), name='institution_data_list'),
    path('edit/cv_position_data_list/', CvPositionDataList.as_view(), name='cv_position_data_list'),
    path('show_skills', ClientShowSkills.as_view(), name='client_show_skills'),
    path('show_education', ClientShowEducation.as_view(), name='client_show_education'),
    path('show_experience', ClientShowExperience.as_view(), name='client_show_experience'),
    path('show_cv', ClientShowCv.as_view(), name='client_show_cv'),
    # Team Rome (end)

    path('chat/', login_required(MessagesView.as_view()), name='contact_with_centre'),
    path('chat_update/', chat_update, name='chat_update'),
    path(r'opinion/', opinion_list, name='opinion_list'),
    path(r'opinion/create/', OpinionCreate.as_view(), name='opinion_create'),
    path(r'opinion/<int:pk>/', opinion_detail, name='opinion_detail'),
    path(r'opinion/edit/<int:pk>/', answer_create, name='opinion_answer'),
    path(r'opinion/edit/<int:pk>/delete/', OpinionDelete.as_view(), name='opinion_delete'),
    path('login/', client_login, name='login'),
    path('logout/', client_logout, name='logout'),
    path('tasks/', tasks, name='tasks_list'),

    path(r'checktask/', checktask),
    path(r'checknotifications/', checknotifications),
    path(r'settings/', settings_menu, name='settings_menu'),
    path(r'settingsset/', set_settings, name='settings_set'),

    # Poland urls (start)
    path('cvs/', ResumesList.as_view(), name='resumes_list_url'),
    path('cv_detail/<id_c>/', ResumeDetail.as_view(), name='resume_detail_url'),
    path('cv/<id_c>/accepted_vacancies/', AcceptedVacancies.as_view(), name='accepted_vacancies_url'),
    path('cv/<id_c>/rejected_vacancies/', RejectedVacancies.as_view(), name='rejected_vacancies_url'),
    path('cv/vacancy/<id_v>/', VacancyDetail.as_view(), name='vacancy_detail_url'),
    path('accept_reject/', accept_reject),
    path('help/', help_list, name='help_list_url'),
    path('viewed/', viewed),
    path('admin_jobinterviews/', admin_jobinterviews),
    path('interviews/', interviews_list, name='interviews_list_url'),
    path(r'checkinterviews/', checkinterviews),
    path('upload', upload, name='client_cv_upload'),
    path('upload', upload, name='upload'),
    # # Poland urls (end)
]
