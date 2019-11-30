from django.contrib.auth import get_user_model
from django.db import models

from client.models import (Sex, Citizenship, FamilyState, Children, City,
                           State, Sphere)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """

UserModel = get_user_model()


class Recruiter(models.Model):  # TeamRome
    class Meta:
        permissions = (("can_use_page", "page permission"),)
    recruiter = models.OneToOneField(UserModel, on_delete=models.CASCADE)

    patronymic = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True,
                            blank=True)

    date_born = models.DateField(null=True, blank=True)
    r_citizenship = models.ForeignKey(Citizenship,
                                      related_name='r_citizenship',
                                      on_delete=models.SET_NULL,
                                      null=True, blank=True)
    family_state = models.ForeignKey(FamilyState, on_delete=models.SET_NULL,
                                     null=True, blank=True)
    children = models.ForeignKey(Children, on_delete=models.SET_NULL,
                                 null=True, blank=True)
    r_country = models.ForeignKey(Citizenship, related_name='r_country',
                                  on_delete=models.SET_NULL, blank=True,
                                  null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True,
                             blank=True)
    street = models.CharField(max_length=100, verbose_name='Улица', null=True,
                              blank=True)
    house = models.CharField(max_length=100, verbose_name='Номер дома',
                             null=True, blank=True)
    flat = models.CharField(max_length=10, verbose_name='Квартира', null=True,
                            blank=True)
    telegram_link = models.CharField(max_length=100, blank=True, null=True,
                                     verbose_name='Ник в телеграмме')  # при верстке учесть @
    link_linkedin = models.URLField(max_length=200, null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)
    img = models.ImageField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True,
                              blank=True)

    def __str__(self):
        return "%s %s %s" % (
        self.recruiter.first_name, self.recruiter.last_name, self.patronymic)


class RecruitExperience(models.Model):  # TeamRome
    """ Опыт работы. ForeignKey = несколько видов опыта работы у одного recruit. """
    recruit_exp = models.ForeignKey(to='Recruiter', on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=True, blank=True,
                            verbose_name='organisation')
    sphere = models.ManyToManyField(Sphere,
                                    verbose_name='sphere')  # ??? not more 3
    position = models.CharField(max_length=100, null=True, blank=True,
                                verbose_name='position')
    start_date = models.DateField(null=True, blank=True,
                                  verbose_name='start_date')
    end_date = models.DateField(null=True, blank=True, verbose_name='end_date')
    duties = models.TextField(max_length=3000, null=True, blank=True,
                              verbose_name='duties')


class RecruitEducation(models.Model):  # TeamRome
    """ Образование / Курсы / Университеты / Коледжы.
        ForeignKey = несколько образований у одного recruit."""
    recruit_edu = models.ForeignKey(to='Recruiter', on_delete=models.CASCADE)

    institution = models.CharField(max_length=100, null=True, blank=True,
                                   verbose_name='institution')
    subject_area = models.CharField(max_length=100, null=True, blank=True,
                                    verbose_name='Предметная область')
    specialization = models.CharField(max_length=100, null=True, blank=True,
                                      verbose_name='Специализация')
    qualification = models.CharField(max_length=100, null=True, blank=True,
                                     verbose_name='Квалификация')
    date_start = models.DateField(null=True, blank=True,
                                  verbose_name='дата начала')
    date_end = models.DateField(null=True, blank=True,
                                verbose_name='дата окончания')


class RecruitSkills(models.Model):  # TeamRome
    """ Навыки. ForeignKey = несколько навыков у одного recruit. """
    recruit_skills = models.ForeignKey(to='Recruiter',
                                       on_delete=models.CASCADE)

    skill = models.CharField(max_length=100, blank=True, null=True)


class RecruitCertificate(models.Model):  # TeamRome
    """ Сертификат: ссылка или картинка.
    ForeignKey = Несколько сертификатов может относиться к одному образованию. """
    education = models.ForeignKey(to='RecruitEducation',
                                  on_delete=models.CASCADE)

    img = models.ImageField(blank=True, null=True,
                            verbose_name='certificate_img')
    link = models.URLField(blank=True, null=True, max_length=100,
                           verbose_name='certificate_link')

    show_img = models.ImageField(blank=True, null=True)


class RecruitTelephone(models.Model):  # TeamRome
    """ Номера телефонов. ForeignKey = несколько телефонов у одного Клиента. """
    recruit_phone = models.ForeignKey(to='Recruiter', on_delete=models.CASCADE)

    telephone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.telephone_number


class RecruitPatternClient(models.Model):
    class Meta:
        verbose_name = "Шаблоны задач для клиента"
        verbose_name_plural = "Шаблоны задач для клиента"

    title = models.TextField(max_length=200)
    comment = models.TextField(max_length=300, blank=True)
    endtime = models.DateTimeField(blank=True, null=True)

    @property
    def show_all(self):
        return self.subtask.all()

    def __str__(self):
        return "Шаблон для %s" % (self.title)


class PatternSubTasks(models.Model):
    class Meta:
        verbose_name = "Шаблонная подзадача"
        verbose_name_plural = "Шаблонные подзадачи"

    title = models.TextField(max_length=100)
    task = models.ForeignKey(RecruitPatternClient, on_delete=models.CASCADE,
                             related_name="subtask")
    status = models.BooleanField(default=True)  # активная задача




