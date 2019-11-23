from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.pages_get import cv_page_get
from client.edit.utility import time_it
from client.models import Client, CV, Employment, TimeJob, TypeSalary, Direction


class ClientEditCVTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'
    TEST_DATA_1 = {'position': 'jun',
                   'direction': Direction.objects.all().first().id,  # pre defined array
                   'employment': Employment.objects.all().first().id,  # pre defined array
                   'time_job': TimeJob.objects.all().first().id,  # pre defined array
                   'salary': '100',
                   'type_salary': TypeSalary.objects.all().first().id,  # pre defined array
                   }

    TEST_DATA_2 = {'position': '',
                   'direction': '',
                   'employment': '',
                   'time_job': TimeJob.objects.all().first().id,
                   'salary': '',
                   'type_salary': '',
                   }

    TEST_DATA_3 = {'position1': '',  # 1
                   'direction1': '',
                   'employment1': '',
                   'time_job1': TimeJob.objects.all().first().id,
                   'salary1': '',
                   'type_salary1': '',
                   'position2': '',  # 2
                   'direction2': '',
                   'employment2': '',
                   'time_job2': TimeJob.objects.all().first().id,
                   'salary2': '',
                   'type_salary2': '',
                   }

    TEST_DATA_4 = {'position1': 'abc',  # 1
                   'direction1': Direction.objects.all().first().id,
                   'employment1': Employment.objects.all().first().id,
                   'time_job1': TimeJob.objects.all().first().id,
                   'salary1': '111',
                   'type_salary1': TypeSalary.objects.all().first().id,
                   'position2': 'def',  # 2
                   'direction2': Direction.objects.all()[1].id,
                   'employment2': Employment.objects.all()[1].id,
                   'time_job2': TimeJob.objects.all()[1].id,
                   'salary2': '222',
                   'type_salary2': TypeSalary.objects.all()[1].id,
                   }

    default_select_fields = ["'employment'", "'time_job'", "'type_salary'", "'direction'"]

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit_cv')

    @time_it
    def test_page_open(self):
        """ Open URL = client/edit/cv/ """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_cv.html')

    @time_it
    def test_GET_no_user(self):
        """ Open page without User Login - AnonymousUser. """
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data'], self.default_select_fields)

    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        cv = CV.objects.create(client_cv=self.client_inst,
                               position=self.TEST_DATA_1['position'],
                               direction=Direction.objects.get(id=self.TEST_DATA_1['direction']),
                               employment=Employment.objects.get(id=self.TEST_DATA_1['employment']),
                               time_job=TimeJob.objects.get(id=self.TEST_DATA_1['time_job']),
                               salary=self.TEST_DATA_1['salary'],
                               type_salary=TypeSalary.objects.get(id=self.TEST_DATA_1['type_salary']),
                               )
        cv_arr = [{'id': cv.id,
                   'client_cv_id': self.client_inst.id,
                   'position': self.TEST_DATA_1['position'],
                   'direction_id': self.TEST_DATA_1['direction'],
                   'employment_id': self.TEST_DATA_1['employment'],
                   'time_job_id': self.TEST_DATA_1['time_job'],
                   'salary': self.TEST_DATA_1['salary'],
                   'type_salary_id': self.TEST_DATA_1['type_salary'],
                   }]
        response = self.client.get(self.url)
        # print(response.context['data']['cl_cvs'])
        self.assertEqual(response.context['data']['cl_cvs'], cv_arr)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_no_user(self):
        """ request.POST without User Login - AnonymousUser. """
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)  # redirect

    @time_it
    def test_POST_user(self):
        """ request.POST with LoggedIn User and TEST_DATA_2. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA_1)  # saves to DB ????

        user_cv = CV.objects.get(client_cv=self.client_inst)

        self.assertEqual(user_cv.position, self.TEST_DATA_1['position'])
        self.assertEqual(user_cv.direction, Direction.objects.get(id=self.TEST_DATA_1['direction']))
        self.assertEqual(user_cv.employment, Employment.objects.get(id=self.TEST_DATA_1['employment']))
        self.assertEqual(user_cv.time_job, TimeJob.objects.get(id=self.TEST_DATA_1['time_job']))
        self.assertEqual(user_cv.salary, self.TEST_DATA_1['salary'])
        self.assertEqual(user_cv.type_salary, TypeSalary.objects.get(id=self.TEST_DATA_1['type_salary']))

        self.assertEquals(response.status_code, 302)  # redirect

    @time_it
    def test_POST_user_2(self):
        """ request.POST with LoggedIn User and TEST_DATA_2. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA_2)  # saves to DB ????

        user_cv = CV.objects.get(client_cv=self.client_inst)

        self.assertEqual(user_cv.position, None)
        self.assertEqual(user_cv.direction, None)
        self.assertEqual(user_cv.employment, None)
        self.assertEqual(user_cv.time_job, TimeJob.objects.get(id=self.TEST_DATA_2['time_job']))
        self.assertEqual(user_cv.salary, None)
        self.assertEqual(user_cv.type_salary, None)

        self.assertEquals(response.status_code, 302)  # redirect

    @time_it
    def test_POST_user_3(self):
        """ request.POST with LoggedIn User and TEST_DATA_3. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA_3)  # saves to DB ????

        user_cvs = CV.objects.filter(client_cv=self.client_inst)
        print("t3_val: %s" % user_cvs.values())
        for cv, count in zip(user_cvs, range(1, len(user_cvs) + 1)):
            self.assertEqual(cv.position, None)
            self.assertEqual(cv.direction, None)
            self.assertEqual(cv.employment, None)
            self.assertEqual(cv.time_job, TimeJob.objects.get(id=self.TEST_DATA_3['time_job%s' % count]))
            self.assertEqual(cv.salary, None)
            self.assertEqual(cv.type_salary, None)

        self.assertEquals(response.status_code, 302)  # redirect

        cv_arr = cv_page_get(self.client_inst)['cl_cvs']
        # print(cv_arr)
        response = self.client.get(self.url)
        # print(response.context['data']['cl_cvs'])
        self.assertEqual(response.context['data']['cl_cvs'], cv_arr)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_user_4(self):
        """ request.POST with LoggedIn User and TEST_DATA_4. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA_4)  # saves to DB ????

        user_cvs = CV.objects.filter(client_cv=self.client_inst)
        print("t4_val: %s" % user_cvs.values())
        for cv, count in zip(user_cvs, range(1, len(user_cvs) + 1)):
            print(type(cv), count)
            self.assertEqual(cv.position, self.TEST_DATA_4['position%s' % count])
            self.assertEqual(cv.direction, Direction.objects.get(id=self.TEST_DATA_4['direction%s' % count]))
            self.assertEqual(cv.employment, Employment.objects.get(id=self.TEST_DATA_4['employment%s' % count]))
            self.assertEqual(cv.time_job, TimeJob.objects.get(id=self.TEST_DATA_4['time_job%s' % count]))
            self.assertEqual(cv.salary, self.TEST_DATA_4['salary%s' % count])
            self.assertEqual(cv.type_salary, TypeSalary.objects.get(id=self.TEST_DATA_4['type_salary%s' % count]))

        self.assertEquals(response.status_code, 302)  # redirect

        cv_arr = cv_page_get(self.client_inst)['cl_cvs']
        # print(cv_arr)
        response = self.client.get(self.url)
        # print(response.context['data']['cl_cvs'])
        self.assertEqual(response.context['data']['cl_cvs'], cv_arr)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    ClientEditCVTests()
