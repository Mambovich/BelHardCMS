from time import perf_counter

from django.shortcuts import redirect, render, get_object_or_404
from client.models import Client
from time import perf_counter

from django.shortcuts import redirect, render, get_object_or_404
from client.models import Client
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect


from django.template.context_processors import csrf
from django.urls import reverse
from django.http import HttpResponse
from .models import *


def recruiter_main_page(request):
    return render(request=request, template_name='recruit/main_template_recruiter.html', )


def base_of_clients(request):
    clients = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html', context={'clients': clients})
from django.template.context_processors import csrf
from .forms import FileFieldForm
from django.views.generic.edit import FormView

from django.urls import reverse
from django.http import HttpResponse
from .models import *


def recruiter_main_page(request):
    return render(request=request, template_name='recruit/main_template_recruiter.html', )


def base_of_applicants(request):
    applicants = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants})


def applicant(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    return render(request, 'recruit/recruiter_applicant.html', context={'applicant_user': applicant_user})


def applicant_tasks(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    response = csrf(request)
    response['applicant_user'] = applicant_user
    if request.method == 'POST':
        response['form'] = FileFieldForm()

    else:
        response['form'] = FileFieldForm()

    return render(request, 'recruit/recruiter_tasks_for_applicant.html', context=response)
    return render(request, 'recruit/recruiter_tasks_for_applicant.html', context={'applicant_user': applicant_user})
def base_of_clients(request):
    clients = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html', context={'clients': clients})
from client.models import Chat, Message
from client.models import Chat, Message, Tasks, UserModel, SubTasks, Settings
from datetime import datetime


def recruit_main_page(request):
    return render(request, template_name='recruit/recruit_main_template.html')

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

    send = {'author_id': mes.author.id, 'author_name': mes.author.username, 'message': mes.message, 'message_id': mes.id,
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
    #context['newtask'] = newtask
    return render(request=request, template_name='recruit/add_task.html', context=context)


def add_new_task(requset):
    try:
        user = UserModel.objects.get(username=requset.POST['name'])
    except UserModel.DoesNotExist: #TODO сделать проверку в отправек формы?
        return HttpResponse('Необходимо задать юзера')
    newtask = Tasks.objects.create()
    newtask.user = user
    newtask.title = requset.POST['task_title']
    newtask.comment = str(requset.POST['task_comment'])
    #newtask.time = datetime.now() TODO
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
"""
class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'recruit/recruiter_tasks_for_applicant.html'  # Replace with your template.
    success_url = 'applicant_tasks_url'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def uploading_files(request):
    pass"""
def base_of_applicants(request):
    applicants = Client.objects.all()
    return render(request=request, template_name='recruit/recruiter_base_of_clients.html',
                  context={'applicants': applicants})


def applicant(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    return render(request, 'recruit/recruiter_applicant.html', context={'applicant_user': applicant_user})


def applicant_tasks(request, id_a):
    applicant_user = Client.objects.get(id=id_a)
    response = csrf(request)
    response['applicant_user'] = applicant_user
    # client_instance = client_check(request.user)
    """if request.method == 'POST':
        print('upload file - request.POST')

        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img')
            client_instance.img = img
            client_instance.save()
            """
            # в БД сохраняется УНИКАЛЬНОЕ имя картинки (пр. user_2_EntrmQR.png)
            # в папке MEDIA_URL = '/media/'

#            print('client save photo - OK')
#            return redirect(to='/client/edit')
#    else:
#        print('client_edit_photo - request.GET')
#        response['client_img'] = load_client_img(client_instance)
#        response['form'] = UploadImgForm()

    return render(request, 'recruit/recruiter_tasks_for_applicant.html', context=response)
