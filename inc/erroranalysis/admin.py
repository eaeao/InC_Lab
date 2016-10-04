from django.contrib import admin

# Register your models here.
from inc.erroranalysis.models import ErrorAnalysisResult


class ErrorAnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','type','date_created')

admin.site.register(ErrorAnalysisResult, ErrorAnalysisResultAdmin)