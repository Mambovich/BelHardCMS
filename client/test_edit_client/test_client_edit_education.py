from datetime import date

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse

from client.edit.utility import time_it
from client.models import Client, Education, Certificate

""" НЕ проверено сохранение файла сертификата """


class ClientEditEducationTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'
    # with open("client/test_edit_client/user_1.png") as file:

    image = Image.open("client/media/user_1.png")

    TEST_DATA_1 = {'institution': 'rocket_science_1',
                   'subject_area': 'rocket_science_1',
                   'specialization': 'rocket_science_1',
                   'qualification': 'rocket_science_1',
                   'date_start': date(2018, 1, 1),
                   'date_end': date.today(),
                   'certificate': ('http://127.0.0.1:8000/qwe', ''),  # (url, img)
                   'certificate_url': 'http://127.0.0.1:8000/qwe',
                   }

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit_education')

    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        edu = Education.objects.create(client_edu=self.client_inst,
                                       institution=self.TEST_DATA_1['institution'],
                                       subject_area=self.TEST_DATA_1['subject_area'],
                                       specialization=self.TEST_DATA_1['specialization'],
                                       qualification=self.TEST_DATA_1['qualification'],
                                       date_start=self.TEST_DATA_1['date_start'] if self.TEST_DATA_1[
                                           'date_start'] else None,
                                       date_end=self.TEST_DATA_1['date_end'] if self.TEST_DATA_1['date_end'] else None,
                                       )
        certificate = Certificate.objects.create(education=edu,
                                                 link=self.TEST_DATA_1['certificate'][0],
                                                 img=self.TEST_DATA_1['certificate'][1],
                                                 )
        edu_arr = [{'id': edu.id,
                    'client_edu_id': self.client_inst.id,
                    'institution': self.TEST_DATA_1['institution'],
                    'subject_area': self.TEST_DATA_1['subject_area'],
                    'specialization': self.TEST_DATA_1['specialization'],
                    'qualification': self.TEST_DATA_1['qualification'],
                    'date_start': self.TEST_DATA_1['date_start'] if self.TEST_DATA_1[
                        'date_start'] else None,
                    'date_end': self.TEST_DATA_1['date_end'] if self.TEST_DATA_1['date_end'] else None,
                    'cert': [{'id': certificate.id,
                              'education_id': certificate.education_id,
                              'img': '/media/' + str(
                                  self.TEST_DATA_1['certificate'][1] if self.TEST_DATA_1['certificate'][1] else ''),
                              'link': self.TEST_DATA_1['certificate'][0],
                              'show_img': certificate.show_img if certificate.show_img else ''}],
                    }]
        # print("\ttest edu_arr: %s" % edu_arr)
        response = self.client.get(self.url)
        self.assertEqual(response.context['data']['cl_edu'], edu_arr)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_user(self):
        """ request.POST with LoggedIn User and TEST_DATA_1. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA_1, content_type=MULTIPART_CONTENT)

        user_edu = Education.objects.get(client_edu=self.client_inst)
        user_cert = Certificate.objects.get(education=user_edu.id)

        self.assertEqual(user_edu.subject_area, self.TEST_DATA_1['subject_area'])
        self.assertEqual(user_edu.specialization, self.TEST_DATA_1['specialization'])
        self.assertEqual(user_edu.qualification, self.TEST_DATA_1['qualification'])
        self.assertEqual(user_edu.date_start, self.TEST_DATA_1['date_start'])
        self.assertEqual(user_edu.date_end, self.TEST_DATA_1['date_end'])
        self.assertEqual(user_cert.img, self.TEST_DATA_1['certificate'][1])
        self.assertEqual(user_cert.link, self.TEST_DATA_1['certificate'][0])

        self.assertEquals(response.status_code, 302)  # redirect


if __name__ == "__main__":
    ClientEditEducationTests()
