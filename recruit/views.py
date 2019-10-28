from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

from client.edit.check_clients import (load_client_img)
from client.models import (CV, JobInterviews, FilesForJobInterviews, Vacancy, State)
from client.models import (Chat, Message, Tasks, UserModel, SubTasks, Settings, Client)
from recruit.edit_pages.check_recruit import (recruit_check)
from recruit.edit_pages.r_forms import (RecruitUploadImgForm)
from recruit.edit_pages.r_pages_get import (recruit_edit_page_get, recruit_experience_page_get,
                                            recruit_education_page_get, recruit_show_page_get)
from recruit.edit_pages.r_pages_get import (skills_page_get)
from recruit.edit_pages.r_pages_post import (photo_page_post, skills_page_post, recruit_education_page_post)
from recruit.edit_pages.r_pages_post import (recruit_edit_page_post, recruit_experience_page_post)
from recruit.models import (Recruiter)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """


# There is Poland's views #################################################################################
def recruit_main_page(request):  # TeamRome
    recruit_instance = recruit_check(request.user)
    response = {'recruit_img': load_client_img(recruit_instance),
                'data': 'foo()',
                }
    return render(request, template_name='recruit/recruit_main_template.html', context=response)


def recruiter_base(request):
    return render(request, template_name='recruit/recruiter_base.html', )


def base_of_applicants(request):
    applicants = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants})


def applicant(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    return render(request, 'recruit/recruiter_applicant.html', context={'applicant_user': applicant_user})


class CreateJobInterview(View):
    def get(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        if CV.objects.filter(client_cv=applicant_user):
            accepted_vacancies = applicant_user.cv_set.all()[0].vacancies_accept.all()
            for resume in applicant_user.cv_set.all()[1:]:
                accepted_vacancies |= resume.vacancies_accept.all()
            # print(accepted_vacancies)
        else:
            accepted_vacancies = None
        return render(request, 'recruit/recruiter_tasks_for_applicant.html',
                      context={'applicant_user': applicant_user, 'accepted_vacancies': accepted_vacancies})

    def post(self, request, id_a):
        applicant_user = Client.objects.get(id=id_a)
        response = request.POST
        files = request.FILES.getlist('files')
        j = JobInterviews(
            client=applicant_user,
            name=response.get('name'),
            jobinterviewtime=response.get('time'),
            jobinterviewdate=response.get('date'),
            # interview_author=Recruiter.objects.get(id=), ################ Filling in this field will be automatic
            # period_of_execution= ###############################          I don't know why is this field needed
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
        # interview_author=Recruiter.objects.get(id=) ################ Filling in this field will be automatic
        # period_of_execution= ###############################          I don't know why is this field needed
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


# End Poland's views #######################################################################################


def recruit_chat(request):
    chat_list = Chat.objects.filter(members=request.user)
    for chat in chat_list:
        mes = chat.members.all()
        for m in mes:
            print(m.username)
    context = {'user': request.user, 'chats': chat_list}
    return render(request=request, template_name='recruit/recruit_chat.html', context=context)


def get_messages(request):
    chat_id = (request.GET['chat_id'])
    chat = Chat.objects.get(id=chat_id)
    messages = Message.objects.filter(chat=chat)

    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in messages:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def send_message(request):
    chat = Chat.objects.get(id=request.GET['chat_id'])
    mes = Message(chat=chat, author=request.user, message=request.GET['message'])
    members = chat.members.all()
    mes.save()

    for m in members:
        if m != request.user:
            try:
                if Settings.objects.get(user=m).email_messages:
                    send_email = EmailMessage('HR-system', 'У вас новое сообщение', to=[str(m.email)])
                    send_email.send()
            except Exception:
                print('Exception: нет адреса электронной почты')

    send = {'author_id': mes.author.id, 'author_name': mes.author.username, 'message': mes.message,
            'message_id': mes.id,
            'pub_date': mes.pub_date.ctime()}
    return JsonResponse(send, safe=False)


def chat_update(request):
    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(id=request.GET['chat_id'])
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id, 'author_name': s.author.username, 'message': s.message, 'message_id': s.id,
             'pub_date': s.pub_date.ctime()})

    return JsonResponse(send2, safe=False)


def check_mes(request):
    chat = Chat.objects.filter(members=request.user)
    send = []
    for c in chat:
        unread_messages = len(Message.objects.filter(chat=c, is_read=False).exclude(author=request.user))
        new_dict = {'chat_id': c.id, 'count': unread_messages}
        send.append(new_dict)

    return JsonResponse(send, safe=False)


def add_task(request):
    context = {}
    context['users_list'] = UserModel.objects.all()
    # context['newtask'] = newtask
    return render(request=request, template_name='recruit/add_task.html', context=context)


def add_new_task(requset):
    try:
        user = UserModel.objects.get(username=requset.POST['name'])
    except UserModel.DoesNotExist:  # TODO сделать проверку в отправек формы?
        return HttpResponse('Необходимо задать юзера')
    newtask = Tasks.objects.create()
    newtask.user = user
    newtask.title = requset.POST['task_title']
    newtask.comment = str(requset.POST['task_comment'])
    # newtask.time = datetime.now() TODO
    newtask.save()
    i = 1
    reqpost = requset.POST
    while True:
        try:
            newsubtask = SubTasks(title=reqpost['task_subtask' + str(i)], task=newtask)
        except:
            break
        i += 1
        newsubtask.save()

        try:
            if Settings.objects.get(user=user).email_messages:
                send_email = EmailMessage('HR-system', 'У вас новая задача', to=[str(user.email)])
                send_email.send()
        except Exception:
            print('Exception: нет адреса электронной почты')

    return redirect(to='add_task')


def favorites(request):
    recruit = Recruiter.objects.get(recruiter=request.user)
    clients = Client.objects.filter(own_recruiter=recruit)
    context = {'clients': clients}

    return render(request, template_name='recruit/favorites.html', context=context)


# обработка избранного рекрутера
def check_favor(request):
    client_id = (request.GET['client'])
    client = Client.objects.get(id=client_id)
    recruit_id = (request.GET['recruit'])
    recruit = Recruiter.objects.get(recruiter=UserModel.objects.get(id=recruit_id))
    if client.is_reserved == True:
        client.is_reserved = False
        client.own_recruiter = None
    else:
        client.is_reserved = True
        client.own_recruiter = recruit
    client.save()
    return HttpResponse(client_id)


def recruit_base(request):
    recruit = Recruiter.objects.get(recruiter=request.user)
    search_request = request.GET.get('recruit_search', '')
    clients_after_search = set()
    if search_request:
        search_params = search_request.split(' ')
        print(search_params)
        clients = Client.objects.all()

        for s in search_params:
            users_for_first_name_list = UserModel.objects.filter(first_name__contains=s)
            users_for_last_name_list = UserModel.objects.filter(last_name__contains=s)
            users_for_patronymic = clients.filter(patronymic__contains=s)
            try:
                users_for_state = clients.filter(state__contains=State.objects.get(state_word=s))
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
        clients_after_search = Client.objects.filter(own_recruiter=None)
    context = {'free_clients': clients_after_search}
    return render(request, template_name='recruit/recruit_base.html', context=context)


class RecruitProfile(TemplateView):  # TeamRome
    template_name = 'recruit/recruit_profile.html'

    def get(self, request, *args, **kwargs):
        recruit_instance = recruit_check(request.user)
        response = {'recruit_img': load_client_img(recruit_instance),
                    'data': recruit_show_page_get(recruit_instance),
                    }
        return render(request=request, template_name=self.template_name, context=response)

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
        response = {'client_img': load_client_img(recruit_instance),
                    'form': RecruitUploadImgForm(),
                    }
        return render(request=request, template_name=self.template_name, context=response)

    def post(self, request):
        recruit_instance = recruit_check(request.user)
        photo_page_post(recruit_instance, request)
        return redirect(to='/recruit/edit')
