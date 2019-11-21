from client.edit.edit_forms import UploadImgForm
from client.edit.parsers import (pars_edu_request, pars_cv_request, pars_exp_request)
from client.edit.utility import (check_input_str, check_phone)
from client.edit.utility import (time_it, try_except)
from client.models import (Skills, Telephone, Sex, Citizenship, FamilyState, Children, City, State, Client, Education,
                           Certificate, CV, Experience, Sphere, Employment, TimeJob, TypeSalary, UserModel, Direction)


@try_except
@time_it
def edit_page_post(client_instance, request):  # TeamRome
    """ views.py ClientEditMain(TemplateView) POST method. """
    """ Входные данные для сохранения: """
    user = request.user
    user_name = request.POST['client_first_name']
    last_name = request.POST['client_last_name']
    patronymic = request.POST['client_middle_name']
    sex = Sex.objects.get(sex_word=request.POST['sex']) if request.POST['sex'] else None
    date = request.POST['date_born'] if request.POST['date_born'] else None
    citizenship = Citizenship.objects.get(country_word=request.POST['citizenship']) if request.POST[
        'citizenship'] else None
    family_state = FamilyState.objects.get(state_word=request.POST['family_state']) if request.POST[
        'family_state'] else None
    children = Children.objects.get(children_word=request.POST['children']) if request.POST['children'] else None
    country = Citizenship.objects.get(country_word=request.POST['country']) if request.POST['country'] else None
    city = City.objects.get(city_word=request.POST['city']) if request.POST['city'] else None
    street = request.POST['street']
    house = request.POST['house']
    flat = request.POST['flat']
    telegram_link = request.POST['telegram_link']
    skype = request.POST['skype_id']
    email = request.POST['email']
    link_linkedin = request.POST['link_linkedin']
    state = State.objects.get(state_word=request.POST['state']) if request.POST['state'] else None
    # print(user_name, last_name, patronymic, sex, date, citizenship, family_state, children, country, city,
    #       street, house, flat, telegram_link, skype, email, link_linkedin, state)

    if not client_instance:
        """ Если карточки нету - создаём. """
        print('\tUser Profile DO NOT exists - creating!')

        client = Client(
            user_client=user,
            patronymic=patronymic,
            sex=sex,
            date_born=date,
            citizenship=citizenship,
            family_state=family_state,
            children=children,
            country=country,
            city=city,
            street=street,
            house=house,
            flat=flat,
            telegram_link=telegram_link,
            skype=skype,
            link_linkedin=link_linkedin,
            state=state,
        )
        client.save()
    else:
        """ Если карточка есть - достаём из БД Объект = Клиент_id.
        Перезаписываем (изменяем) существующие данныев. """
        print('\tUser Profile exists - Overwriting user data')

        user_model = UserModel.objects.get(id=client_instance.user_client_id)
        user_model.first_name = user_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()

        client = client_instance
        client.name = user_name
        client.last_name = last_name
        client.patronymic = patronymic
        client.sex = sex
        client.date_born = date
        client.citizenship = citizenship
        client.family_state = family_state
        client.children = children
        client.country = country
        client.city = city
        client.street = street
        client.house = house
        client.flat = flat
        client.telegram_link = telegram_link
        client.skype = skype
        client.email = email
        client.link_linkedin = link_linkedin
        client.state = state
        client.save()

    """ Сохранение телефонных номеров клиента """
    tel = request.POST.getlist('phone')
    if any(tel):
        Telephone.objects.filter(client_phone=client_instance).delete()
    for t in tel:
        t = check_phone(t)
        if t:
            phone = Telephone(
                client_phone=client,
                telephone_number=t,
            )
            phone.save()


@try_except
@time_it
def skills_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditSkills(TemplateView) POST method.  """
    skills_arr = request.POST.getlist('skill') if request.POST.getlist('skill') else None

    if any(skills_arr):
        Skills.objects.filter(client_skills=client_instance).delete()
        # print("\tskill: %s" % skills_arr)
        for s in skills_arr:
            if s:
                """ ОБЪЕДИНЕНИЕ модуля Навыки с конкретным залогиненым клиентом!!! """
                skill = Skills(
                    client_skills=client_instance,
                    skill=check_input_str(s, False)
                )
                skill.save()
    else:
        print("\tNo skills")


@try_except
@time_it
def photo_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditPhoto(TemplateView) POST method.
    В БД сохраняется УНИКАЛЬНОЕ имя картинки (пр: user_2_EntrmQR.png) в папке MEDIA_URL = '/media/' """
    form = UploadImgForm(request.POST, request.FILES)
    if form.is_valid():
        img = form.cleaned_data.get('img')
        client_instance.img = img
        client_instance.save()


@try_except
@time_it
def education_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditEducation(TemplateView) POST method.  """
    arr_edu = pars_edu_request(request.POST, request.FILES)  # list of dictionaries

    if any(arr_edu):
        Education.objects.filter(client_edu=client_instance).delete()
        for edus in arr_edu:
            if any(edus.values()):

                education = Education(
                    client_edu=client_instance,
                    institution=edus['institution'],
                    subject_area=edus['subject_area'],
                    specialization=edus['specialization'],
                    qualification=edus['qualification'],
                    date_start=edus['date_start'],
                    date_end=edus['date_end'],
                )
                education.save()

                if edus['certificate']:
                    for c in edus['certificate']:  # array of tuples
                        certificate = Certificate(
                            education=education,
                            img=c[1],
                            link=c[0],
                        )
                        certificate.save()

                # print("\tEducation Form - OK:\n\t", institution, subject_area, specialization, qualification,
                #       date_start, date_end, cert_arr)
            else:
                print('\tEducation Form is Empty')
    else:
        print('\tEducation Parser is Empty')


@try_except
@time_it
def cv_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditCv(TemplateView) POST method. """
    if client_instance:
        arr_cv = pars_cv_request(request.POST)  # list of dictionaries

        if any(arr_cv):
            CV.objects.filter(client_cv=client_instance).delete()

            for cvs in arr_cv:
                if any(cvs.values()):

                    cv = CV(
                        client_cv=client_instance,
                        direction=Direction.objects.get(id=cvs['direction']) if cvs['direction'] else None,
                        position=cvs['position'],
                        employment=Employment.objects.get(id=cvs['employment']) if cvs['employment'] else None,
                        time_job=TimeJob.objects.get(id=cvs['time_job']) if cvs['time_job'] else None,
                        salary=cvs['salary'],
                        type_salary=TypeSalary.objects.get(id=cvs['type_salary']) if cvs['type_salary'] else None,
                    )
                    cv.save()
                    # print("\tCV Form - OK:\n\t", position, employment, time_job, salary, type_salary)
                else:
                    print('\tCv form is Empty')
        else:
            print('\tCV Parser is Empty')
    else:
        print('\tclient_instance = None!')


@try_except
@time_it
def experience_page_post(client_instance, request):  # TeamRome
    """" views.py ClientEditExperience(TemplateView) POST method. """
    arr = pars_exp_request(request.POST)  # list of dictionaries

    if any(arr):
        """ Delete old data for this client. Bug fix for duplicate date save. """
        Experience.objects.filter(client_exp=client_instance).delete()
        for dic in arr:
            if any(dic.values()):
                """ If this dictionary hes any values? than take them and save to Exp. instance. """
                experiences = Experience(
                    client_exp=client_instance,
                    name=dic['name'],
                    position=dic['position'],
                    start_date=dic['start_date'],
                    end_date=dic['end_date'],
                    duties=dic['duties'],
                )
                experiences.save()

                if dic['sphere']:
                    for s in dic['sphere']:
                        if s:
                            """ Save ManyToManyField 'sphere' """
                            sp = Sphere.objects.get(id=s)   # TODO: type(s) == str !!!
                            sp.save()
                            experiences.sphere.add(sp)

                # print("\tExperience Form - OK:\n\t", organisation, spheres, position, start_date, end_date, duties)
            else:
                print('\tExperience Form is Empty')
    else:
        print('\tExperience Parser is Empty')
