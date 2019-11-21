from client.edit.edit_forms import UploadImgForm
from client.edit.parsers import (pars_exp_request, pars_edu_request)
from client.edit.utility import (time_it, try_except, check_input_str, check_home_number, check_telegram, check_phone)
from client.models import (Sphere, Sex, Citizenship, FamilyState, Children, City, State)
from recruit.models import (RecruitExperience, UserModel, Recruiter, RecruitTelephone, RecruitEducation,
                            RecruitCertificate)
from recruit.models import (RecruitSkills)


@try_except
@time_it
def recruit_edit_page_post(recruit_instance, request):  # TeamRome
    """ views.py RecruitEditMain(TemplateView) POST method. """
    """ Входные данные для сохранения: """
    user = request.user
    user_name = check_input_str(request.POST['recruit_first_name'])
    last_name = check_input_str(request.POST['recruit_last_name'])
    patronymic = check_input_str(request.POST['recruit_middle_name'])
    sex = Sex.objects.get(sex_word=request.POST['sex']) if request.POST['sex'] else None
    date_born = request.POST['date_born'] if request.POST['date_born'] else None
    citizenship = Citizenship.objects.get(country_word=request.POST['citizenship']) if request.POST[
        'citizenship'] else None
    family_state = FamilyState.objects.get(state_word=request.POST['family_state']) if request.POST[
        'family_state'] else None
    children = Children.objects.get(children_word=request.POST['children']) if request.POST['children'] else None
    country = Citizenship.objects.get(country_word=request.POST['country']) if request.POST['country'] else None
    city = City.objects.get(city_word=request.POST['city']) if request.POST['city'] else None
    street = check_input_str(request.POST['street'])
    house = check_home_number(request.POST['house'])
    flat = check_home_number(request.POST['flat'])
    telegram_link = check_telegram(request.POST['telegram_link'])
    skype = check_input_str(request.POST['skype_id'])
    email = request.POST['email']
    link_linkedin = request.POST['link_linkedin']
    state = State.objects.get(state_word=request.POST['state']) if request.POST['state'] else None

    if not recruit_instance:
        """ Если карточки нету - создаём. """
        print('\tUser Profile DO NOT exists - creating!')
        recruit = Recruiter(
            recruiter=user,
            patronymic=patronymic,
            sex=sex,
            date_born=date_born,
            r_citizenship=citizenship,
            family_state=family_state,
            children=children,
            r_country=country,
            city=city,
            street=street,
            house=house,
            flat=flat,
            telegram_link=telegram_link,
            skype=skype,
            link_linkedin=link_linkedin,
            state=state,
        )
        recruit.save()
    else:
        """ Если карточка есть - достаём из БД Объект = Клиент_id.
        Перезаписываем (изменяем) существующие данныев. """
        print('\tUser Profile exists - Overwriting user data')
        user_model = UserModel.objects.get(id=recruit_instance.recruiter_id)
        user_model.first_name = user_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()

        recruit = recruit_instance
        recruit.name = user_name
        recruit.last_name = last_name
        recruit.patronymic = patronymic
        recruit.sex = sex
        recruit.date_born = date_born
        recruit.r_citizenship = citizenship
        recruit.family_state = family_state
        recruit.children = children
        recruit.r_country = country
        recruit.city = city
        recruit.street = street
        recruit.house = house
        recruit.flat = flat
        recruit.telegram_link = telegram_link
        recruit.skype = skype
        recruit.email = email
        recruit.link_linkedin = link_linkedin
        recruit.state = state
        recruit.save()

    """ Сохранение телефонных номеров клиента """
    tel = request.POST.getlist('phone')
    if any(tel):
        RecruitTelephone.objects.filter(recruit_phone=recruit_instance).delete()
    for t in tel:
        t = check_phone(t)
        if t:
            phone = RecruitTelephone(
                recruit_phone=recruit,
                telephone_number=t,
            )
            phone.save()


@try_except
@time_it
def recruit_experience_page_post(recruit_instance, request):  # TeamRome
    """" views.py ClientEditExperience(TemplateView) POST method. """
    arr = pars_exp_request(request.POST)  # list of dictionaries

    if any(arr):
        """ Delete old data for this recruit. Bug fix for duplicate date save. """
        RecruitExperience.objects.filter(recruit_exp=recruit_instance).delete()
        for dic in arr:
            if any(dic.values()):
                """ If this dictionary hes any values? than take them and save to Exp. instance. """
                organisation = dic['name']
                position = dic['position']
                start_date = dic['start_date']
                end_date = dic['end_date']
                duties = dic['duties']

                experiences = RecruitExperience(
                    recruit_exp=recruit_instance,
                    name=organisation,
                    position=position,
                    start_date=start_date,
                    end_date=end_date,
                    duties=duties,
                )
                experiences.save()

                spheres = dic['sphere']
                for s in spheres:
                    if s:
                        """ Save ManyToManyField 'sphere' """
                        sp = Sphere.objects.get(id=s)
                        sp.save()
                        experiences.sphere.add(sp)
            else:
                print('\tExperience Form is Empty')
    else:
        print('\tExperience Parser is Empty')



@time_it
def recruit_skills_page_post(recruit_instance, request):  # TeamRome
    skills_arr = request.POST.getlist('skill') if request.POST.getlist('skill') else None

    if any(skills_arr):
        RecruitSkills.objects.filter(recruit_skills=recruit_instance).delete()
        print("\t skill: %s" % skills_arr)
        for s in skills_arr:
            if s:
                skill = RecruitSkills(
                    recruit_skills=recruit_instance,
                    skill=s,
                )
                skill.save()
    else:
        print("\tNo skills")


@try_except
@time_it
def photo_page_post(recruit_instance, request):  # TeamRome
    if recruit_instance:
        form = UploadImgForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data.get('img')
            recruit_instance.img = img
            recruit_instance.save()


@try_except
@time_it
def recruit_education_page_post(recruit_instance, request):  # TeamRome
    arr_edu = pars_edu_request(request.POST, request.FILES)  # list of dictionaries

    if any(arr_edu):
        RecruitEducation.objects.filter(recruit_edu=recruit_instance).delete()
        for edus in arr_edu:
            if any(edus.values()):

                institution = edus['institution']
                subject_area = edus['subject_area']
                specialization = edus['specialization']
                qualification = edus['qualification']
                date_start = edus['date_start']
                date_end = edus['date_end']
                cert_arr = edus['certificate']

                education = RecruitEducation(
                    recruit_edu=recruit_instance,
                    institution=institution,
                    subject_area=subject_area,
                    specialization=specialization,
                    qualification=qualification,
                    date_start=date_start,
                    date_end=date_end,
                )
                education.save()

                for c in cert_arr:  # array of tuples
                    certificate = RecruitCertificate(
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
