from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it
from client.models import Sex, Citizenship, FamilyState, Children, City, State
from recruit.models import Recruiter, UserModel, RecruitTelephone


class RecruiterEditMainTests(TestCase):
    """ python manage.py test recruit/test_edit_recruit/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'

    default_select_fields = ["'sex'", "'citizenship'", "'family_state'", "'children'", "'country'", "'city'", "'state'"]

    TEST_DATA_1 = {
        'recruit_first_name': 'ikikikik',
        'recruit_last_name': 'hmdmklsrisr',
        'recruit_middle_name': 'zxcawqdcbergve',
        'sex': Sex.objects.all().first(),
        'date_born': date(1991, 1, 1),
        'citizenship': Citizenship.objects.all().first(),
        'family_state': FamilyState.objects.all().first(),
        'children': Children.objects.all().first(),
        'country': Citizenship.objects.all().last(),
        'city': City.objects.all().first(),
        'street': 'momomomoomo',
        'house': '666d',
        'flat': '13',
        'telegram_link': '@helly',
        'skype_id': 'madman',
        'email': 'asdasdasd@mail.ru',
        'link_linkedin': 'like-a-pro',
        'state': State.objects.all().first(),
        'phone': ['+31231312', '+8171231'],
    }

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Recruiter.objects.create(recruiter=self.test_user)
        self.url = reverse('recruit_edit')

    @time_it
    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruit/edit_pages/recruit_edit_main.html')

    @time_it
    def test_GET_no_user(self):
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data'], self.default_select_fields)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_GET_with_user(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        self.client_inst.patronymic = self.TEST_DATA_1['recruit_middle_name']

        response = self.client.get(self.url)
        self.assertEqual(response.context['data']['recruit'], self.client_inst)

        self.assertEqual(response.context['data']['user_model']['email'],
                         UserModel.objects.get(id=self.client_inst.recruiter_id).email)

        # self.assertEqual(response.context['data']['sex'], Sex.objects.all())  # почему они разные ?
        # self.assertEquals(response.context['data']['citizenship'], Citizenship.objects.all())

        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_with_user(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.post(path=self.url, data=self.TEST_DATA_1)

        get_recruit_obj = Recruiter.objects.get(id=self.client_inst.id)
        print(get_recruit_obj)

        self.assertEqual([i.telephone_number for i in RecruitTelephone.objects.filter(recruit_phone=self.client_inst)],
                         self.TEST_DATA_1['phone'])

        self.assertEqual(get_recruit_obj.recruiter.first_name, self.TEST_DATA_1['recruit_first_name'])
        self.assertEqual(get_recruit_obj.recruiter.last_name, self.TEST_DATA_1['recruit_last_name'])
        self.assertEqual(get_recruit_obj.patronymic, self.TEST_DATA_1['recruit_middle_name'])
        self.assertEqual(get_recruit_obj.sex, self.TEST_DATA_1['sex'])
        self.assertEqual(get_recruit_obj.date_born, self.TEST_DATA_1['date_born'])
        self.assertEqual(get_recruit_obj.r_citizenship, self.TEST_DATA_1['citizenship'])
        self.assertEqual(get_recruit_obj.family_state, self.TEST_DATA_1['family_state'])
        self.assertEqual(get_recruit_obj.children, self.TEST_DATA_1['children'])
        self.assertEqual(get_recruit_obj.r_country, self.TEST_DATA_1['country'])
        self.assertEqual(get_recruit_obj.city, self.TEST_DATA_1['city'])
        self.assertEqual(get_recruit_obj.street, self.TEST_DATA_1['street'])
        self.assertEqual(get_recruit_obj.house, self.TEST_DATA_1['house'])
        self.assertEqual(get_recruit_obj.flat, self.TEST_DATA_1['flat'])
        self.assertEqual(get_recruit_obj.telegram_link, self.TEST_DATA_1['telegram_link'])
        self.assertEqual(get_recruit_obj.link_linkedin, self.TEST_DATA_1['link_linkedin'])
        self.assertEqual(get_recruit_obj.skype, self.TEST_DATA_1['skype_id'])
        self.assertEqual(get_recruit_obj.recruiter.email, self.TEST_DATA_1['email'])
        self.assertEqual(get_recruit_obj.state, self.TEST_DATA_1['state'])

        self.assertEquals(response.status_code, 302)  # redirect



if __name__ == "__main__":
    RecruiterEditMainTests()
