import os
import sys

import django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelHardCRM.settings")
django.setup()

from client.models import Client


class ClientEditExperienceTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit_experience')


if __name__ == "__main__":
    ClientEditExperienceTests()
