from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it
from client.models import Client


class ClientEditMainTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'
    TEST_MAIN = []

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit')

    @time_it
    def test_POST_user(self):
        """ request.POST this LoggedIn User. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data={
            'sex': self.TEST_MAIN, 'citizenship': self.TEST_MAIN, 'family_state': self.TEST_MAIN,
            'children': self.TEST_MAIN, 'country': self.TEST_MAIN, 'city': self.TEST_MAIN, 'state': self.TEST_MAIN,
        })

        for i in self.TEST_MAIN:
            i_client = Client.objects.get(client_skills=self.client_inst, skill=i)
            self.assertEqual(i_client, i)

        self.assertEqual(response.status_code, 302)

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(reverse('client_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_main.html')

    def test_POST_no_user(self):
        self.url = reverse('client_edit')
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)

    default_select_fields = ["'sex'", "'citizenship'", "'family_state'", "'children'", "'country'", "'city'", "'state'"]

    def test_GET_no_user(self):
        self.url = reverse('client_edit')
        response = self.client.get(self.url)
        # self.assertEqual(response.context['data'], self.default_select_fields)
        self.assertQuerysetEqual(response.context['data'], self.default_select_fields)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    ClientEditMainTests()
