from django.contrib import admin

from recruit.models import RecruitReportsClients

from client.models import (SubTasks, CV, Vacancy, Help, Opinion, Answer, Chat,
                           Tasks, Message, Sex, Citizenship,
                           FamilyState, Children, City, EducationWord,
                           SkillsWord, Sphere, CvWord, Employment, TimeJob,
                           TypeSalary, State, Settings, FilesForJobInterviews,
                           JobInterviews, Experience, Education,
                           Client, Direction)

""" PEP 8: Wildcard imports (from <module> import *) should be avoided, 
as they make it unclear which names are present in the namespace, 
confusing both readers and many automated tools. """


class Subtasks_Inline(admin.StackedInline):
    model = SubTasks
    extra = 1


class Tasks_Admin(admin.ModelAdmin):
    inlines = [Subtasks_Inline]
    readonly_fields = ['endtime']


admin.site.register(CV)


class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'state', 'organization', 'address', 'employment', 'description',
        'skills', 'requirements', 'duties', 'conditions', 'creating_date',
    )
    list_display_links = (
        'state', 'organization', 'description', 'creating_date',
    )
    search_fields = (
        'state', 'organization', 'description', 'creating_date',
    )


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Help)
admin.site.register(RecruitReportsClients)
admin.site.register(Opinion)
admin.site.register(Answer)
admin.site.register(Chat)
admin.site.register(Tasks, Tasks_Admin)
admin.site.register(Message)


class SexAdmin(admin.ModelAdmin):
    model = Sex


class CitizenshipAdmin(admin.ModelAdmin):
    model = Citizenship


class FamilyStateAdmin(admin.ModelAdmin):
    model = FamilyState


class ChildrenAdmin(admin.ModelAdmin):
    model = Children


class CityAdmin(admin.ModelAdmin):
    model = City


class EducationWordAdmin(admin.ModelAdmin):
    model = EducationWord


class SkillsWordAdmin(admin.ModelAdmin):
    model = SkillsWord


class SphereAdmin(admin.ModelAdmin):
    model = Sphere


class CvWordAdmin(admin.ModelAdmin):
    model = CvWord


class EmploymentAdmin(admin.ModelAdmin):
    model = Employment


class TimeJobAdmin(admin.ModelAdmin):
    model = TimeJob


class TypeSalaryAdmin(admin.ModelAdmin):
    model = TypeSalary


class StateAdmin(admin.ModelAdmin):
    model = State


admin.site.register(Settings)
admin.site.register(Sex, SexAdmin)
admin.site.register(Citizenship, CitizenshipAdmin)
admin.site.register(FamilyState, FamilyStateAdmin)
admin.site.register(Children, ChildrenAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(EducationWord, EducationWordAdmin)
admin.site.register(SkillsWord, SkillsWordAdmin)
admin.site.register(Sphere, SphereAdmin)
admin.site.register(CvWord, CvWordAdmin)
admin.site.register(Employment, EmploymentAdmin)
admin.site.register(TimeJob, TimeJobAdmin)
admin.site.register(TypeSalary, TypeSalaryAdmin)
admin.site.register(State, StateAdmin)


class InlineFilesForJobInterviews(admin.TabularInline):
    model = FilesForJobInterviews


class InlineExp(admin.TabularInline):  # TeamRome
    model = Experience


class InlineEdu(admin.TabularInline):  # TeamRome
    model = Education


class InlineCV(admin.TabularInline):  # TeamRome
    model = CV


class ClientAdmin(admin.ModelAdmin):  # TeamRome
    model = Client
    inlines = [InlineExp, InlineEdu, InlineCV]


# TeamRome
admin.site.register(Client, ClientAdmin)


# TeamPoland
class JobInterviewsAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'name', 'location'
    )
    list_display_links = (
        'client', 'name', 'location'
    )
    search_fields = (
        'client', 'name', 'location'
    )

    model = JobInterviews
    inlines = [InlineFilesForJobInterviews]

    # class Media:
    #    js = ['js/scriptJob.js']


admin.site.register(JobInterviews, JobInterviewsAdmin)


class DirectionAdmin(admin.ModelAdmin):  # TeamRome
    model = Direction


admin.site.register(Direction, DirectionAdmin)  # TeamRome
