from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

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


if __name__ == "__main__":
    RecruiterProfileTests()
