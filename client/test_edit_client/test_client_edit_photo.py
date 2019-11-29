from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.edit_forms import UploadImgForm
from client.models import Client


class ClientEditPhotoTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit_photo')

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_photo.html')

    def test_POST_no_user(self):
        """ request.POST without User Login - AnonymousUser. """
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)

    default_select_fields = []

    # def test_GET_no_user(self):  # не работает
    #     response = self.client.get(self.url)
    #     self.assertQuerysetEqual(response.context['form'].values(), [])


if __name__ == "__main__":
    ClientEditPhotoTests()
