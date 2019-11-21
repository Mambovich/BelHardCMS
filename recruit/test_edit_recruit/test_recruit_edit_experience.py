from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it
from client.models import Sphere
from recruit.models import Recruiter, RecruitExperience


class RecruiterEditExperienceTests(TestCase):
    """ python manage.py test recruit/test_edit_recruit/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'

    TEST_DATA_1 = {'name': 'rocket_science_1',
                   'sphere': Sphere.objects.all().first().id,
                   'position': 'rocket_science_1',
                   'start_date': date(2018, 1, 1),
                   'end_date': date.today(),
                   'duties': 'Hello',
                   }

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Recruiter.objects.create(recruiter=self.test_user)
        self.url = reverse('recruit_edit_experience')

    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        exp = RecruitExperience.objects.create(recruit_exp=self.client_inst,
                                               name=self.TEST_DATA_1['name'],
                                               position=self.TEST_DATA_1['position'],
                                               start_date=self.TEST_DATA_1['start_date'],
                                               end_date=self.TEST_DATA_1['end_date'],
                                               duties=self.TEST_DATA_1['duties'],
                                               )
        exp.sphere.add(self.TEST_DATA_1['sphere'])

        exp_arr = [{'id': exp.id,
                    'recruit_exp_id': self.client_inst.id,
                    'name': self.TEST_DATA_1['name'],
                    'sphere': [Sphere.objects.get(id=self.TEST_DATA_1['sphere']).sphere_word],
                    'position': self.TEST_DATA_1['position'],
                    'start_date': self.TEST_DATA_1['start_date'] if self.TEST_DATA_1[
                        'start_date'] else None,
                    'end_date': self.TEST_DATA_1['end_date'] if self.TEST_DATA_1['end_date'] else None,
                    'duties': self.TEST_DATA_1['duties'],
                    }]
        response = self.client.get(self.url)
        self.assertEqual(response.context['data']['rec_exp'], exp_arr)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_user(self):
        """ request.POST with LoggedIn User and TEST_DATA_1. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA_1)

        rec_exp = RecruitExperience.objects.get(recruit_exp=self.client_inst)

        self.assertEqual(rec_exp.name, self.TEST_DATA_1['name'])
        self.assertEqual(rec_exp.sphere.first().id, self.TEST_DATA_1['sphere'])
        self.assertEqual(rec_exp.position, self.TEST_DATA_1['position'])
        self.assertEqual(rec_exp.start_date, self.TEST_DATA_1['start_date'])
        self.assertEqual(rec_exp.end_date, self.TEST_DATA_1['end_date'])
        self.assertEqual(rec_exp.duties, self.TEST_DATA_1['duties'])

        self.assertEquals(response.status_code, 302)  # redirect


if __name__ == "__main__":
    RecruiterEditExperienceTests()
