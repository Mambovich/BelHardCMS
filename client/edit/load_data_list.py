import json

from django.http import HttpResponse
from django.views.generic import TemplateView

from client.edit.utility import try_except
from client.models import (SkillsWord, EducationWord, CvWord)


class SkillsDataList(TemplateView):  # TeamRome
    @try_except
    def get(self, request, *args, **kwargs):
        # print('SkillsDataList.GET: %s' % request.GET)
        words = [i.skills_word for i in SkillsWord.objects.all()]
        json_data = json.dumps({'words': words}, ensure_ascii=False)
        return HttpResponse(json_data)


class InstitutionDataList(TemplateView):  # TeamRome
    @try_except
    def get(self, request, *args, **kwargs):
        # print('InstitutionDataList.GET: %s' % request.GET)
        words = [i.education_word for i in EducationWord.objects.all()]
        json_data = json.dumps({'words': words}, ensure_ascii=False)
        return HttpResponse(json_data)


class CvPositionDataList(TemplateView):  # TeamRome
    @try_except
    def get(self, request, *args, **kwargs):
        # print('CvPositionDataList.GET: %s' % request.GET)
        words = [i.position_word for i in CvWord.objects.all()]
        json_data = json.dumps({'words': words}, ensure_ascii=False)
        return HttpResponse(json_data)
