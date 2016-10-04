from django.contrib import admin

# Register your models here.
from inc.evaluation.models import EvaluationQuestion, EvaluationQuestionInputCase, EvaluationRecord


class EvaluationQuestionInputCaseAdminInline(admin.StackedInline):
    model = EvaluationQuestionInputCase
    can_delete = True


class EvaluationQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title','content','date_created')
    inlines = [EvaluationQuestionInputCaseAdminInline]


class EvaluationQuestionInputCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'case')


class EvaluationRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question')



admin.site.register(EvaluationQuestion, EvaluationQuestionAdmin)
admin.site.register(EvaluationQuestionInputCase, EvaluationQuestionInputCaseAdmin)
admin.site.register(EvaluationRecord, EvaluationRecordAdmin)