from BelHardCRM.settings import MEDIA_URL
from client.edit.log_color import (log_info, log_error)
from client.edit.utility import try_except, time_it
from client.models import Client


# @try_except
# @time_it
def client_check(some_one):  # TeamRome
    """ список карточек c id клиента.
    Список Юзеров с зарегистрированной карточкой клиента. """
    client_id_list = [i.user_client_id for i in Client.objects.all()]
    log_info("\tclient_id_list: %s" % client_id_list)

    """ Имя юзера и его ID. """
    log_info("\tuser_name: %s, user_id: %s" % (some_one, some_one.id))

    """ Проверка: есть ли текущий Юзер в списке Клиентов. """
    if some_one.id in client_id_list:
        """ Если он есть - возвращаем Объект Клиента. """
        client = Client.objects.get(user_client=some_one)
        log_info("\tclient_id: %s" % client.id)
        return client
    else:
        log_error('\tClient profile DOES NOT exists!')
        return None


# @try_except
def load_client_img(client):  # TeamRome
    """ Show Client Img in the Navigation Bar.
    Img loaded from DB, if user do not have img - load default. """
    if client:
        if client.img:
            return "%s%s" % (MEDIA_URL, client.img)
    return '/media/user_1.png'
