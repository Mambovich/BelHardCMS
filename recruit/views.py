
from time import perf_counter
from collections import defaultdict

from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, TemplateView
from django.views.generic.edit import FormView
from django.template.context_processors import csrf
from django.urls import reverse

from client.edit.check_clients import (load_client_img)
from client.models import (CV, JobInterviews, FilesForJobInterviews, Vacancy,
                           State)
from client.models import (Chat, Message, Tasks, UserModel, SubTasks, Settings,
                           Client)
from recruit.edit_pages.check_recruit import (recruit_check)
from recruit.edit_pages.r_forms import (RecruitUploadImgForm)
from recruit.edit_pages.r_pages_get import (recruit_edit_page_get,
                                            recruit_experience_page_get,
                                            recruit_education_page_get,
                                            recruit_show_page_get)
from recruit.edit_pages.r_pages_get import (skills_page_get)
from recruit.edit_pages.r_pages_post import (photo_page_post, skills_page_post,
                                             recruit_education_page_post)
from recruit.edit_pages.r_pages_post import (recruit_edit_page_post,
                                             recruit_experience_page_post)
from recruit.models import (Recruiter)

from datetime import datetime
from client.models import *
from .models import * #TODO fix *
from .forms import RecruitReportsClientsForm

from .models import *  # TODO fix *

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """


# There is Poland's views #
def recruit_main_page(request):  # TeamRome
    recruit_instance = recruit_check(request.user)
    response = {'recruit_img': load_client_img(recruit_instance),
                'data': 'foo()',
                }
    return render(request, template_name='recruit/recruit_main_template.html',
                  context=response)


def recruiter_base(request):
    return render(request, template_name='recruit/recruiter_base.html', )


def recruiter_base(request):
    return render(request, template_name='recruit/recruiter_base.html', )


def base_of_applicants(request):
    # applicants = Client.objects.all()
    own_status = 'all'

    # Для проверки на наличие в списке избранного
    recruiter = Recruiter.objects.get(recruiter=request.user)
    owner_list = Client.objects.filter(own_recruiter=recruiter)
    owner_range = len(owner_list)

    clients_after_search = client_filtration(request, own_status)
    applicants = clients_after_search
    return render(request,
                  template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants,
                           'owner_list': owner_list,
                           'owner_range': owner_range})


class ApplicantDet(View):
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        resumes = applicant_user.cv_set.all()
        vacancies = Vacancy.objects.all()
        return render(request, 'recruit/recruiter_applicant.html',
                      context={'applicant_user': applicant_user,
                               'resumes': resumes, 'vacancies': vacancies})

    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        resume = CV.objects.get(id=response['id_cv'])
        vacancies_id = request.POST.getlist('id_v')

        print('resume  ', resume)
        print('vacansies_id ', vacancies_id)
        for id_v in vacancies_id:
            vacancy = Vacancy.objects.get(id=id_v)
            resume.vacancies_in_waiting.add(vacancy)
            resume.notification.add(vacancy)
            print(vacancy)

        return redirect(applicant_user.get_absolute_url())


class CreateJobInterview(View):
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        if CV.objects.filter(client_cv=applicant_user):
            accepted_vacancies = applicant_user.cv_set.all()[
                0].vacancies_accept.all()
            for resume in applicant_user.cv_set.all()[1:]:
                accepted_vacancies |= resume.vacancies_accept.all()
            # print(accepted_vacancies)
        else:
            accepted_vacancies = None
        return render(request, 'recruit/recruiter_tasks_for_applicant.html',
                      context={'applicant_user': applicant_user,
                               'accepted_vacancies': accepted_vacancies})

    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST

        files = request.FILES.getlist('files')
        j = JobInterviews(
            client=applicant_user,
            name=response.get('name'),
            jobinterviewtime=response.get('time'),
            jobinterviewdate=response.get('date'),
            # interview_author=Recruiter.objects.get(id=),
            # Filling in this field will be automatic
            # period_of_execution= #  I don't know why is this field needed
            position=response.get('position'),
            organization=response.get('organization'),
            responsible_person=response.get('responsible_person'),
            contact_responsible_person_1str=response.get('phone'),
            contact_responsible_person_2str=response.get('telegram'),
            location=response.get('address'),
            additional_information=response.get('addition'),
        )
        if response.get('vacancy'):
            j.vacancies = Vacancy.objects.get(id=int(response.get('vacancy')))
        j.save()
        if files:
            for file in files:
                # print(file)
                f = FilesForJobInterviews(
                    add_file=file,
                    jobinterviews_files=j,
                )
                f.save()
        return redirect(applicant_user.get_tasks_url())


class EditJobInterview(View):
    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        files = request.FILES.getlist('files')
        # print(request.POST['id_job_edit'])
        j = JobInterviews.objects.get(id=request.POST['id_job_edit'])
        j.name = response.get('name')
        j.jobinterviewtime = response.get('time')
        j.jobinterviewdate = response.get('date')
        # interview_author=Recruiter.objects.get(id=) # Filling in this field
        # will be automatic
        # period_of_execution= # I don't know why is this field needed
        j.position = response.get('position')
        j.organization = response.get('organization')
        j.responsible_person = response.get('responsible_person')
        j.contact_responsible_person_1str = response.get('phone')
        j.contact_responsible_person_2str = response.get('telegram')
        j.location = response.get('address')
        j.additional_information = response.get('addition')

        if response.get('vacancy'):
            j.vacancies = Vacancy.objects.get(id=int(response.get('vacancy')))
        j.save()
        if files:
            for file in files:
                # print(file)
                f = FilesForJobInterviews(
                    add_file=file,
                    jobinterviews_files=j,
                )
                f.save()
        return redirect(applicant_user.get_tasks_url())


class DelJobInterview(View):
    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        j = JobInterviews.objects.get(id=request.POST['id_job'])
        j.delete()
        return redirect(applicant_user.get_tasks_url())


class Vacancies(View):
    def get(self, request):
        vacancies = Vacancy.objects.all()
        return render(request, 'recruit/recruiter_vacancies.html',
                      context={'vacancies': vacancies})

    def post(self, request):
        response = request.POST
        v = Vacancy(
            state=response['position'],
            salary=response['salary'],
            organization=response['organization'],
            address=response['address'],
            employment=response['employment'],
            description=response['description'],
            skills=response['skills'],
            requirements=response['requirements'],
            duties=response['duties'],
            conditions=response['conditions'],
        )
        v.save()
        return redirect('vacancies_url')


class VacancyDet(View):
    def get(self, request, id_v):
        vacancy = Vacancy.objects.get(id=id_v)
        return render(request, 'recruit/recruiter_vacancy_detail.html',
                      context={'vacancy': vacancy})

    def post(self, request, id_v):
        response = request.POST
        v = Vacancy.objects.get(id=id_v)

        v.state = response['position']
        v.salary = response['salary']
        v.organization = response['organization']
        v.address = response['address']
        v.employment = response['employment']
        v.description = response['description']
        v.skills = response['skills']
        v.requirements = response['requirements']
        v.duties = response['duties']
        v.conditions = response['conditions']

        v.save()

        return redirect(v.get_absolute_url2())


class DelVacancy(View):
    def post(self, request, id_v):
        v = Vacancy.objects.get(id=request.POST['id_vac'])
        v.delete()
        return redirect('vacancies_url')


def reports(request):
    return render(request, 'recruit/recruit_reports.html')


class EmployedClients(View):
    def get(self, request):
        starting_period = request.GET.get('starting_period', '')
        end_period = request.GET.get('end_period', '')
        speciality = request.GET.get('speciality', '')
        print(starting_period)
        print(end_period)
        print(speciality)
        #form = RecruitReportsClientsForm()
        recruit = Recruiter.objects.get(recruiter=request.user)
        recruit_clients = client_filtration(request, recruit)
        context = {
            'recruit_clients': recruit_clients,
        }
        return render(request, 'recruit/recruit_employed_clients.html', context=context)

    def post(self, request):
        response = request.POST
        return redirect('employed_clients_url')


# End Poland's views #


def recruit_chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    for chat in chat_list:
        mes = chat.members.all()
        for m in mes:
            print(m.username)
    context = {'user': request.user, 'chats': chat_list}
    return render(request=request, template_name='recruit/recruit_chat.html',
                  context=context)


def get_messages(request):
    chat_id = (request.GET['chat_id'])
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(
            author=request.user).update(is_read=True)

    send2 = []
    for s in messages:
        send2.append(
            {'author_id': s.author.id, 'user_id': request.user.id,
             'author_first_name': s.author.first_name,
             'author_last_name': s.author.last_name, 'message': s.message,
             'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def send_message(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])
    mes = Message(chat=chat, author=request.user,
                  message=request.GET['message'])
    members = chat.members.all()
    mes.save()

    for m in members:
        if m != request.user:
            try:
                if Settings.objects.get(user=m).email_messages:
                    send_email = EmailMessage('HR-system',
                                              'У вас новое сообщение',
                                              to=[str(m.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')

    send = {'author_id': mes.author.id, 'user_id': request.user.id,
            'author_first_name': mes.author.first_name,
            'author_last_name': mes.author.last_name, 'message': mes.message,
            'message_id': mes.id,
            'pub_date': mes.pub_date.ctime()}

    return JsonResponse(send, safe=False)


def chat_update(request):
    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(id=request.GET['chat_id'])
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(
            author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username,
             'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def check_mes(request):
    chat = Chat.objects.filter(members=request.user)
    send = []
    for c in chat:
        unread_messages = len(
            Message.objects.filter(chat=c, is_read=False).exclude(
                author=request.user))
        new_dict = {'chat_id': c.id, 'count': unread_messages}
        send.append(new_dict)

    return JsonResponse(send, safe=False)


class pattern_task(View):

    def get(self, request):
        client_id = request.GET['user_id']
        pattern_tasks = RecruitPatternClient.objects.all()
        check = 1

        return render(request, template_name='recruit/pattern_task.html', context={'client_id': client_id,
                                                                                   'pattern_tasks': pattern_tasks,
                                                                                   'check': check})

    def post(self, request):
        if 'form1' in request.POST:
            client_id = request.POST['user_id']
            client = Client.objects.get(id=client_id)
            pattern_tasks = RecruitPatternClient.objects.all()
            chosen_task = RecruitPatternClient.objects.get(title=request.POST['pattern_task'])
            chosen_id = chosen_task.id
            check = 2
            return render(request, template_name='recruit/pattern_task.html', context={'client_id': client_id,
                                                                                       'pattern_tasks': pattern_tasks,
                                                                                       'check': check,
                                                                                       'task': chosen_task,
                                                                                       'task_id': chosen_id})

        if 'form2' in request.POST:
           # return HttpResponse('test area')
            client = Client.objects.get(id=request.POST['user_id'])
            client_user = client.user_client
            newtask = Tasks.objects.create()
            newtask.user = client_user
            newtask.title = request.POST['task_title']
            newtask.comment = str(request.POST['task_comment'])
            newtask.save()
            i = 1
            reqpost = request.POST
            while True:
                try:
                    newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
                except:
                    break
                i += 1
                newsubtask.save()

            try:
                if Settings.objects.get(user=client).email_messages:
                    send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(client.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')
            return redirect(client.get_add_client_task())
        else:
            return HttpResponse('ОШИБКА В НАЗВАНИИ ФФОРЫФ')


class change_task(View):
    def get(self, request, id_t):
        task = Tasks.objects.get(id=id_t)
        sub_len = len(task.show_all)
        return render(request, template_name='recruit/change_client_task.html', context={'task_id': id_t,
                                                                                         'task': task,
                                                                                         'sub_len': sub_len})

    def post(self, request, id_t):
        task = Tasks.objects.get(id=id_t)
        task_user = task.user
        client = Client.objects.get(user_client=task_user)
        task.title = request.POST['task_title']
        task.comment = str(request.POST['task_comment'])
        subtasks = task.show_all
        task.save()


        for sub in subtasks:
            sub.title = request.POST['subtask_' + str(sub.id)]
            sub.save()


        return redirect(client.get_add_client_task())



class client_task_adding(View):

    def get(self, request, id_a):
        client = Client.objects.get(id=id_a)
        client_user = client.user_client #ссылается на UserModel
        client_activ_tasks = Tasks.objects.filter(user=client_user, status=False) #просмотр активных задач клинета
        return render(request, template_name='recruit/adding_task_to_client.html', context={'client':client,
                                                                                            'client_user': client_user,
                                                                                            'client_activ_tasks':client_activ_tasks,})


    def post(self, request, id_a):
        client = Client.objects.get(id=id_a)
        client_user = client.user_client
        newtask = Tasks.objects.create()
        newtask.user = client_user
        newtask.title = request.POST['task_title']
        newtask.comment = str(request.POST['task_comment'])
        newtask.save()
        i = 1
        reqpost = request.POST
        while True:
            try:
                newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
            except:
                break
            i += 1
            newsubtask.save()

        try:
            if Settings.objects.get(user=client).email_messages:
                send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(client.email)])
                send_email.send()
        except Exception:
            print('Exception: нет адреса электронной почты')
        return redirect(client.get_add_client_task())

# список избранных клиентов, для рекрутера
def favorites(request):
    own_status = Recruiter.objects.get(recruiter=request.user)
    # own_status = recruit
    clients = client_filtration(request, own_status)
    context = {'applicants': clients}

    return render(request, template_name='recruit/favorites.html',
                  context=context)


# обработка избранного рекрутера
def check_favor(request):
    client_id = (request.GET['client'])
    client = Client.objects.get(id=client_id)
    recruit_id = (request.GET['recruit'])
    recruit = Recruiter.objects.get(
        recruiter=UserModel.objects.get(id=recruit_id))
    if client.is_reserved == True:

        client.is_reserved = False
        client.own_recruiter = None
        chat = Chat.objects.get(members=client.user_client)
        chat.members.remove(recruit.recruiter)
    else:
        client.is_reserved = True
        client.own_recruiter = recruit
        chat = Chat.objects.get(members=client.user_client)
        chat.members.add(recruit.recruiter)
    client.save()
    return HttpResponse(client_id)


# список незарезервированных клиентов, для рекрутера
def recruit_base(request):
    applicants = Client.objects.all()
    own_status = None
    clients_after_search = client_filtration(request, own_status)
    context = {'free_clients': clients_after_search, 'applicants': applicants}
    return render(request, template_name='recruit/recruit_base.html',
                  context=context)


# функция поиска по списку клиентов, для рекрутера
def client_filtration(request, own_status):
    recruit = Recruiter.objects.get(recruiter=request.user)
    search_request = request.GET.get('recruit_search', '')
    clients_after_search = set()
    if search_request:
        search_params = search_request.split(' ')
        print(search_params)
        clients = Client.objects.all()

        for s in search_params:
            users_for_first_name_list = UserModel.objects.filter(
                first_name__contains=s)
            users_for_last_name_list = UserModel.objects.filter(
                last_name__contains=s)
            users_for_patronymic = clients.filter(patronymic__contains=s)
            try:
                users_for_state = clients.filter(
                    state__contains=State.objects.get(state_word=s))
                clients_after_search.update(users_for_state)
            except:
                print('ясно')
            users_for_first_name = set()
            users_for_last_name = set()
            for u in users_for_first_name_list:
                users_for_first_name.add(clients.get(user_client=u))
            for u in users_for_last_name_list:
                users_for_last_name.add(clients.get(user_client=u))

            clients_after_search.update(users_for_first_name)
            clients_after_search.update(users_for_last_name)
            clients_after_search.update(users_for_patronymic)
    else:
        if own_status == 'all':
            clients_after_search = Client.objects.all()
            return clients_after_search
        clients_after_search = Client.objects.filter(own_recruiter=own_status)

    return clients_after_search


class RecruitProfile(TemplateView):  # TeamRome
    template_name = 'recruit/recruit_profile.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_show_page_get(recruit_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        pass


class RecruitEditMain(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_edit_main.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_edit_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_edit_page_post(recruit_instance, request)
        return redirect(to='/recruit/profile/')


class RecruitEditExperience(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_edit_experience.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    "data": recruit_experience_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_experience_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit/')


class RecruitEditEducation(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_edit_education.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_education_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        recruit_education_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit/')


class RecruitEditSkills(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_skills.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': skills_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        skills_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit')


class RecruitEditPhoto(TemplateView):  # TeamRome
    template_name = 'recruit/edit_pages/recruit_photo.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'form': RecruitUploadImgForm(),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        photo_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit')


class RecruitShowSkills(TemplateView):  # TeamRome
    template_name = 'recruit/show/show_skills.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': skills_page_get(recruit_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)


class RecruitShowEducation(TemplateView):  # TeamRome
    template_name = 'recruit/show/show_education.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_education_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)


class RecruitShowExperience(TemplateView):  # TeamRome
    template_name = 'recruit/show/show_experience.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    "data": recruit_experience_page_get(recruit_instance),
                    }
        return render(request, self.template_name, response)

