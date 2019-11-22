import re

from client.edit.utility import (time_it, try_except)


@try_except
@time_it
def pars_exp_request(req_post) -> list:  # TeamRome
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели Experience. """
    print("\texp_request.POST: %s" % req_post)
    arr = []  # output list
    dict_up = {'name': None, 'sphere': None, 'position': None,
               'start_date': None, 'end_date': None, 'duties': None}  # temporary dictionary
    count = 1  # crutch for detection Client Spheres in several forms
    for i in dict(req_post).items():
        # print("\ti: %s, %s" % (i[0], i[1]))

        if re.match('name', i[0]):  # 'name1': ['rocket_science_1']
            dict_up['name'] = i[1][0] if i[1][0] else None

        if re.match('sphere', i[0]):  # 'sphere1': ['1', '2']
            dict_up['sphere'] = req_post.getlist(i[0])

        if re.match('position', i[0]):  # 'position1': ['rocket_science_1'],
            dict_up['position'] = i[1][0] if i[1][0] else None

        if re.match('start_date', i[0]):  # 'start_date1': [''] or 'start_date1': ['2018-01-01']
            dict_up['start_date'] = i[1][0] if i[1][0] else None

        if re.match('end_date', i[0]):  # 'end_date1': [''] or 'end_date1': ['2018-02-02']
            dict_up['end_date'] = i[1][0] if i[1][0] else None

        if re.match('duties', i[0]):  # 'duties1': ['rocket_science_1']
            dict_up['duties'] = i[1][0] if i[1][0] else None

            """ Конец первого словаря из request.POST. 
            Сохраняем временный словарь в массив. Обнуляем временный словарь. """
            arr.append(dict_up)
            # print("\tdict_up: %s" % dict_up)
            dict_up = {'name': None, 'sphere': None, 'position': None,
                       'start_date': None, 'end_date': None, 'duties': None}
            count += 1
            # print('\t----')
    print("\tout_arr: %s" % arr)
    return arr


@try_except
@time_it
def pars_cv_request(req_post: dict) -> list:  # TeamRome
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели CV. """
    print("exp_request.POST: %s" % req_post)
    arr = []
    dict_up = {'position': None, 'direction': None, 'employment': None, 'time_job': None, 'salary': None,
               'type_salary': None}
    for i in req_post.items():
        # print("i: %s, %s" % (i[0], i[1]))

        if re.match('position', i[0]):
            dict_up['position'] = i[1] if i[1] else None

        if re.match('direction', i[0]):
            dict_up['direction'] = i[1] if i[1] else None

        if re.match('employment', i[0]):
            dict_up['employment'] = i[1] if i[1] else None

        if re.match('time_job', i[0]):
            dict_up['time_job'] = i[1] if i[1] else None

        if re.match('salary', i[0]):
            dict_up['salary'] = i[1] if i[1] else None

        if re.match('type_salary', i[0]):
            dict_up['type_salary'] = i[1] if i[1] else None

            # print(dict_up)
            arr.append(dict_up)
            dict_up = {'position': None, 'direction': None, 'employment': None, 'time_job': None, 'salary': None,
                       'type_salary': None}
            # print('----')

    print("arr: %s" % arr)
    return arr


@try_except
@time_it
def pars_edu_request(req_post, _file) -> list:  # TeamRome
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели Education. """
    print("\texp_request.POST: %s" % req_post)
    print("\texp_request.FILE: %s" % _file)
    arr = []  # output list
    dict_up = {'institution': None, 'subject_area': None, 'specialization': None, 'qualification': None,
               'date_start': None, 'date_end': None, 'certificate': None}  # temporary dictionary
    count_cert = 0  # crutch for detection Edu. Certificates in several forms
    cert_arr = []  # temporary certificate array

    for i in dict(req_post).items():
        # print("\ti: %s, %s" % (i[0], i[1]))

        if re.match('institution', i[0]):  # 'institution': ['rocket_science_1']

            if any(dict_up.values()):
                """ If it is a next Edu. dictionary from POST. Clean all temporary objects. """
                cert_arr = []
                # print("\tdict_up: %s" % dict_up)
                arr.append(dict_up)
                dict_up = {'institution': None, 'subject_area': None, 'specialization': None, 'qualification': None,
                           'date_start': None, 'date_end': None, 'certificate': None}
                # print('\t----')

            dict_up['institution'] = i[1][0] if i[1][0] else None

        if re.match('subject_area', i[0]):  # 'subject_area': ['rocket_science_1']
            dict_up['subject_area'] = i[1][0] if i[1][0] else None

        if re.match('specialization', i[0]):  # 'specialization': ['rocket_science_1']
            dict_up['specialization'] = i[1][0] if i[1][0] else None

        if re.match('qualification', i[0]):  # 'qualification': ['rocket_science_1']
            dict_up['qualification'] = i[1][0] if i[1][0] else None

        if re.match('date_start', i[0]):  # 'date_start': [''] or 'date_start': ['2018-01-01']
            dict_up['date_start'] = i[1][0] if i[1][0] else None

        if re.match('date_end', i[0]):  # 'date_end': [''] or 'date_end': ['2019-11-22']
            dict_up['date_end'] = i[1][0] if i[1][0] else None

        if re.match('certificate_url', i[0]):  # 'certificate_url': ['http://127.0.0.1:8000/qwe']
            url = i[1][0] if i[1][0] else None
            img = None
            count_img = 0
            count_cert += 1
            """ request.FILE == MultiValueDict{'key': [<InMemoryUploadedFile: x.png (image/png)>]} """
            for f in dict(_file).items():
                count_img += 1
                if count_img == count_cert:
                    """ URL and Img gos in pairs. 
                    So we need to compare url № and take img with this number:
                    1st url and 1st img, than 2d url and 2d img from FILE dictionary. """
                    # print("\tf: %s, %s" % (f[0], f[1]))
                    # f: certificate_img11, [<InMemoryUploadedFile: 123.png (image/png)>]
                    img = f[1][0] if f[1][0] else None
                    break

            cert_arr.append((url, img))
            dict_up['certificate'] = cert_arr

    """ For loop ends - save temporary dictionary to the output arr. """
    # print("\tdict_up: %s" % dict_up)
    arr.append(dict_up)
    print("\tout_arr: %s" % arr)
    return arr
