from django.test import TestCase
from django.urls import reverse


class ClientEditMainTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'admin'
    TEST_USER_PASSWORD = 'admin'

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(reverse('client_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_main.html')


if __name__ == "__main__":
    ClientEditMainTests()
