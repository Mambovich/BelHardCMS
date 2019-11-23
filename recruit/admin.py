from django.contrib import admin

from recruit.models import Recruiter
from recruit.models import (RecruitSkills, RecruitExperience, RecruitEducation,
                             RecruitPatternClient, PatternSubTasks)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided,
as they make it unclear which names are present in the namespace,
confusing both readers and many automated tools. """


class InlineRecruitSkills(admin.TabularInline):  # TeamRome
    model = RecruitSkills


class InlineRecruitEducation(admin.TabularInline):  # TeamRome
    model = RecruitExperience


class InlineRecruitExperience(admin.TabularInline):  # TeamRome
    model = RecruitEducation


class RecruitAdmin(admin.ModelAdmin):  # TeamRome
    model = Recruiter
    inlines = [InlineRecruitEducation, InlineRecruitExperience, InlineRecruitSkills]


class PatternSubTask(admin.StackedInline):
    model = PatternSubTasks
    extra = 1


class PatternTaskAdmin(admin.ModelAdmin):
    model = RecruitPatternClient
    inlines = [PatternSubTask]


admin.site.register(Recruiter, RecruitAdmin)  # TeamRome
admin.site.register(RecruitPatternClient, PatternTaskAdmin)
