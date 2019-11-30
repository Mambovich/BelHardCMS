import json
from django.contrib import auth
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.context_processors import csrf
from django.urls import reverse

# from .forms import UploadImgForm, AddSkillForm, AddSkillFormSet, OpinionForm,
# AnswerForm, MessageForm


from django.utils import timezone

from django.views.generic import View, TemplateView

from client.edit.check_clients import (client_check, load_client_img)

# from .forms import UploadImgForm, EducationFormSet, CertificateFormSet

from .models import *  # TODO change *
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from tika import parser
import re

from client.edit.edit_forms import UploadImgForm
from client.edit.pages_get import (show_profile, edit_page_get,
                                   skills_page_get, cv_page_get,
                                   education_page_get,
                                   experience_page_get)
from client.edit.pages_post import (edit_page_post, skills_page_post,
                                    photo_page_post, cv_page_post,
                                    education_page_post, experience_page_post)
from client.forms import (OpinionForm, AnswerForm, MessageForm)
from client.models import (Client, CV, Tasks, JobInterviews, Chat, Message,
                           Settings, Opinion, Answer, Vacancy, Help)
from client.utils_for_mixins import ObjectResumeMixin

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """


def client_main_page(request):  # !!!!!!!!!!!!!!!!!!!!!Alert
    response = csrf(request)
    # Poland
    try:
        client = Client.objects.get(user_client=request.user)
    except Client.DoesNotExist:
        Client.objects.create(user_client=request.user)
        client = Client.objects.get(user_client=request.user)
    resumes = CV.objects.filter(client_cv=client)  # Poland
    suggestions = 0  # Poland
    for resume in resumes:  # Poland
        suggestions += resume.notification.count()
    readtask = len(Tasks.objects.filter(user=request.user, readtask=False))
    readinterview = len(
        JobInterviews.objects.filter(client=client, readinterview=False))
    chat = Chat.objects.get(members=request.user)
    unread_messages = len(
        Message.objects.filter(chat=chat, is_read=False).exclude(
            author=request.user))
    settings = Settings.objects.get(user=request.user)
    context = {'unread_messages': unread_messages, 'readtask': readtask,
               'settings': settings,
               'readinterview': readinterview}

    # Poland
    response['unread_suggestions'] = suggestions
    client_instance = client_check(request.user)
    response['client_img'] = load_client_img(client_instance)
    context.update(response)
    # print(context['unread_suggestions'])
    return render(request=request,
                  template_name='client/main_template_client.html',
                  context=context)


class ClientProfile(TemplateView):  # TeamRome
    template_name = 'client/client_profile.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': show_profile(client_instance)
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        pass


class ClientEditMain(TemplateView):  # TeamRome
    template_name = 'client/edit_forms/client_edit_main.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': edit_page_get(client_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        client_instance = client_check(request.user)
        edit_page_post(client_instance, request)
        return redirect(to='/client/profile')


class ClientEditSkills(TemplateView):  # TeamRome
    template_name = 'client/edit_forms/client_edit_skills.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': skills_page_get(client_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        client_instance = client_check(request.user)
        if client_instance:
            skills_page_post(client_instance, request)
        return redirect(to='/client/edit')


class ClientEditPhoto(TemplateView):  # TeamRome
    template_name = 'client/edit_forms/client_edit_photo.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'form': UploadImgForm(),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        client_instance = client_check(request.user)
        photo_page_post(client_instance, request)
        return redirect(to='/client/edit')


class ClientEditCv(TemplateView):  # TeamRome
    template_name = 'client/edit_forms/client_edit_cv.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': cv_page_get(client_instance),
                    }  # сюда влетел словарь который сформировался в pages_get
        return render(request, self.template_name,
                      response)  # а здесь он залетел в соответствующий
        # темплейт для заполнения полей

    def post(self, request):
        client_instance = client_check(request.user)
        cv_page_post(client_instance, request)
        return redirect(to='/client/edit')


class ClientEditEducation(TemplateView):  # TeamRome
    template_name = 'client/edit_forms/client_edit_education.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': education_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        client_instance = client_check(request.user)
        education_page_post(client_instance, request)
        return redirect('/client/edit')


class ClientEditExperience(TemplateView):  # TeamRome
    template_name = 'client/edit_forms/client_edit_experience.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    "data": experience_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        client_instance = client_check(request.user)
        experience_page_post(client_instance, request)
        return redirect('/client/edit')


class MessagesView(View):
    def get(self, request):
        try:
            chat = Chat.objects.get(members=request.user)
            if request.user in chat.members.all():
                chat.message_set.filter(is_read=False).exclude(
                    author=request.user).update(is_read=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        unread_messages = len(
            Message.objects.filter(chat=chat, is_read=False).exclude(
                author=request.user))
        context = {'user_profile': request.user,
                   'unread_messages': unread_messages,
                   'chat': chat,
                   'form': MessageForm()}
        client_instance = client_check(request.user)
        context['client_img'] = load_client_img(client_instance)
        return render(request, 'client/client_chat.html', context)

    def post(self, request):
        form = MessageForm(data=request.POST)
        chat = Chat.objects.get(members=request.user)
        print(form)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat.id
            message.author = request.user
            message.save()
        return redirect(reverse('contact_with_centre'))


def answer_create(request, pk):
    opinion = get_object_or_404(Opinion, id=pk)
    answer = Answer.objects.filter(pk=pk)
    form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.opinion = opinion
            form.user = request.user
            form.save()
            return redirect('opinion_detail', pk)
    return render(request, 'opinion/answer_create.html',
                  context={'form': form, 'opinion': opinion, "answer": answer})


def opinion_list(request):
    opinion = Opinion.objects.all()
    return render(request, 'opinion/index.html', context={'opinion': opinion})


class OpinionCreate(View):
    def get(self, request):
        opinions = Opinion.objects.all()
        form = OpinionForm()
        client_instance = client_check(request.user)
        return render(request, 'opinion/opinion_create.html',
                      context={'form': form,
                               'client_img': load_client_img(client_instance),
                               'opinions': opinions})

    def post(self, request):
        opinions = Opinion.objects.all()
        form = OpinionForm(request.POST)

        if form.is_valid():
            new_opinion = form.save(commit=False)
            new_opinion.user = request.user
            new_opinion.save()
            return redirect('opinion_detail', pk=new_opinion.pk)
        client_instance = client_check(request.user)
        return render(request, 'opinion/opinion_create.html',
                      context={'form': form,
                               'client_img': load_client_img(client_instance),
                               'opinions': opinions})


def opinion_detail(request, pk):
    opinion = get_object_or_404(Opinion, pk=pk)
    return render(request, 'opinion/opinion_detail.html', {'opinion': opinion})


class OpinionDelete(View):
    def get(self, request, pk):
        opinion = Opinion.objects.filter(pk=pk)
        return render(request, 'opinion/opinion_delete.html',
                      context={'opinion': opinion})

    def post(self, request, pk):
        opinion = Opinion.objects.filter(pk=pk)
        opinion.delete()
        return redirect(reverse('opinion_list'))


def client_login(request):  # ввести логин/пароль -> зайти в систему
    res = csrf(request)
    res['url'] = 'login'
    if request.user.is_authenticated:  # редирект авторизированых пользователей со страницы логина
        return redirect(to='client')
    if request.POST:
        password = request.POST['password']
        user = request.POST['user']
        u = auth.authenticate(username=user, password=password)
        if u:
            auth.login(request, u)
        else:
            res['error'] = "Неверный login/пароль"
            return render(request, 'registration.html', res)
    else:
        return render(request, 'registration.html', res)
    try:
        user_chat = Chat.objects.get(members=request.user)
    except Chat.DoesNotExist:
        user_chat = Chat.objects.create()
        user_chat.members.add(
            request.user)  # TODO сюда добавить менеджера, которому, по дефолту, передают юзера
    try:
        user_settings = Settings.objects.get(user=request.user)
    except Settings.DoesNotExist:
        user_settings = Settings.objects.create(user=request.user)
    if not Group.objects.filter(name='Users').exists():
        Group.objects.create(name='Users')
    if u.groups.filter(name='Users').exists():
        return redirect('client')
    elif u.groups.filter(name='Recruiters').exists():
        return redirect('recruiter_url')
    else:  # добавляет юзера к группе 'Users' поумолчанию, если у него нет никаких групп
        user_group = Group.objects.get(name='Users')
        u.groups.add(user_group)
        u.save()
        return redirect('client')


def client_logout(request):  # выйти из системы, возврат на стартовую страницу
    auth.logout(request)
    return redirect(to='login')  # вставить редирект куда требуется


def tasks(request):
    task = Tasks.objects.filter(user=request.user, status=False)
    task_false = Tasks.objects.filter(user=request.user,
                                      status=True)  # status=False)
    task_false = sorted(task_false, key=lambda x: x.endtime, reverse=True)
    client_instance = client_check(request.user)
    return render(request, 'client/tasks.html', context={'task': task,
                                                         'task_false': task_false,
                                                         'client_img': load_client_img(
                                                             client_instance)})


def check_subtask(request):
    sub_id = request.GET['sub_id']
    subtask = SubTasks.objects.get(id=sub_id)
    task_id = request.GET['task_id']
    task = Tasks.objects.get(id=task_id)
    subtask_amount = len(task.show_all)

    if subtask.status == False:
        subtask.status = True
        subtask.save()
        return HttpResponse()
    else:
        subtask.status = False
    subtask.save()
    i = 0
    for sub in task.show_all:
        if sub.status == True:
            return HttpResponse()
        else:
            i+= 1

    if i == subtask_amount:
        task.status = True
        task.endtime = timezone.now()
        task.save()

    return HttpResponse()

def checktask(request):
    id = (request.GET['id'])
    task = Tasks.objects.get(id=id)

    if task.status == False:
        task.status = True
        task.endtime = timezone.now()
    else:
        task.status = False
        task.endtime = None
        for sub in task.show_all:
            sub.status = True
            sub.save()

    task.save()
    return HttpResponse(task)


def checknotifications(request):
    client = get_object_or_404(Client, user_client=request.user)
    chat = Chat.objects.get(members=request.user)
    unread_messages = len(
        Message.objects.filter(chat=chat, is_read=False).exclude(
            author=request.user))
    readtask = len(Tasks.objects.filter(user=request.user, readtask=False))
    readinterview = len(
        JobInterviews.objects.filter(client=client, readinterview=False))
    client = Client.objects.get(user_client=request.user)
    resumes = CV.objects.filter(client_cv=client)
    suggestions = 0
    for resume in resumes:
        suggestions += resume.notification.count()

    data = [unread_messages, readtask, suggestions, readinterview]

    return HttpResponse(data)


def settings_menu(request):
    settings = Settings.objects.get(user=request.user)
    context = {'settings': settings, }
    client_instance = client_check(request.user)
    context['client_img'] = load_client_img(client_instance)
    return render(request=request, template_name='client/client_settings.html',
                  context=context)


def set_settings(request):
    setting = request.GET['setting']
    status = request.GET['state'] == 'true'
    settings = Settings.objects.get(user=request.user)

    if setting == 'messages':
        settings.messages = status
    elif setting == 'tasks':
        settings.tasks = status
    elif setting == 'suggestions':
        settings.suggestions = status
    elif setting == 'meetings':
        settings.meetings = status
    elif setting == 'reviews':
        settings.reviews = status
    elif setting == 'email_messages':
        settings.email_messages = status
    elif setting == 'email_tasks':
        settings.email_tasks = status
    elif setting == 'email_suggestions':
        settings.email_suggestions = status
    elif setting == 'email_meetings':
        settings.email_meetings = status
    elif setting == 'email_reviews':
        settings.email_reviews = status

    settings.save()

    return HttpResponse(settings)


def chat_update(request):
    last_id = (request.GET['last_id'])
    chat = Chat.objects.get(members=request.user)
    messages = Message.objects.filter(chat=chat)
    mes = (m for m in messages if m.id > int(last_id))
    if request.user in chat.members.all():
        chat.message_set.filter(is_read=False).exclude(
            author=request.user).update(is_read=True)

    send2 = []
    for s in mes:
        send2.append(
            {'author_id': s.author.id,
             'author_first_name': s.author.first_name,
             'author_last_name': s.author.last_name, 'message': s.message,
             'message_id': s.id,
             'pub_date': s.pub_date.ctime()})
    return JsonResponse(send2, safe=False)


# Poland's views #

#  There's a lot of work to remove all bugs  #
class VacancyDetail(View):
    def get(self, request, id_v):
        client = get_object_or_404(Client, user_client=request.user)
        vacancy = get_object_or_404(Vacancy, id=id_v)
        resume_for_waiting = vacancy.in_waiting_for_resume.filter(
            client_cv=client)
        resume_for_accepted = vacancy.accept_for_resume.filter(
            client_cv=client)
        resume_for_rejected = vacancy.reject_for_resume.filter(
            client_cv=client)
        first_flag = 1 if bool(
            resume_for_waiting or resume_for_rejected) else 0
        second_flag = 1 if bool(
            resume_for_waiting or resume_for_accepted) else 0
        return render(request, 'client/client_vacancy_detail.html', context={
            'vacancy': vacancy,
            'first_flag': first_flag,
            'second_flag': second_flag,
            'resume_for_waiting': resume_for_waiting,
            'resume_for_accepted': resume_for_accepted,
            'resume_for_rejected': resume_for_rejected,
        })


class ResumesList(View):
    def get(self, request):
        client = get_object_or_404(Client, user_client=request.user)
        resumes = CV.objects.filter(client_cv=client)
        client_instance = client_check(request.user)
        return render(request, 'client/client_resumes.html',
                      context={'resumes': resumes,
                               'client_img': load_client_img(client_instance)})


class ResumeDetail(ObjectResumeMixin, View):  # Look utils_for_mixins.py
    template = 'client/client_resume_detail.html'


class AcceptedVacancies(ObjectResumeMixin, View):  # Look utils_for_mixins.py
    template = 'client/client_accepted_vacancies.html'


class RejectedVacancies(ObjectResumeMixin, View):  # Look utils_for_mixins.py
    template = 'client/client_rejected_vacancies.html'


def accept_reject(request):
    client = get_object_or_404(Client, user_client=request.user)
    if request.GET['flag'] == 'accept' and \
            Vacancy.objects.get(
                id=request.GET['id_v']).in_waiting_for_resume.filter(
                client_cv=client):
        print(request.GET['id_v'], 1)
        r = Vacancy.objects.get(
            id=request.GET['id_v']).in_waiting_for_resume.get(client_cv=client)
        v = Vacancy.objects.get(id=request.GET['id_v'])
        r.vacancies_accept.add(v)
        r.vacancies_in_waiting.remove(v)
        r.save()
        return HttpResponse('accept_server')

    elif request.GET['flag'] == 'reject' and \
            Vacancy.objects.get(
                id=request.GET['id_v']).in_waiting_for_resume.filter(
                client_cv=client):
        print(request.GET['id_v'], 2)
        r = Vacancy.objects.get(
            id=request.GET['id_v']).in_waiting_for_resume.get(client_cv=client)
        v = Vacancy.objects.get(id=request.GET['id_v'])
        r.vacancies_reject.add(v)
        r.vacancies_in_waiting.remove(v)
        r.save()
        return HttpResponse('reject_server')

    elif request.GET['flag'] == 'accept' and \
            Vacancy.objects.get(
                id=request.GET['id_v']).reject_for_resume.filter(
                client_cv=client):
        print(request.GET['id_v'], 3)
        r = Vacancy.objects.get(id=request.GET['id_v']).reject_for_resume.get(
            client_cv=client)
        v = Vacancy.objects.get(id=request.GET['id_v'])
        r.vacancies_accept.add(v)
        r.vacancies_reject.remove(v)
        r.save()
        return HttpResponse('accept_server')

    elif request.GET['flag'] == 'reject' and \
            Vacancy.objects.get(
                id=request.GET['id_v']).accept_for_resume.filter(
                client_cv=client):
        print(request.GET['id_v'], 4)
        r = Vacancy.objects.get(id=request.GET['id_v']).accept_for_resume.get(
            client_cv=client)
        v = Vacancy.objects.get(id=request.GET['id_v'])
        r.vacancies_reject.add(v)
        r.vacancies_accept.remove(v)
        r.save()
        return HttpResponse('reject_server')


def help_list(request):
    faqs = Help.objects.all()
    client_instance = client_check(request.user)
    return render(request, 'client/help.html',
                  context={'faqs': faqs,
                           'client_img': load_client_img(client_instance)})


def viewed(request):
    if request.GET['action'] == 'clear':
        client = get_object_or_404(Client, user_client=request.user)
        resumes = CV.objects.filter(client_cv=client)
        for resume in resumes:
            r = resume
            r.notification.clear()
        return HttpResponse('cleared')


def interviews_list(request):
    client = get_object_or_404(Client, user_client=request.user)
    interviews = JobInterviews.objects.filter(client=client, status=False)
    interviews_false = JobInterviews.objects.filter(client=client,
                                                    status=True)  # False
    interviews_false = sorted(interviews_false,
                              key=lambda x: x.period_of_execution,
                              reverse=True)
    client_instance = client_check(request.user)

    return render(request, 'client/interviews.html',
                  context={'interviews': interviews,
                           'interviews_false': interviews_false,
                           'client_img': load_client_img(client_instance)})


def checkinterviews(request):
    id = request.GET['id']
    interviews = JobInterviews.objects.get(id=id)

    if interviews.status == False:
        interviews.status = True
        interviews.period_of_execution = timezone.now()
    else:
        interviews.status = False
        interviews.period_of_execution = None
    interviews.save()
    return HttpResponse(interviews)


def admin_jobinterviews(request):  # for admin panel
    client = Client.objects.get(id=request.GET['id_client'])
    resumes = CV.objects.filter(client_cv=client)
    resumes = {key: val for val, key in [(i.position, i.id) for i in resumes]}
    resumes = json.dumps(resumes, ensure_ascii=False)
    return HttpResponse(resumes)


# PDF upload
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


# PDF Parsing

def parsing():
    raw = parser.from_file('Astapenka Dima.pdf')
    text = (raw['content'])
    client_row = Client.objects.get(id=Client.id)
    lastname_name_exp = re.findall(r'\w+', text)
    lastname = lastname_name_exp[0]
    client_row.lastname = lastname
    name = lastname_name_exp[1]
    client_row.name = name
    sex = lastname_name_exp[2]
    client_row.sex = sex
    email_exp = r'[\w\d.-]+@[\w.]+'
    email = re.findall(email_exp, text)
    client_row.email = email
    phone_exp = \
        [i.strip() for i in re.findall(r'\+?[\s\d()-]+', text) if
         len(i) >= 10][
            1].strip()
    client_row.telephone = phone_exp
    citizenship_exp = re.findall(r'\Г\w+:\s\w+\w', text)
    citizenship = citizenship_exp[0].split()[1]
    client_row.citizenship = citizenship
    city_exp = re.findall(r'\П\w+:\s\w+\w', text)
    city = city_exp[0].split()[1]
    client_row.city = city

    client_row.save()


# End Poland's views #


class ClientShowSkills(TemplateView):  # TeamRome
    template_name = 'client/show/show_skills.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': skills_page_get(client_instance),
                    }
        return render(request=request, template_name=self.template_name,
                      context=response)

    def post(self, request):
        pass


class ClientShowEducation(TemplateView):  # TeamRome
    template_name = 'client/show/show_education.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': education_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        pass


class ClientShowExperience(TemplateView):  # TeamRome
    template_name = 'client/show/show_experience.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    "data": experience_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        pass


class ClientShowCv(TemplateView):  # TeamRome
    template_name = 'client/show/show_cv.html'

    def get(self, request, *args, **kwargs):
        client_instance = client_check(request.user)
        response = {'client_img': load_client_img(client_instance),
                    'data': cv_page_get(client_instance),
                    }
        return render(request, self.template_name, response)

    def post(self, request):
        pass
