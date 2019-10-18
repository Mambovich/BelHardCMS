import re

from time import perf_counter


# TeamRome
def pars_exp_request(req_post) -> list:
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели Experience. """
    print("pars_exp_request()")
    # print("\texp_request.POST: %s" % req_post)
    time_0 = perf_counter()

    arr = []  # выходной массив
    dict_up = {'experience_1': '', 'experience_2': '', 'experience_3': '',
               'exp_date_start': '', 'exp_date_end': '', 'experience_4': ''}  # временный словарь
    count = 0  # костыль для обнаружения Сферы деятельности в нескольких формах
    for i in dict(req_post).items():
        # print("\ti: %s, %s" % (i[0], i[1]))
        if re.match('experience_11', i[0]):  # i: experience_11, ['qwe1 qwe1']
            dict_up['experience_1'] = i[1][0]

        if re.match('experience_21', i[0]):  # i: experience_21, ['1', '2']
            if count:  # if count > 0 ->   getlist('experience_21N')
                dict_up['experience_2'] = req_post.getlist('experience_21%s' % count)
            else:  # if count == 0
                dict_up['experience_2'] = req_post.getlist('experience_21')

        if re.match('experience_31', i[0]):  # i: experience_31, ['qwe1 qwe1']
            dict_up['experience_3'] = i[1][0]

        if re.match('exp_date_start1', i[0]):  # i: exp_date_start1, [''] or exp_date_start1, ['2019-10-06']
            dict_up['exp_date_start'] = i[1][0] if i[1][0] else None

        if re.match('exp_date_end1', i[0]):  # i: exp_date_end1, [''] or exp_date_end1, ['2019-10-17']
            dict_up['exp_date_end'] = i[1][0] if i[1][0] else None

        if re.match('experience_41', i[0]):  # i: experience_41, ['qwe1 qwe1']
            dict_up['experience_4'] = i[1][0]

            """ Конец первого словаря из request.POST. 
            Сохраняем временный словарь в массив. Обнуляем временный словарь. """
            arr.append(dict_up)
            # print("\tdict_up: %s" % dict_up)
            dict_up = {'experience_1': '', 'experience_2': '', 'experience_3': '',
                       'exp_date_start': '', 'exp_date_end': '', 'experience_4': ''}
            count += 1
            # print('\t----')
    print('\tpars_exp_request() - OK; TIME: %s sec' % (perf_counter() - time_0))
    print("\tout_arr: %s" % arr)
    return arr


# TeamRome
def pars_cv_request(req_post: dict) -> list:
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели CV. """
    print("pars_cv_request()")
    # print("exp_request.POST: %s" % req_post)
    from time import perf_counter
    time_0 = perf_counter()

    arr = []
    dict_up = {'position': '', 'employment': '', 'time_job': '', 'salary': '', 'type_salary': ''}
    for i in req_post.items():
        # print("i: %s, %s" % (i[0], i[1]))

        if re.match('position', i[0]):
            dict_up['position'] = i[1]

        if re.match('employment', i[0]):
            dict_up['employment'] = i[1]

        if re.match('time_job', i[0]):
            dict_up['time_job'] = i[1]

        if re.match('salary', i[0]):
            dict_up['salary'] = i[1]

        if re.match('type_salary', i[0]):
            dict_up['type_salary'] = i[1]

            # print(dict_up)
            arr.append(dict_up)
            dict_up = {'position': '', 'employment': '', 'time_job': '', 'salary': '', 'type_salary': ''}
            # print('----')

    print('time_it = %s sec' % (perf_counter() - time_0))
    print("arr: %s" % arr)
    return arr


# TeamRome
def pars_edu_request(req_post, _file) -> list:
    """ Опасно для глаз!!! Быдло-код !!!
    Парсит QueryDict == request.POST в список из нескольких словарей, отсортированных по полям модели Education. """
    print("pars_edu_request()")
    # print("exp_request.POST: %s" % req_post)
    # print("exp_request.FILE: %s" % _file)
    from time import perf_counter
    time_0 = perf_counter()

    arr = []
    dict_up = {'institution': '', 'subject_area': '', 'specialization': '', 'qualification': '',
               'date_start': '', 'date_end': '', 'certificate_img': '', 'certificate_url': ''}
    count = 0
    for i in req_post.items():
        # print("i: %s, %s" % (i[0], i[1]))

        if re.match('institution', i[0]):
            dict_up['institution'] = i[1]

        if re.match('subject_area', i[0]):
            dict_up['subject_area'] = i[1]

        if re.match('specialization', i[0]):
            dict_up['specialization'] = i[1]

        if re.match('qualification', i[0]):
            dict_up['qualification'] = i[1]

        if re.match('date_start', i[0]):
            dict_up['date_start'] = i[1]

        if re.match('date_end', i[0]):
            dict_up['date_end'] = i[1]

        if re.match('certificate_url', i[0]):
            dict_up['certificate_url'] = i[1]  # req_post.getlist('certificate_url')

            """ request.FILE == MultiValueDict{'key': [<InMemoryUploadedFile: x.png (image/png)>]} """
            for f in _file.items():
                if re.match('certificate_img[0-9][0-9]?', f[0]):
                    if (str(f[0])[-1] == str(count)) or (count == 0):
                        dict_up['certificate_img'] = f[1]
                        break

            # print(dict_up)
            arr.append(dict_up)
            dict_up = {'institution': '', 'subject_area': '', 'specialization': '', 'qualification': '',
                       'date_start': '', 'date_end': '', 'certificate_img': '', 'certificate_url': ''}
            count += 1
            # print('----')

    print('time_it = %s sec' % (perf_counter() - time_0))
    print("arr: %s" % arr)
    return arr
