import os
import sys

import django
from django.test import TestCase
from django.urls import reverse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelHardCRM.settings")
django.setup()


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
