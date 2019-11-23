from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it
from client.models import Client


class ClientProfileTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.recruit_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_profile')

    @time_it
    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_profile.html')

    @time_it
    def test_GET_nUnD(self):  # no user no data
        response = self.client.get(path=self.url)
        self.assertEqual(any(response.context['data'].values()), False)
        # self.assertEqual(response.context['data'], False)

    @time_it
    def test_GET_WUnD(self):  # no user no data
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(path=self.url)
        # self.assertEqual(any(response.context['data'].values()), False)
        self.assertEqual(response.context['data']['cl_edu_profile'], [])
        self.assertEqual(response.context['data']['cl_exp_profile'], [])
        self.assertEqual(response.context['data']['cl_cvs_profile'], [])
        self.assertEqual(response.context['data']['cl_skill_profile'], [])
        self.assertEqual(response.context['data']['user_model'],
                         {'first_name': '', 'last_name': '', 'email': 'test_user'})
        self.assertEqual(response.context['data']['cl_phone'], [])
        self.assertEqual(response.context['data']['age'], None)
        self.assertEqual(response.context['data']['client'].user_client.email, self.TEST_USER_EMAIL)


if __name__ == "__main__":
    ClientProfileTests()
