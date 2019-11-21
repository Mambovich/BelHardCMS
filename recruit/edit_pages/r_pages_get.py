import calendar
import datetime
from collections import defaultdict

from BelHardCRM.settings import MEDIA_URL
from client.edit.utility import (time_it, try_except)
from client.models import (Sphere, Sex, Citizenship, FamilyState, Children, City, State)
from recruit.models import (RecruitExperience, UserModel, RecruitTelephone, RecruitEducation, RecruitCertificate,
                            RecruitSkills)


@try_except
@time_it
def recruit_edit_page_get(recruit):  # TeamRome
    """ views.py RecruitEditMain(TemplateView) GET method.
    Загрузка из БД списков для выбора данных Recruit. """
    response = defaultdict()
    # default select fields
    response['sex'] = Sex.objects.all()
    response['citizenship'] = Citizenship.objects.all()
    response['family_state'] = reversed(FamilyState.objects.all())
    response['children'] = reversed(Children.objects.all())
    response['country'] = response['citizenship']
    response['city'] = reversed(City.objects.all())
    response['state'] = reversed(State.objects.all())

    if recruit:
        user_model = UserModel.objects.get(id=recruit.recruiter_id)
        response['user_model'] = {
            "first_name": user_model.first_name,
            "last_name": user_model.last_name,
            "email": user_model.email,
        }
        phone_arr = [i.telephone_number for i in RecruitTelephone.objects.filter(recruit_phone=recruit)]
        response['recruit_phone'] = phone_arr
        response['recruit'] = recruit

    return response


@try_except
@time_it
def recruit_experience_page_get(recruit):  # TeamRome
    response = defaultdict()
    response['sphere'] = Sphere.objects.all()
    if recruit:
        exp = RecruitExperience.objects.filter(recruit_exp=recruit)
        exp_dict = [i for i in exp.values()]
        response['rec_exp'] = exp_dict

        for i, e in enumerate(exp):
            exp_dict[i]['sphere'] = [i['sphere_word'] for i in e.sphere.values()]

    return response


@try_except
@time_it
def recruit_skills_page_get(recruit):  # TeamRome
    response = defaultdict()
    if recruit:
        skills_arr = [i['skill'] for i in RecruitSkills.objects.filter(recruit_skills=recruit).values()]
        response['rec_skill'] = skills_arr

    return response


@try_except
@time_it
def recruit_education_page_get(recruit):  # TeamRome
    response = defaultdict()
    if recruit:
        edus = [i for i in RecruitEducation.objects.filter(recruit_edu=recruit).values()]
        response['rec_edu'] = edus
        edu_id = [e['id'] for e in response['rec_edu']]
        certs = [[c for c in RecruitCertificate.objects.filter(education_id=i).values()] for i in edu_id]
        # print("\tcerts: %s" % certs)
        for e in edus:
            # print("\te: %s" % e)
            for c in certs:
                # print("\tc: %s" % c)
                if c:
                    if c[0]['education_id'] == e['id']:
                        for cert in c:
                            cert['img'] = "%s%s" % (MEDIA_URL, cert['img'])
                        e['cert'] = c
    return response


@try_except
@time_it
def recruit_show_page_get(recruit):  # TeamRome
    response = defaultdict()

    if recruit:
        response['r_edu_profile'] = [i for i in
                                     RecruitEducation.objects.filter(recruit_edu=recruit).values('institution',
                                                                                                 'qualification')]
        response['r_exp_profile'] = [i for i in
                                     RecruitExperience.objects.filter(recruit_exp=recruit).values('start_date',
                                                                                                  'end_date',
                                                                                                  'position',
                                                                                                  'name')]

        response['r_skill_profile'] = [i for i in RecruitSkills.objects.filter(recruit_skills=recruit).values('skill')]

        user_model = UserModel.objects.get(id=recruit.recruiter_id)
        response['user_model'] = {
            "first_name": user_model.first_name,
            "last_name": user_model.last_name,
            "email": user_model.email,
        }
        response['r_phone'] = [i for i in
                               RecruitTelephone.objects.filter(recruit_phone=recruit).values("telephone_number")]

        response["recruit"] = recruit

        data_b = recruit.date_born
        age = None
        if data_b:
            dt_now = datetime.date.today()
            ly = calendar.leapdays(data_b.year, dt_now.year)
            age = int(((dt_now - data_b).days - ly) / 365)
        response["age"] = age
        if age:
            # word for age
            goda = [2, 3, 4]
            a = str(age)[1]

            if int(a) == 1:
                k = 'год'
            elif int(a) in goda:
                k = 'года'
            else:
                k = "лет"
            response["nameage"] = k

        # word for children
        c = str(recruit.children)
        if len(c) == 4:
            g = 'дети'
        else:
            g = 'детей'
        response["namechild"] = g

    return response
