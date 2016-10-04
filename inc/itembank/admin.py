from django.contrib import admin

# Register your models here.
from inc.itembank.models import Unit1, Unit2, Unit3, Question, Content, ChoiceItem, ImageItem, TestpaperRecord


class Unit1Admin(admin.ModelAdmin):
    list_display = ('id','title')


class Unit2Admin(admin.ModelAdmin):
    list_display = ('id','unit','title')


class Unit3Admin(admin.ModelAdmin):
    list_display = ('id', 'unit', 'title')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'unit', 'type', 'title', 'date_created', 'is_active')


class ChoiceItemInline(admin.StackedInline):
    model = ChoiceItem
    can_delete = True


class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'type', 'contents')
    inlines = [ChoiceItemInline]


class ChoiceItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'text')


class ImageItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'src')


class TestpaperRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'items', 'answer', 'date_created')


admin.site.register(Unit1, Unit1Admin)
admin.site.register(Unit2, Unit2Admin)
admin.site.register(Unit3, Unit3Admin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(ChoiceItem, ChoiceItemAdmin)
admin.site.register(ImageItem, ImageItemAdmin)
admin.site.register(TestpaperRecord, TestpaperRecordAdmin)