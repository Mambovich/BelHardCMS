from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it
from recruit.models import Recruiter


class RecruiterProfileTests(TestCase):
    """ python manage.py test recruit/test_edit_recruit/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.recruit_inst = Recruiter.objects.create(recruiter=self.test_user)
        self.url = reverse('recruit_profile')

    @time_it
    def test_page_open_user(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruit/recruit_profile.html')

    @time_it
    def test_GET_nUnD(self):  # no user no data
        response = self.client.get(path=self.url)
        self.assertEqual(any(response.context['data'].values()), False)

    @time_it
    def test_GET_WUnD(self):  # no user no data
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(path=self.url)
        # self.assertEqual(any(response.context['data'].values()), False)
        self.assertEqual(response.context['data']['r_edu_profile'], [])
        self.assertEqual(response.context['data']['r_exp_profile'], [])
        self.assertEqual(response.context['data']['r_skill_profile'], [])
        self.assertEqual(response.context['data']['user_model'],
                         {'first_name': '', 'last_name': '', 'email': 'test_user'})
        self.assertEqual(response.context['data']['r_phone'], [])
        self.assertEqual(response.context['data']['age'], None)
        self.assertEqual(response.context['data']['recruit'].recruiter.email, self.TEST_USER_EMAIL)


if __name__ == "__main__":
    RecruiterProfileTests()
