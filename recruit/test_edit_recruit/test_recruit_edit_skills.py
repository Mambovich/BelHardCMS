from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it
from recruit.models import Recruiter, RecruitSkills


class RecruiterEditSkillsTests(TestCase):
    """ python manage.py test recruit/test_edit_recruit/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'
    TEST_SKILLS = ['Python', 'Django']

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Recruiter.objects.create(recruiter=self.test_user)
        self.url = reverse('recruit_edit_skills')

    @time_it
    def test_page_open_user(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recruit/edit_pages/recruit_skills.html')

    @time_it
    def test_GET_nUnD(self):  # no user no data
        response = self.client.get(path=self.url)
        self.assertEqual(any(response.context['data'].values()), False)

    @time_it
    def test_POST_nUnD(self):  # no user no data
        response = self.client.post(path=self.url, data={'skill': ''})
        self.assertEqual(response.status_code, 302)

    @time_it
    def test_GET_wUnD(self):  # with user no data
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(path=self.url)
        self.assertEqual(any(response.context['data'].values()), False)

    @time_it
    def test_POST_wUnD(self):  # with user no data
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.post(path=self.url, data={'skill': ''})
        self.assertEqual(response.status_code, 302)

    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.get(self.url)
        for a, b in zip(response.context['data']['rec_skill'], self.TEST_SKILLS):
            self.assertEqual(a, b)

    @time_it
    def test_POST_user(self):
        """ request.POST this LoggedIn User. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data={'skill': self.TEST_SKILLS})

        for i in self.TEST_SKILLS:
            i_skill = RecruitSkills.objects.get(recruit_skills=self.client_inst, skill=i)
            self.assertEqual(i_skill.skill, i)

        self.assertEqual(response.status_code, 302)  # redirect


if __name__ == "__main__":
    RecruiterEditSkillsTests()
